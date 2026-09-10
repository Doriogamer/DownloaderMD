# 📋 Changelog

Todos los cambios notables en este proyecto serán documentados en este archivo.

## [1.1.0] - 2026-09-10

### ✨ Agregado
- `main.py` como punto de entrada documentado (`python main.py`)
- Detección de URLs de YouTube Music y `m.youtube.com`
- Versión de app `1.1.0` en el código

### 🔧 Mejorado
- Ajustes persistentes en una ruta portable:
  - Windows: `%LOCALAPPDATA%\\DownloaderMD`
  - macOS: `~/Library/Application Support/DownloaderMD`
  - Linux: `~/.config/DownloaderMD`
- Carpeta de descarga por defecto: Escritorio, o Descargas si no existe
- Dependencias actualizadas: `yt-dlp`, `requests`, `customtkinter`, `Pillow`
- `setup.py`: script de consola `downloadermd` apunta a `downloader:main`

### 📝 Notas
- Sigue siendo necesario `ffmpeg` en el PATH para extraer MP3 de forma fiable

## [1.0] - 2026-07-12

### ✨ Agregado
- Descarga de videos de YouTube en múltiples resoluciones (360p, 480p, 720p, 1080p)
- Extracción de audio MP3 desde YouTube
- Descarga de archivos desde enlaces directos usando Requests
- Interfaz gráfica moderna estilo WhatsApp
- Soporte para Windows 10 y superior
- Validación de URLs
- Manejo de errores robusto

### 🔧 Técnico
- Motor: `yt-dlp` para descargas de YouTube
- Requests para descargas HTTP
- Interfaz gráfica con customtkinter
- Código limpio y documentado

### 📝 Notas
- Versión inicial del proyecto
