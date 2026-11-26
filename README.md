# 📥 DownloaderMD

**Descargador universal para YouTube, MP3 y links directos**  
Interfaz grafica moderna. Funciona en Windows 10+. Rapido, facil y sin complicaciones.

![Python](https://img.shields.io/badge/Python-3.11+-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Version](https://img.shields.io/badge/Version-1.64.0-brightgreen)
![Status](https://img.shields.io/badge/Status-Active-success)

---

## ✨ Caracteristicas

- **📺 YouTube y mas**: YouTube, TikTok, Instagram, Threads, X/Twitter, Facebook, Vimeo, Twitch, SoundCloud, Reddit, Dailymotion, Bilibili y muchos más sitios compatibles con yt-dlp
- **📑 Playlists**: Descarga listas de reproduccion
- **🎵 Audio**: Extrae audio en mp3, m4a, opus, wav o flac (requiere ffmpeg)
- **🌐 Enlaces directos**: Descarga cualquier archivo desde un link directo. Reanuda si el archivo ya existe a medias
- **🎨 Interfaz moderna**: GUI estilo chat, intuitiva con CustomTkinter
- **💻 Multiplataforma**: Windows, Linux y macOS
- **📜 Historial**: Ultimas descargas en history.json
- **🍪 Cookies**: soporte para cookies
- **🔒 Proxy**: soporte para proxy
- **🔓 Codigo abierto**: el motor GUI vive en `engine.py`

---

## 📥 Instalacion

### Opcion 1: Descargar el instalador (Recomendado)

1. Ve a la seccion **[Releases](https://github.com/Doriogamer/DownloaderMD/releases)**
2. Descarga `installer.exe` (version mas reciente)
3. Ejecuta el instalador

### Opcion 2: Instalacion manual (Para desarrolladores)

**Requisitos previos:**
- Python 3.11 o superior
- pip
- ffmpeg en el PATH (para audio)

```bash
git clone https://github.com/Doriogamer/DownloaderMD.git
cd DownloaderMD
pip install -r requirements.txt
python main.py
```

---

## 🚀 Como Usar

### Interfaz grafica

1. Abre la aplicacion (`python main.py`)
2. Pega un link en la barra de entrada
3. Selecciona el formato (video o Audio)
4. Elige la carpeta de destino
5. Pulsa **DESCARGAR**

### Linea de comandos

```bash
python main.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ" --format video --quality 720
python main.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ" --format mp3 -o ./Descargas
```

---

## 📦 Dependencias

```
yt-dlp>=2026.11.23
requests>=2.32.0
customtkinter>=6.0.0
Pillow>=13.0.0
```

---

## 📜 Licencia

MIT. Autor: **Doriogamer** — [GitHub](https://github.com/Doriogamer)

Contacto: dalvarezwallace2@gmail.com
