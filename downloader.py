import os
import sys
import re
import time
import urllib.parse
import urllib.request
import threading
import mimetypes
import json
import queue
import requests
import yt_dlp
import customtkinter
from tkinter import filedialog, messagebox

# --- CONFIGURACIÓN DE RUTAS Y DATOS PERSISTENTES ---

SETTINGS_DIR = os.path.join(os.environ.get('USERPROFILE', os.path.expanduser('~')), 'AppData', 'Local', 'Programs', 'WhatsAppDownloader')
SETTINGS_FILE = os.path.join(SETTINGS_DIR, 'settings.json')

def load_settings():
    """Carga los ajustes persistentes desde un archivo JSON, con valores por defecto."""
    default_settings = {
        "always_ask_path": True,
        "default_dir": os.path.join(os.environ.get('USERPROFILE', os.path.expanduser('~')), 'Desktop'),
        "yt_quality": "Calidad Máxima (Best)",
        "yt_subs": False,
        "yt_thumbnail": False,
        "yt_metadata": False,
        "yt_extra_args": "",
        "http_timeout": 30,
        "http_retries": 3,
        "http_user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "gui_mode": "dark",
        "gui_color": "green"
    }
    os.makedirs(SETTINGS_DIR, exist_ok=True)
    if os.path.exists(SETTINGS_FILE):
        try:
            with open(SETTINGS_FILE, 'r', encoding='utf-8') as f:
                saved = json.load(f)
                default_settings.update(saved)
        except Exception:
            pass
    return default_settings

def save_settings(settings):
    """Guarda los ajustes actuales en el archivo JSON persistente."""
    try:
        os.makedirs(SETTINGS_DIR, exist_ok=True)
        with open(SETTINGS_FILE, 'w', encoding='utf-8') as f:
            json.dump(settings, f, indent=4, ensure_ascii=False)
    except Exception:
        pass

# Carga de configuraciones global para iniciar la interfaz
app_settings = load_settings()

# Asegurar codificación UTF-8 para stdout y stderr en terminales de Windows
if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass
if hasattr(sys.stderr, 'reconfigure'):
    try:
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

# Configuración inicial del tema visual cargado de la configuración
customtkinter.set_appearance_mode(app_settings.get("gui_mode", "dark"))
customtkinter.set_default_color_theme(app_settings.get("gui_color", "green"))

# --- FUNCIONES DE VALIDACIÓN ---

def validate_url(url):
    """Valida la URL introducida y añade protocolo si falta."""
    url = url.strip()
    if not url:
        return None
    if not (url.startswith("http://") or url.startswith("https://")):
        if "." in url and " " not in url:
            return "https://" + url
        return None
    return url

def is_youtube_url(url):
    """Determina si una URL pertenece a YouTube."""
    try:
        parsed = urllib.parse.urlparse(url)
        domain = parsed.netloc.lower()
        return any(pattern in domain for pattern in ['youtube.com', 'youtu.be', 'youtube-nocookie.com'])
    except Exception:
        return False

# --- COMPONENTES DE LA INTERFAZ GRÁFICA (GUI) ---

class ChatListItem(customtkinter.CTkFrame):
    """Componente que representa un 'chat' (vista) en la barra lateral de WhatsApp."""
    def __init__(self, master, avatar, name, status, onClick, **kwargs):
        super().__init__(master, fg_color="transparent", height=70, cursor="hand2", **kwargs)
        self.pack_propagate(False)
        self.onClick = onClick
        
        self.bind("<Button-1>", lambda e: self.onClick())
        
        # Avatar (Foto de perfil estilo WhatsApp)
        self.avatar_label = customtkinter.CTkLabel(
            self,
            text=avatar,
            font=("Segoe UI", 22),
            width=48,
            height=48,
            fg_color="#202c33",
            corner_radius=24
        )
        self.avatar_label.pack(side="left", padx=12, pady=11)
        self.avatar_label.bind("<Button-1>", lambda e: self.onClick())
        
        # Contenedor de Texto informativo
        self.info_frame = customtkinter.CTkFrame(self, fg_color="transparent")
        self.info_frame.pack(side="left", fill="both", expand=True, pady=11)
        self.info_frame.bind("<Button-1>", lambda e: self.onClick())
        
        self.name_label = customtkinter.CTkLabel(
            self.info_frame,
            text=name,
            font=("Segoe UI", 13, "bold"),
            text_color="#e9edef",
            anchor="w"
        )
        self.name_label.pack(fill="x", anchor="w")
        self.name_label.bind("<Button-1>", lambda e: self.onClick())
        
        self.status_label = customtkinter.CTkLabel(
            self.info_frame,
            text=status,
            font=("Segoe UI", 11),
            text_color="#8696a0",
            anchor="w"
        )
        self.status_label.pack(fill="x", anchor="w")
        self.status_label.bind("<Button-1>", lambda e: self.onClick())
        
    def update_status(self, new_status):
        self.status_label.configure(text=new_status)

class MessageBubble(customtkinter.CTkFrame):
    """Burbuja de mensaje de chat tradicional de WhatsApp."""
    def __init__(self, master, text, is_user=False, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        
        bubble_color = "#005c4b" if is_user else "#202c33"
        align = "right" if is_user else "left"
        padx = (50, 10) if is_user else (10, 50)
        
        self.inner = customtkinter.CTkFrame(
            self, 
            fg_color=bubble_color, 
            corner_radius=10
        )
        self.inner.pack(side=align, padx=padx, pady=4)
        
        self.label = customtkinter.CTkLabel(
            self.inner, 
            text=text, 
            text_color="#e9edef", 
            justify="left",
            wraplength=380,
            font=("Segoe UI", 12)
        )
        self.label.pack(padx=12, pady=(8, 4), anchor="w")
        
        now = time.strftime("%H:%M")
        self.time_label = customtkinter.CTkLabel(
            self.inner,
            text=now,
            text_color="#8696a0",
            font=("Segoe UI", 9)
        )
        self.time_label.pack(padx=12, pady=(0, 4), anchor="e")

class DownloadBubble(customtkinter.CTkFrame):
    """Burbuja especial de chat que contiene el progreso activo de la descarga."""
    def __init__(self, master, title, file_size="Desconocido", **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        
        self.inner = customtkinter.CTkFrame(
            self, 
            fg_color="#202c33", 
            corner_radius=10
        )
        self.inner.pack(side="left", padx=(10, 50), pady=4)
        
        # Fila superior: Logo y Título
        self.header_frame = customtkinter.CTkFrame(self.inner, fg_color="transparent")
        self.header_frame.pack(fill="x", padx=10, pady=(8, 4), anchor="w")
        
        self.icon_label = customtkinter.CTkLabel(
            self.header_frame,
            text="📄",
            font=("Segoe UI", 18),
            width=28
        )
        self.icon_label.pack(side="left", padx=(0, 6))
        
        self.title_label = customtkinter.CTkLabel(
            self.header_frame,
            text=f"Descargando:\n{title}",
            text_color="#e9edef",
            justify="left",
            font=("Segoe UI", 12, "bold"),
            wraplength=320
        )
        self.title_label.pack(side="left", fill="x", expand=True, anchor="w")
        
        # Barra de progreso
        self.progress_bar = customtkinter.CTkProgressBar(
            self.inner,
            width=320,
            progress_color="#00a884",
            fg_color="#2a3942"
        )
        self.progress_bar.pack(padx=12, pady=5, fill="x")
        self.progress_bar.set(0.0)
        
        # Texto de estado actualizable
        self.status_label = customtkinter.CTkLabel(
            self.inner,
            text=f"Conectando... (Tamaño: {file_size})",
            text_color="#8696a0",
            font=("Segoe UI", 10),
            justify="left"
        )
        self.status_label.pack(padx=12, pady=(0, 6), anchor="w")
        
    def update_progress(self, percent_float, status_text):
        self.progress_bar.set(percent_float)
        self.status_label.configure(text=status_text)

# --- VENTANA PRINCIPAL DE LA APLICACIÓN (WHATSAPP UI) ---

class WhatsAppDownloaderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("WhatsApp - Gestor de Descargas")
        self.root.geometry("850x680")
        self.root.minsize(750, 550)
        
        # Cargar ajustes
        self.settings = load_settings()
        
        # Base de datos local temporal de la ejecución
        self.detected_servers = set()
        self.downloading_active = True
        
        # Configuración de columnas (Sidebar = 250px, Chat Area = Expandible)
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_rowconfigure(0, weight=1)
        
        # 1. Crear Barra Lateral (Sidebar)
        self.create_sidebar()
        
        # 2. Crear Contenedor Principal de Vistas
        self.main_container = customtkinter.CTkFrame(self.root, fg_color="transparent")
        self.main_container.grid(row=0, column=1, sticky="nsew")
        self.main_container.grid_rowconfigure(0, weight=1)
        self.main_container.grid_columnconfigure(0, weight=1)
        
        # Crear los 4 frames de vista correspondientes
        self.downloader_frame = self.create_downloader_view(self.main_container)
        self.servers_frame = self.create_servers_view(self.main_container)
        self.config_frame = self.create_config_view(self.main_container)
        self.ayuda_frame = self.create_ayuda_view(self.main_container)
        
        # Posicionar todos en el contenedor principal usando grid overlapping
        self.downloader_frame.grid(row=0, column=0, sticky="nsew")
        self.servers_frame.grid(row=0, column=0, sticky="nsew")
        self.config_frame.grid(row=0, column=0, sticky="nsew")
        self.ayuda_frame.grid(row=0, column=0, sticky="nsew")
        
        # Mostrar vista inicial del descargador
        self.show_view("downloader")
        
        # Mensaje de bienvenida inicial
        self.add_system_message("¡Hola! 👋 Escribe o pega una URL para descargar. No importa el tipo de enlace, te pediré que elijas dónde guardarlo y qué nombre ponerle. Configura tus ajustes en la pestaña lateral de Ajustes.")

    def create_sidebar(self):
        """Crea el panel lateral izquierdo estilo WhatsApp."""
        sidebar = customtkinter.CTkFrame(self.root, fg_color="#111b21", width=250, corner_radius=0)
        sidebar.grid(row=0, column=0, sticky="nsew")
        sidebar.pack_propagate(False)
        
        # Cabecera superior lateral
        hdr = customtkinter.CTkFrame(sidebar, fg_color="#202c33", height=60, corner_radius=0)
        hdr.pack(fill="x")
        
        lbl_avatar = customtkinter.CTkLabel(
            hdr, text="🟢", font=("Segoe UI", 18), width=35
        )
        lbl_avatar.pack(side="left", padx=15, pady=15)
        
        lbl_name = customtkinter.CTkLabel(
            hdr, text="Mi Cuenta", font=("Segoe UI", 12, "bold"), text_color="#e9edef"
        )
        lbl_name.pack(side="left", pady=15)
        
        # Buscador decorativo para asemejar a WhatsApp Web
        search_frame = customtkinter.CTkFrame(sidebar, fg_color="#111b21", height=50, corner_radius=0)
        search_frame.pack(fill="x")
        
        search_entry = customtkinter.CTkEntry(
            search_frame,
            placeholder_text="Busca o empieza un nuevo chat",
            fg_color="#202c33",
            border_width=0,
            corner_radius=8,
            text_color="#e9edef",
            font=("Segoe UI", 11)
        )
        search_entry.pack(fill="x", padx=12, pady=10)
        search_entry.configure(state="disabled")
        
        # Lista de Chats
        self.chat_list_frame = customtkinter.CTkFrame(sidebar, fg_color="transparent")
        self.chat_list_frame.pack(fill="both", expand=True)
        
        self.chat_list_items = {}
        
        # Chat 1: Descargador
        c1 = ChatListItem(
            self.chat_list_frame,
            avatar="📥",
            name="Descargador App",
            status="En línea",
            onClick=lambda: self.show_view("downloader")
        )
        c1.pack(fill="x")
        self.chat_list_items["downloader"] = c1
        
        # Chat 2: Servidores
        c2 = ChatListItem(
            self.chat_list_frame,
            avatar="🖥️",
            name="Servidores YT",
            status="Ver hostnames",
            onClick=lambda: self.show_view("servers")
        )
        c2.pack(fill="x")
        self.chat_list_items["servers"] = c2
        
        # Chat 3: Configuración
        c3 = ChatListItem(
            self.chat_list_frame,
            avatar="⚙️",
            name="Ajustes",
            status="Opciones avanzadas",
            onClick=lambda: self.show_view("config")
        )
        c3.pack(fill="x")
        self.chat_list_items["config"] = c3
        
        # Chat 4: Guía de uso
        c4 = ChatListItem(
            self.chat_list_frame,
            avatar="❓",
            name="Ayuda y Guía",
            status="Manual de uso",
            onClick=lambda: self.show_view("ayuda")
        )
        c4.pack(fill="x")
        self.chat_list_items["ayuda"] = c4

    def create_downloader_view(self, parent):
        """Crea la vista del panel de chat de descargas."""
        frame = customtkinter.CTkFrame(parent, fg_color="transparent")
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_rowconfigure(1, weight=1)
        
        # Cabecera de chat (Header)
        hdr = customtkinter.CTkFrame(frame, fg_color="#202c33", height=60, corner_radius=0)
        hdr.grid(row=0, column=0, sticky="ew")
        
        lbl_av = customtkinter.CTkLabel(hdr, text="📥", font=("Segoe UI", 22), width=45, height=45, fg_color="#111b21", corner_radius=22)
        lbl_av.pack(side="left", padx=12, pady=8)
        
        info_sub = customtkinter.CTkFrame(hdr, fg_color="transparent")
        info_sub.pack(side="left", fill="both", expand=True, pady=8)
        
        lbl_chattitle = customtkinter.CTkLabel(info_sub, text="Descargador App", font=("Segoe UI", 13, "bold"), text_color="#e9edef", anchor="w")
        lbl_chattitle.pack(fill="x", anchor="w")
        
        lbl_chatstatus = customtkinter.CTkLabel(info_sub, text="En línea", font=("Segoe UI", 10), text_color="#00a884", anchor="w")
        lbl_chatstatus.pack(fill="x", anchor="w")
        
        # Panel del chat scrollable
        self.chat_scroll = customtkinter.CTkScrollableFrame(frame, fg_color="#0b141a", corner_radius=0)
        self.chat_scroll.grid(row=1, column=0, sticky="nsew")
        
        # Barra de entrada de texto inferior
        self.input_frame = customtkinter.CTkFrame(frame, fg_color="#202c33", height=60, corner_radius=0)
        self.input_frame.grid(row=2, column=0, sticky="ew")
        
        self.url_entry = customtkinter.CTkEntry(
            self.input_frame, 
            placeholder_text="Escribe o pega una URL para descargar...",
            fg_color="#2a3942",
            border_width=0,
            corner_radius=20,
            text_color="#e9edef",
            font=("Segoe UI", 12)
        )
        self.url_entry.pack(side="left", fill="x", expand=True, padx=(20, 10), pady=12)
        self.url_entry.bind("<Return>", lambda e: self.on_send())
        
        self.send_button = customtkinter.CTkButton(
            self.input_frame,
            text="Descargar",
            width=80,
            height=36,
            corner_radius=18,
            fg_color="#00a884",
            hover_color="#008f72",
            font=("Segoe UI", 11, "bold"),
            command=self.on_send
        )
        self.send_button.pack(side="right", padx=(0, 20), pady=12)
        
        return frame

    def create_servers_view(self, parent):
        """Crea la vista para listar los servidores de Google Video detectados."""
        frame = customtkinter.CTkFrame(parent, fg_color="transparent")
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_rowconfigure(1, weight=1)
        
        hdr = customtkinter.CTkFrame(frame, fg_color="#202c33", height=60, corner_radius=0)
        hdr.grid(row=0, column=0, sticky="ew")
        
        lbl_title = customtkinter.CTkLabel(hdr, text="Servidores Detectados", font=("Segoe UI", 14, "bold"), text_color="#e9edef")
        lbl_title.pack(side="left", padx=20, pady=18)
        
        self.servers_scroll = customtkinter.CTkScrollableFrame(frame, fg_color="#0b141a", corner_radius=0)
        self.servers_scroll.grid(row=1, column=0, sticky="nsew")
        
        return frame

    def create_config_view(self, parent):
        """Crea el panel de configuraciones completas de la app."""
        frame = customtkinter.CTkFrame(parent, fg_color="transparent")
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_rowconfigure(1, weight=1)
        
        hdr = customtkinter.CTkFrame(frame, fg_color="#202c33", height=60, corner_radius=0)
        hdr.grid(row=0, column=0, sticky="ew")
        
        lbl_title = customtkinter.CTkLabel(hdr, text="Ajustes de la Aplicación", font=("Segoe UI", 14, "bold"), text_color="#e9edef")
        lbl_title.pack(side="left", padx=20, pady=18)
        
        scroll = customtkinter.CTkScrollableFrame(frame, fg_color="#0b141a", corner_radius=0)
        scroll.grid(row=1, column=0, sticky="nsew")
        scroll.grid_columnconfigure(0, weight=1)
        
        def add_section(text):
            lbl = customtkinter.CTkLabel(scroll, text=text, font=("Segoe UI", 12, "bold"), text_color="#00a884", anchor="w")
            lbl.pack(fill="x", padx=15, pady=(15, 6))
            
        # --- SECCIÓN 1: GENERALES ---
        add_section("Ajustes de Descarga Generales")
        
        self.switch_ask_path = customtkinter.CTkSwitch(
            scroll, text="Preguntar ubicación antes de descargar (File Explorer)", 
            progress_color="#00a884", text_color="#e9edef", font=("Segoe UI", 11)
        )
        self.switch_ask_path.pack(fill="x", padx=25, pady=5)
        if self.settings.get("always_ask_path", True):
            self.switch_ask_path.select()
            
        dir_frame = customtkinter.CTkFrame(scroll, fg_color="transparent")
        dir_frame.pack(fill="x", padx=25, pady=5)
        
        lbl_dir = customtkinter.CTkLabel(dir_frame, text="Carpeta por defecto / inicial:", text_color="#e9edef", font=("Segoe UI", 11))
        lbl_dir.pack(side="left", padx=(0, 10))
        
        self.entry_dir = customtkinter.CTkEntry(dir_frame, fg_color="#2a3942", border_width=0, text_color="#e9edef", font=("Segoe UI", 11))
        self.entry_dir.pack(side="left", fill="x", expand=True)
        self.entry_dir.insert(0, self.settings.get("default_dir", ""))
        
        btn_browse = customtkinter.CTkButton(
            dir_frame, text="Buscar...", width=60, height=26, fg_color="#2a3942", hover_color="#3a4f5c",
            command=self.on_browse_dir
        )
        btn_browse.pack(side="right", padx=(10, 0))
        
        # --- SECCIÓN 2: YOUTUBE ---
        add_section("Configuraciones de YouTube (yt-dlp)")
        
        qual_frame = customtkinter.CTkFrame(scroll, fg_color="transparent")
        qual_frame.pack(fill="x", padx=25, pady=5)
        
        lbl_qual = customtkinter.CTkLabel(qual_frame, text="Calidad / Formato de descarga:", text_color="#e9edef", font=("Segoe UI", 11))
        lbl_qual.pack(side="left", padx=(0, 10))
        
        self.menu_qual = customtkinter.CTkOptionMenu(
            qual_frame, 
            values=["Calidad Máxima (Best)", "1080p", "720p", "480p", "Solo Audio (MP3)"],
            fg_color="#2a3942", button_color="#202c33", button_hover_color="#3a4f5c", dropdown_fg_color="#2a3942"
        )
        self.menu_qual.pack(side="left")
        self.menu_qual.set(self.settings.get("yt_quality", "Calidad Máxima (Best)"))
        
        self.switch_subs = customtkinter.CTkSwitch(
            scroll, text="Descargar e incrustar subtítulos en el video", 
            progress_color="#00a884", text_color="#e9edef", font=("Segoe UI", 11)
        )
        self.switch_subs.pack(fill="x", padx=25, pady=5)
        if self.settings.get("yt_subs"):
            self.switch_subs.select()
            
        self.switch_thumb = customtkinter.CTkSwitch(
            scroll, text="Incrustar miniatura en el archivo final", 
            progress_color="#00a884", text_color="#e9edef", font=("Segoe UI", 11)
        )
        self.switch_thumb.pack(fill="x", padx=25, pady=5)
        if self.settings.get("yt_thumbnail"):
            self.switch_thumb.select()
            
        self.switch_metadata = customtkinter.CTkSwitch(
            scroll, text="Incrustar metadatos multimedia en el archivo", 
            progress_color="#00a884", text_color="#e9edef", font=("Segoe UI", 11)
        )
        self.switch_metadata.pack(fill="x", padx=25, pady=5)
        if self.settings.get("yt_metadata"):
            self.switch_metadata.select()
            
        args_frame = customtkinter.CTkFrame(scroll, fg_color="transparent")
        args_frame.pack(fill="x", padx=25, pady=5)
        
        lbl_args = customtkinter.CTkLabel(args_frame, text="Argumentos extra de yt-dlp:", text_color="#e9edef", font=("Segoe UI", 11))
        lbl_args.pack(side="left", padx=(0, 10))
        
        self.entry_args = customtkinter.CTkEntry(
            args_frame, fg_color="#2a3942", border_width=0, text_color="#e9edef", font=("Segoe UI", 11),
            placeholder_text="ej: --cookies-from-browser chrome"
        )
        self.entry_args.pack(side="left", fill="x", expand=True)
        self.entry_args.insert(0, self.settings.get("yt_extra_args", ""))
        
        # --- SECCIÓN 3: RED ---
        add_section("Configuraciones de Red (HTTP)")
        
        net_frame = customtkinter.CTkFrame(scroll, fg_color="transparent")
        net_frame.pack(fill="x", padx=25, pady=5)
        
        lbl_timeout = customtkinter.CTkLabel(net_frame, text="Timeout (segundos):", text_color="#e9edef", font=("Segoe UI", 11))
        lbl_timeout.pack(side="left", padx=(0, 10))
        
        self.entry_timeout = customtkinter.CTkEntry(net_frame, width=60, fg_color="#2a3942", border_width=0, text_color="#e9edef", font=("Segoe UI", 11))
        self.entry_timeout.pack(side="left", padx=(0, 20))
        self.entry_timeout.insert(0, str(self.settings.get("http_timeout", 30)))
        
        lbl_retries = customtkinter.CTkLabel(net_frame, text="Reintentos máximos:", text_color="#e9edef", font=("Segoe UI", 11))
        lbl_retries.pack(side="left", padx=(0, 10))
        
        self.entry_retries = customtkinter.CTkEntry(net_frame, width=50, fg_color="#2a3942", border_width=0, text_color="#e9edef", font=("Segoe UI", 11))
        self.entry_retries.pack(side="left")
        self.entry_retries.insert(0, str(self.settings.get("http_retries", 3)))
        
        ua_frame = customtkinter.CTkFrame(scroll, fg_color="transparent")
        ua_frame.pack(fill="x", padx=25, pady=5)
        
        lbl_ua = customtkinter.CTkLabel(ua_frame, text="User-Agent HTTP:", text_color="#e9edef", font=("Segoe UI", 11))
        lbl_ua.pack(side="left", padx=(0, 10))
        
        self.entry_ua = customtkinter.CTkEntry(ua_frame, fg_color="#2a3942", border_width=0, text_color="#e9edef", font=("Segoe UI", 11))
        self.entry_ua.pack(side="left", fill="x", expand=True)
        self.entry_ua.insert(0, self.settings.get("http_user_agent", ""))
        
        # --- SECCIÓN 4: INTERFAZ ---
        add_section("Configuración de Interfaz (GUI)")
        
        gui_frame = customtkinter.CTkFrame(scroll, fg_color="transparent")
        gui_frame.pack(fill="x", padx=25, pady=5)
        
        lbl_theme = customtkinter.CTkLabel(gui_frame, text="Modo visual:", text_color="#e9edef", font=("Segoe UI", 11))
        lbl_theme.pack(side="left", padx=(0, 10))
        
        self.menu_theme = customtkinter.CTkOptionMenu(
            gui_frame, values=["Oscuro (Dark)", "Claro (Light)", "Sistema"], width=100,
            fg_color="#2a3942", button_color="#202c33", button_hover_color="#3a4f5c", dropdown_fg_color="#2a3942"
        )
        self.menu_theme.pack(side="left", padx=(0, 20))
        self.menu_theme.set("Oscuro (Dark)" if self.settings.get("gui_mode") == "dark" else "Claro (Light)" if self.settings.get("gui_mode") == "light" else "Sistema")
        
        lbl_color = customtkinter.CTkLabel(gui_frame, text="Color de énfasis:", text_color="#e9edef", font=("Segoe UI", 11))
        lbl_color.pack(side="left", padx=(0, 10))
        
        self.menu_color = customtkinter.CTkOptionMenu(
            gui_frame, values=["Verde (WhatsApp)", "Azul", "Azul Oscuro"], width=120,
            fg_color="#2a3942", button_color="#202c33", button_hover_color="#3a4f5c", dropdown_fg_color="#2a3942"
        )
        self.menu_color.pack(side="left")
        self.menu_color.set("Verde (WhatsApp)" if self.settings.get("gui_color") == "green" else "Azul" if self.settings.get("gui_color") == "blue" else "Azul Oscuro")
        
        # Botón Guardar
        btn_save = customtkinter.CTkButton(
            scroll, text="Guardar todas las configuraciones", height=40,
            fg_color="#00a884", hover_color="#008f72", font=("Segoe UI", 12, "bold"),
            command=self.on_save_settings
        )
        btn_save.pack(fill="x", padx=25, pady=25)
        
        return frame

    def create_ayuda_view(self, parent):
        """Crea la vista de ayuda estructurada como una conversación de WhatsApp."""
        frame = customtkinter.CTkFrame(parent, fg_color="transparent")
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_rowconfigure(1, weight=1)
        
        hdr = customtkinter.CTkFrame(frame, fg_color="#202c33", height=60, corner_radius=0)
        hdr.grid(row=0, column=0, sticky="ew")
        
        lbl_title = customtkinter.CTkLabel(hdr, text="Guía de Uso & FAQs", font=("Segoe UI", 14, "bold"), text_color="#e9edef")
        lbl_title.pack(side="left", padx=20, pady=18)
        
        scroll = customtkinter.CTkScrollableFrame(frame, fg_color="#0b141a", corner_radius=0)
        scroll.grid(row=1, column=0, sticky="nsew")
        
        faqs = [
            ("¿Cómo funciona el guardado personalizado?", 
             "Siempre que pegues un enlace en el chat y comience la descarga, se abrirá la ventana de Windows Explorer. "
             "Podrás elegir la carpeta exacta y modificar el nombre del archivo final antes de descargar. "
             "Esto funciona tanto para videos de YouTube como para archivos directos."),
            
            ("¿Qué opciones de calidad de YouTube tengo?", 
             "Puedes ir a la pestaña **Ajustes** y seleccionar resoluciones fijas como 1080p, 720p, 480p, o la opción "
             "'Solo Audio (MP3)' si quieres extraer únicamente el sonido del video."),
             
            ("¿Qué significan los servidores detectados?", 
             "Son los servidores físicos de Google (`*.googlevideo.com`) que distribuyen la señal del video en streaming. "
             "Puedes verlos e incluso copiarlos desde el chat de **Servidores YT** para realizar diagnósticos o configuraciones."),
             
            ("¿Cómo edito la interfaz gráfica de la app?", 
             "En la pestaña **Ajustes**, bajo 'Modo visual', puedes activar el modo claro o usar el tema del sistema. "
             "También puedes cambiar el color principal de los botones de la app.")
        ]
        
        for q, a in faqs:
            q_bub = MessageBubble(scroll, q, is_user=True)
            q_bub.pack(fill="x", pady=4)
            a_bub = MessageBubble(scroll, a, is_user=False)
            a_bub.pack(fill="x", pady=4)
            
        return frame

    def show_view(self, name):
        """Intercambia las vistas visibles elevándolas con tkraise."""
        for item_name, item in self.chat_list_items.items():
            if item_name == name:
                item.configure(fg_color="#2a3942")
            else:
                item.configure(fg_color="transparent")
                
        if name == "downloader":
            self.downloader_frame.tkraise()
        elif name == "servers":
            self.servers_frame.tkraise()
            self.refresh_servers_list()
        elif name == "config":
            self.config_frame.tkraise()
        elif name == "ayuda":
            self.ayuda_frame.tkraise()

    def refresh_servers_list(self):
        """Vuelve a renderizar la lista de servidores en la pestaña de Servidores."""
        for w in self.servers_scroll.winfo_children():
            w.destroy()
            
        if not self.detected_servers:
            lbl_empty = customtkinter.CTkLabel(
                self.servers_scroll,
                text="Aún no se han detectado servidores de YouTube.\nIntroduce un enlace de YouTube en la pestaña principal.",
                text_color="#8696a0",
                justify="center",
                font=("Segoe UI", 12)
            )
            lbl_empty.pack(pady=40, fill="x")
            return
            
        for server in sorted(self.detected_servers):
            row = customtkinter.CTkFrame(self.servers_scroll, fg_color="#1c2830", corner_radius=8)
            row.pack(fill="x", pady=4, padx=12)
            
            lbl = customtkinter.CTkLabel(
                row,
                text=server,
                font=("Consolas", 12),
                text_color="#e9edef",
                anchor="w"
            )
            lbl.pack(side="left", padx=15, pady=10, fill="x", expand=True)
            
            btn_copy = customtkinter.CTkButton(
                row,
                text="Copiar",
                width=60,
                height=28,
                fg_color="#00a884",
                hover_color="#008f72",
                corner_radius=6,
                command=lambda s=server: self.copy_to_clipboard(s)
            )
            btn_copy.pack(side="right", padx=15, pady=10)

    def copy_to_clipboard(self, text):
        """Copia una cadena al portapapeles y envía mensaje de confirmación al chat."""
        self.root.clipboard_clear()
        self.root.clipboard_append(text)
        self.add_system_message(f"📋 Servidor copiado al portapapeles:\n`{text}`")

    def add_user_message(self, text):
        """Añade un globo de chat del usuario (verde a la derecha)."""
        bubble = MessageBubble(self.chat_scroll, text, is_user=True)
        bubble.pack(fill="x", pady=4)
        self.scroll_to_bottom()

    def add_system_message(self, text):
        """Añade un globo de chat del sistema (gris a la izquierda)."""
        bubble = MessageBubble(self.chat_scroll, text, is_user=False)
        bubble.pack(fill="x", pady=4)
        self.scroll_to_bottom()
        return bubble

    def add_download_bubble(self, title, file_size="Desconocido"):
        """Añade una tarjeta de descarga con barra de progreso."""
        bubble = DownloadBubble(self.chat_scroll, title, file_size)
        bubble.pack(fill="x", pady=4)
        self.scroll_to_bottom()
        return bubble

    def scroll_to_bottom(self):
        """Desplaza automáticamente el scroll del chat al fondo de forma segura."""
        self.root.update_idletasks()
        try:
            self.chat_scroll._parent_canvas.yview_moveto(1.0)
        except Exception:
            pass

    def on_browse_dir(self):
        """Abre un diálogo de selección de carpeta para definir la ruta por defecto."""
        chosen = filedialog.askdirectory(parent=self.root, initialdir=self.entry_dir.get())
        if chosen:
            self.entry_dir.delete(0, 'end')
            self.entry_dir.insert(0, os.path.abspath(chosen))

    def on_save_settings(self):
        """Manejador para procesar y guardar las opciones de configuración."""
        try:
            self.settings["always_ask_path"] = self.switch_ask_path.get() == 1
            self.settings["default_dir"] = self.entry_dir.get().strip()
            self.settings["yt_quality"] = self.menu_qual.get()
            self.settings["yt_subs"] = self.switch_subs.get() == 1
            self.settings["yt_thumbnail"] = self.switch_thumb.get() == 1
            self.settings["yt_metadata"] = self.switch_metadata.get() == 1
            self.settings["yt_extra_args"] = self.entry_args.get().strip()
            
            try:
                self.settings["http_timeout"] = int(self.entry_timeout.get().strip())
            except ValueError:
                pass
            
            try:
                self.settings["http_retries"] = int(self.entry_retries.get().strip())
            except ValueError:
                pass
                
            self.settings["http_user_agent"] = self.entry_ua.get().strip()
            
            # Cambiar modo visual
            theme_val = self.menu_theme.get()
            self.settings["gui_mode"] = "dark" if "Oscuro" in theme_val else "light" if "Claro" in theme_val else "system"
            customtkinter.set_appearance_mode(self.settings["gui_mode"])
            
            # Cambiar color tema (se aplicará en el próximo reinicio de la ventana)
            color_val = self.menu_color.get()
            self.settings["gui_color"] = "green" if "Verde" in color_val else "blue" if "Azul" in color_val and "Oscuro" not in color_val else "dark-blue"
            
            save_settings(self.settings)
            
            self.add_system_message("⚙️ ¡Ajustes guardados correctamente! El color de énfasis se aplicará por completo en el próximo inicio.")
            self.show_view("downloader")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron guardar las configuraciones: {e}")

    def prompt_save_dialog_threadsafe(self, initial_name, default_ext):
        """Abre de forma thread-safe un cuadro de diálogo 'Guardar como' de Windows Explorer."""
        q = queue.Queue()
        
        def run_on_main():
            initial_dir = self.settings.get("default_dir") or os.path.expanduser("~/Desktop")
            if not os.path.exists(initial_dir):
                initial_dir = os.path.expanduser("~/Desktop")
                
            file_types = [("Todos los archivos", "*.*")]
            if default_ext:
                ext_clean = default_ext.replace(".", "").lower()
                file_types.insert(0, (f"Archivo {ext_clean.upper()}", f"*.{ext_clean}"))
                
            chosen_path = filedialog.asksaveasfilename(
                parent=self.root,
                initialdir=initial_dir,
                initialfile=initial_name,
                defaultextension=default_ext,
                filetypes=file_types,
                title="Guardar archivo como..."
            )
            q.put(chosen_path)
            
        self.root.after(0, run_on_main)
        # Espera que el usuario seleccione la ruta (bloquea el hilo de descarga, no la GUI)
        return q.get()

    def on_send(self):
        """Manejador de envío cuando el usuario pulsa Entrar o el botón Descargar."""
        url_input = self.url_entry.get().strip()
        if not url_input:
            return
            
        self.url_entry.delete(0, 'end')
        self.add_user_message(url_input)
        
        url = validate_url(url_input)
        if not url:
            self.add_system_message("❌ Error: URL no válida. Asegúrate de incluir el protocolo (http:// o https://).")
            return
            
        if is_youtube_url(url):
            self.chat_list_items["downloader"].update_status("Analizando YouTube...")
            process_youtube_url_gui(self, url)
        else:
            self.chat_list_items["downloader"].update_status("Descargando archivo...")
            self.add_system_message("🌐 Enlace genérico detectado. Iniciando análisis de descarga...")
            threading.Thread(target=download_normal_file_gui, args=(self, url), daemon=True).start()

# --- SUBPROCESOS EN SEGUNDO PLANO PARA DESCARGAS (GUI THREAD-SAFE) ---

def process_youtube_url_gui(app, url):
    """Subproceso para analizar y extraer información de un vídeo de YouTube."""
    app.add_system_message("🔍 Analizando enlace de YouTube...")
    
    def run_info():
        try:
            ydl_opts = {
                'quiet': True,
                'no_warnings': True,
            }
            # Cargar User-Agent si está configurado
            ua = app.settings.get("http_user_agent", "").strip()
            if ua:
                ydl_opts['http_headers'] = {'User-Agent': ua}
                
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                
            title = info.get('title', 'video_youtube')
            uploader = info.get('uploader', 'Canal Desconocido')
            duration = info.get('duration')
            
            # Formateo de duración
            duration_str = "Desconocida"
            if duration:
                mins, secs = divmod(duration, 60)
                hours, mins = divmod(mins, 60)
                duration_str = f"{hours:02d}:{mins:02d}:{secs:02d}" if hours > 0 else f"{mins:02d}:{secs:02d}"
                
            metadata_msg = (
                f"🎥 *Detalles del Video:*\n"
                f"• Título: {title}\n"
                f"• Canal: {uploader}\n"
                f"• Duración: {duration_str}"
            )
            
            # Extraer servidores de Google Video
            formats = info.get('formats', [])
            servers = set()
            for fmt in formats:
                fmt_url = fmt.get('url')
                if fmt_url:
                    parsed_url = urllib.parse.urlparse(fmt_url)
                    hostname = parsed_url.hostname
                    if hostname and ('googlevideo.com' in hostname or 'youtube.com' in hostname):
                        servers.add(hostname)
                        
            direct_url = info.get('url')
            if direct_url:
                parsed_url = urllib.parse.urlparse(direct_url)
                if parsed_url.hostname:
                    servers.add(parsed_url.hostname)
                    
            if servers:
                for s in servers:
                    app.detected_servers.add(s)
                server_list = "\n".join([f"• `{s}`" for s in sorted(servers)])
                server_msg = f"🖥️ *Servidores CDN de YouTube detectados:*\n{server_list}"
            else:
                server_msg = "⚠️ No se encontraron servidores de streaming directo (Google Video)."
                
            # Publicar resultados
            app.root.after(0, lambda: app.add_system_message(f"{metadata_msg}\n\n{server_msg}"))
            
            # Preguntar al usuario dónde guardar la descarga (File Explorer) si está habilitado
            title_clean = re.sub(r'[\\/*?:"<>|]', "", title)
            
            # Formatear extensión por defecto según calidad elegida
            qual = app.settings.get("yt_quality", "Calidad Máxima (Best)")
            default_ext = ".mp3" if qual == "Solo Audio (MP3)" else "." + (info.get('ext') or "mp4")
            
            chosen_path = None
            if app.settings.get("always_ask_path", True):
                chosen_path = app.prompt_save_dialog_threadsafe(title_clean, default_ext)
                if not chosen_path:
                    app.root.after(0, lambda: app.add_system_message("🛑 Descarga de YouTube cancelada al seleccionar ruta."))
                    app.root.after(0, lambda: app.chat_list_items["downloader"].update_status("En línea"))
                    return
            else:
                # Usar carpeta por defecto
                ddir = app.settings.get("default_dir") or os.path.expanduser("~/Desktop")
                chosen_path = os.path.join(ddir, title_clean + default_ext)
                
            # Iniciar descarga asíncrona pasándole la ruta final seleccionada
            def start_dl(path):
                bubble = app.add_download_bubble(title_clean, "Obteniendo...")
                threading.Thread(target=download_youtube_gui, args=(app, url, bubble, path), daemon=True).start()
                
            app.root.after(0, lambda: start_dl(chosen_path))
            
        except Exception as e:
            app.root.after(0, lambda: app.add_system_message(f"❌ Error al analizar enlace de YouTube: {e}"))
            app.root.after(0, lambda: app.chat_list_items["downloader"].update_status("En línea"))
            
    threading.Thread(target=run_info, daemon=True).start()

def make_yt_progress_hook(app, bubble):
    """Crea un gancho de progreso de yt-dlp que actualiza la interfaz de usuario en el hilo principal."""
    def progress_hook(d):
        if d['status'] == 'downloading':
            total = d.get('total_bytes') or d.get('total_bytes_estimate') or 0
            downloaded = d.get('downloaded_bytes', 0)
            percent_str = d.get('_percent_str', '0%').replace('%', '').strip()
            
            try:
                percent = float(percent_str) / 100.0
            except ValueError:
                percent = 0.0
                
            speed = d.get('_speed_str', 'Desconocido').strip()
            eta = d.get('_eta_str', 'Desconocido').strip()
            
            size_mb = total / (1024*1024) if total else 0
            dl_mb = downloaded / (1024*1024)
            
            status_text = f"{dl_mb:.1f} / {size_mb:.1f} MB | {speed} | ETA: {eta}" if size_mb else f"{dl_mb:.1f} MB | {speed}"
            app.root.after(0, lambda p=percent, s=status_text: bubble.update_progress(p, s))
            
        elif d['status'] == 'finished':
            app.root.after(0, lambda: bubble.update_progress(1.0, "Procesamiento finalizado. Guardando..."))
    return progress_hook

def download_youtube_gui(app, url, bubble, path):
    """Subproceso para descargar el vídeo de YouTube utilizando la configuración guardada."""
    try:
        # Configuración dinámica del formato
        qual = app.settings.get("yt_quality", "Calidad Máxima (Best)")
        fmt = 'bestvideo+bestaudio/best'
        if qual == "1080p":
            fmt = 'bestvideo[height<=1080]+bestaudio/best'
        elif qual == "720p":
            fmt = 'bestvideo[height<=720]+bestaudio/best'
        elif qual == "480p":
            fmt = 'bestvideo[height<=480]+bestaudio/best'
        elif qual == "Solo Audio (MP3)":
            fmt = 'bestaudio/best'
            
        ydl_opts = {
            'outtmpl': path,
            'format': fmt,
            'progress_hooks': [make_yt_progress_hook(app, bubble)],
            'quiet': True,
            'no_warnings': True,
            'postprocessors': []
        }
        
        # User-Agent
        ua = app.settings.get("http_user_agent", "").strip()
        if ua:
            ydl_opts['http_headers'] = {'User-Agent': ua}
            
        # Post-procesamiento opcional
        if qual == "Solo Audio (MP3)":
            ydl_opts['postprocessors'].append({
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            })
            
        if app.settings.get("yt_subs"):
            ydl_opts['writesubtitles'] = True
            ydl_opts['allsubtitles'] = True
            ydl_opts['embedsubtitles'] = True
            
        if app.settings.get("yt_thumbnail"):
            ydl_opts['writethumbnail'] = True
            ydl_opts['postprocessors'].append({
                'key': 'EmbedThumbnail',
                'already_have_thumbnail': False,
            })
            
        if app.settings.get("yt_metadata"):
            ydl_opts['postprocessors'].append({
                'key': 'Metadata',
                'add_metadata': True,
            })
            
        # Argumentos extra de la configuración
        extra_args = app.settings.get("yt_extra_args", "").strip()
        if extra_args:
            # Dividir los argumentos simples por espacios
            import shlex
            parsed_args = shlex.split(extra_args)
            # PyInstaller/yt-dlp permite parsear argumentos en ydl_opts a nivel CLI
            # Para evitar inyecciones críticas, se limita a las opciones estándar de yt-dlp.
            
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
            
        app.root.after(0, lambda: app.add_system_message(f"✅ ¡Descarga de YouTube completada!\nGuardado como: {os.path.abspath(path)}"))
    except Exception as e:
        app.root.after(0, lambda: app.add_system_message(f"❌ Error al descargar de YouTube: {e}"))
    finally:
        app.root.after(0, lambda: app.chat_list_items["downloader"].update_status("En línea"))

def download_normal_file_gui(app, url, bubble=None):
    """Subproceso para descargar una URL genérica abriendo previamente el diálogo de guardar."""
    try:
        timeout = app.settings.get("http_timeout", 30)
        retries = app.settings.get("http_retries", 3)
        user_agent = app.settings.get("http_user_agent", "")
        
        headers = {}
        if user_agent:
            headers['User-Agent'] = user_agent
            
        # Intentar descargar con reintentos
        session = requests.Session()
        adapter = requests.adapters.HTTPAdapter(max_retries=retries)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        
        response = session.get(url, stream=True, headers=headers, timeout=timeout)
        response.raise_for_status()
        
        final_url = response.url
        filename = None
        cd = response.headers.get('content-disposition')
        if cd:
            fname = re.findall("filename\\*?=(?:utf-8'')?([^;]+)", cd)
            if fname:
                filename = urllib.parse.unquote(fname[0].strip('\'"'))
            else:
                fname = re.findall('filename="?([^";]+)"?', cd)
                if fname:
                    filename = fname[0]
                    
        if not filename:
            parsed_url = urllib.parse.urlparse(final_url)
            filename = os.path.basename(parsed_url.path)
            if not filename:
                filename = "archivo_descargado"
                
        # Deducción de extensión si falta
        name_only, ext = os.path.splitext(filename)
        if not ext:
            content_type = response.headers.get('content-type')
            if content_type:
                mime = content_type.split(';')[0].strip()
                guessed_ext = mimetypes.guess_extension(mime)
                if guessed_ext:
                    ext = guessed_ext
                    filename += ext
                    
        # Sanitizar para Windows
        filename_clean = re.sub(r'[\\/*?:"<>|]', "", name_only)
        if not filename_clean:
            filename_clean = "archivo_descargado"
            
        # Abrir diálogo para guardar archivo en el hilo principal
        chosen_path = None
        if app.settings.get("always_ask_path", True):
            chosen_path = app.prompt_save_dialog_threadsafe(filename_clean, ext)
            if not chosen_path:
                response.close()
                app.root.after(0, lambda: app.add_system_message("🛑 Descarga cancelada al seleccionar la ruta de guardado."))
                app.root.after(0, lambda: app.chat_list_items["downloader"].update_status("En línea"))
                return
        else:
            ddir = app.settings.get("default_dir") or os.path.expanduser("~/Desktop")
            chosen_path = os.path.join(ddir, filename_clean + ext)
            
        # Inicializar burbuja de progreso
        total_size = int(response.headers.get('content-length', 0))
        bubble = app.add_download_bubble(os.path.basename(chosen_path), "Iniciando...")
        
        def init_bubble():
            sz = f"{total_size / (1024*1024):.2f} MB" if total_size else "Desconocido"
            bubble.title_label.configure(text=f"Descargando:\n{os.path.basename(chosen_path)}")
            bubble.status_label.configure(text=f"Iniciando... (Tamaño: {sz})")
        app.root.after(0, init_bubble)
        
        start_time = time.time()
        downloaded = 0
        
        with open(chosen_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=1024*64):
                if not app.downloading_active:
                    break
                if chunk:
                    f.write(chunk)
                    downloaded += len(chunk)
                    if total_size:
                        percent = downloaded / total_size
                        elapsed = time.time() - start_time
                        speed = downloaded / elapsed / 1024 if elapsed > 0 else 0
                        speed_str = f"{speed/1024:.2f} MB/s" if speed > 1024 else f"{speed:.1f} KB/s"
                        status_text = f"{downloaded/(1024*1024):.1f} / {total_size/(1024*1024):.1f} MB | {speed_str}"
                        app.root.after(0, lambda p=percent, s=status_text: bubble.update_progress(p, s))
                    else:
                        status_text = f"Descargado: {downloaded/(1024*1024):.2f} MB"
                        app.root.after(0, lambda s=status_text: bubble.update_progress(0.0, s))
                        
        if app.downloading_active:
            app.root.after(0, lambda: app.add_system_message(f"✅ ¡Descarga completada!\nGuardado como: {os.path.abspath(chosen_path)}"))
            
    except Exception as e:
        app.root.after(0, lambda: app.add_system_message(f"❌ Error al descargar con requests: {e}"))
    finally:
        app.root.after(0, lambda: app.chat_list_items["downloader"].update_status("En línea"))

# --- MODO DE LÍNEA DE COMANDOS (FALLBACK CLI) ---

def run_cli_mode(url_input):
    """Lanza la aplicación en modo línea de comandos (sin abrir File Dialogs)."""
    print("==================================================")
    print("      GESTOR DE DESCARGAS (CLI)                  ")
    print("==================================================")
    
    url = validate_url(url_input)
    if not url:
        print("[-] Error: URL no válida. Asegúrate de incluir el protocolo.")
        sys.exit(1)
        
    print(f"\n[*] Analizando destino...")
    
    if is_youtube_url(url):
        print("[*] Destino: URL de YouTube.")
        # Simulación de extracción simple en CLI
        ydl_opts = {'quiet': True, 'no_warnings': True}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            try:
                info = ydl.extract_info(url, download=False)
                title = info.get('title', 'video_youtube')
                title_clean = re.sub(r'[\\/*?:"<>|]', "", title)
                path = os.path.join(".", title_clean + "." + (info.get('ext') or "mp4"))
                print(f"[+] Título: {title}")
                print(f"[+] Servidor sugerido: {info.get('url')}")
                print(f"[*] Descargando en la ruta local: {path}")
                ydl_opts['outtmpl'] = path
                ydl_opts['quiet'] = False  # Mostrar barra nativa en CLI
                with yt_dlp.YoutubeDL(ydl_opts) as ydl_down:
                    ydl_down.download([url])
                print("[+] ¡Descarga de YouTube completada!")
            except Exception as e:
                print(f"[-] Error: {e}")
    else:
        print("[*] Destino: URL genérica.")
        try:
            response = requests.get(url, stream=True, timeout=30)
            response.raise_for_status()
            parsed_url = urllib.parse.urlparse(response.url)
            filename = os.path.basename(parsed_url.path) or "archivo_descargado"
            filename = re.sub(r'[\\/*?:"<>|]', "", filename)
            
            print(f"[*] Descargando como: {filename}")
            with open(filename, 'wb') as f:
                for chunk in response.iter_content(chunk_size=1024*64):
                    if chunk:
                        f.write(chunk)
            print(f"[+] ¡Descarga completada! Guardado en local como: {filename}")
        except Exception as e:
            print(f"[-] Error al descargar por CLI: {e}")

# --- PUNTOS DE ENTRADA (MAIN RUNNERS) ---

def run_gui_mode():
    """Lanza la aplicación en modo ventana gráfica."""
    root = customtkinter.CTk()
    app = WhatsAppDownloaderApp(root)
    
    # Intentar cargar el logo del escritorio como icono de la aplicación
    try:
        from PIL import Image, ImageTk
        desktop_logo_path = os.path.expanduser("~/Desktop/logo.jpg")
        if os.path.exists(desktop_logo_path):
            pil_img = Image.open(desktop_logo_path)
            pil_img_resized = pil_img.resize((64, 64), Image.Resampling.LANCZOS)
            icon_img = ImageTk.PhotoImage(pil_img_resized)
            root.iconphoto(True, icon_img)
            root._icon_image_ref = icon_img
    except Exception:
        pass
        
    # Manejar cierre de la ventana de forma limpia cancelando descargas activas
    def on_closing():
        app.downloading_active = False
        root.destroy()
        
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()

def main():
    if len(sys.argv) > 1:
        run_cli_mode(sys.argv[1])
    else:
        run_gui_mode()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n[-] Operación cancelada por el usuario.")
        sys.exit(0)
