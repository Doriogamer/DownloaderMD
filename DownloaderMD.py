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
            values=["Calidad Máxima (Best)", "1080p", "720p", "
