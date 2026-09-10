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
