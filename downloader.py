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

def _app_data_dir():
    """Directorio de configuración persistente, portable entre Windows, Linux y macOS."""
    if sys.platform.startswith("win"):
        base = os.environ.get("LOCALAPPDATA") or os.path.join(
            os.environ.get("USERPROFILE", os.path.expanduser("~")), "AppData", "Local"
        )
        return os.path.join(base, "DownloaderMD")
    if sys.platform == "darwin":
        return os.path.join(os.path.expanduser("~"), "Library", "Application Support", "DownloaderMD")
    xdg = os.environ.get("XDG_CONFIG_HOME", os.path.join(os.path.expanduser("~"), ".config"))
    return os.path.join(xdg, "DownloaderMD")


def _default_download_dir():
    desktop = os.path.join(os.path.expanduser("~"), "Desktop")
    if os.path.isdir(desktop):
        return desktop
    downloads = os.path.join(os.path.expanduser("~"), "Downloads")
    if os.path.isdir(downloads):
        return downloads
    return os.path.expanduser("~")


SETTINGS_DIR = _app_data_dir()
SETTINGS_FILE = os.path.join(SETTINGS_DIR, "settings.json")
APP_VERSION = "1.1.0"

def load_settings():
    """Carga los ajustes persistentes desde un archivo JSON, con valores por defecto."""
    default_settings = {
        "always_ask_path": True,
        "default_dir": _default_download_dir(),
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
        return any(pattern in domain for pattern in [
            'youtube.com', 'youtu.be', 'youtube-nocookie.com', 'music.youtube.com', 'm.youtube.com'
        ])
    except Exception:
        return False
