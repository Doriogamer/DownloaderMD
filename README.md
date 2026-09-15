# 📥 DownloaderMD

**Descargador universal para YouTube, MP3 y links directos**  
Interfaz grafica moderna. Funciona en Windows 10+. Rapido, facil y sin complicaciones.

![Python](https://img.shields.io/badge/Python-3.8+-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Version](https://img.shields.io/badge/Version-1.4.0-brightgreen)
![Status](https://img.shields.io/badge/Status-Active-success)

---

## ✨ Caracteristicas

- **📺 YouTube y mas**: YouTube, TikTok, Instagram, X/Twitter, Facebook, Vimeo, Twitch, SoundCloud, Reddit, Dailymotion, Bilibili, Pinterest, Bandcamp, Mixcloud, Kick, Rumble y otros sitios compatibles con yt-dlp
- **📃 Playlists**: Descarga listas de reproduccion (se puede desactivar en Ajustes / `--no-playlist`)
- **🎵 MP3**: Extrae solo el audio con un click (requiere ffmpeg)
- **🌐 Enlaces directos**: Descarga cualquier archivo desde un link directo
- **🎨 Interfaz moderna**: GUI estilo chat, intuitiva
- **💻 Multiplataforma**: Windows, Linux y macOS (configuracion en la carpeta de datos del sistema)
- **📜 Historial**: Ultimas descargas en `history.json`
- **🍪 Cookies del navegador**: `--cookies-from-browser chrome` (u otro) para videos que piden sesion

---

## 📥 Instalacion

### Opcion 1: Descargar el instalador (Recomendado)

1. Ve a la seccion **[Releases](https://github.com/Doriogamer/DownloaderMD/releases)**
2. Descarga `installer.exe` (version mas reciente)
3. Ejecuta el instalador

### Opcion 2: Instalacion manual (Para desarrolladores)

**Requisitos previos:**
- Python 3.8 o superior
- pip
- ffmpeg en el PATH (para MP3 y para unir video+audio)

```bash
git clone https://github.com/Doriogamer/DownloaderMD.git
cd DownloaderMD
pip install -r requirements.txt
python main.py
```

---

## 🛠️ Requisitos del Sistema

| Requisito | Minimo | Recomendado |
|-----------|--------|------------|
| **OS** | Windows 10 / Linux / macOS | Windows 10/11 |
| **Python** | 3.8 | 3.10+ |
| **RAM** | 512 MB | 2 GB |
| **Espacio** | 100 MB | 500 MB |
| **Internet** | Requerida | Requerida |

---

## 🚀 Como Usar

### Interfaz grafica

1. Abre la aplicacion (`python main.py`)
2. Pega un link en la barra de entrada
3. Selecciona el formato en Ajustes (video o MP3)
4. Elige la carpeta de destino (opcional)
5. Pulsa **DESCARGAR**

### Linea de comandos

```bash
python main.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ" --format video --quality 720
python main.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ" --format mp3 -o ./Descargas
python main.py "URL" --no-playlist
python main.py "URL" --cookies-from-browser chrome
```

Calidades: `360`, `480`, `720`, `1080`, `1440`, `2160`.

---

## 📦 Dependencias

```
yt-dlp>=2025.1.0
requests>=2.31.0
customtkinter>=5.2.0
Pillow>=10.0.0
```

---

## 🐛 Solucionar Problemas

### "No se puede conectar a YouTube"
- Verifica tu conexion
- Actualiza yt-dlp: `pip install --upgrade yt-dlp`
- Si el video pide login o edad: `--cookies-from-browser chrome`

### El programa no abre
- `pip install --upgrade -r requirements.txt`
- Python 3.8+
- Abre un [Issue](https://github.com/Doriogamer/DownloaderMD/issues)

---

## 📜 Licencia

MIT. Autor: **Doriogamer** — [GitHub](https://github.com/Doriogamer)

Contacto: dalvarezwallace2@gmail.com
