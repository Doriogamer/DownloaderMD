# 📥 DownloaderMD

**Descargador universal para YouTube, MP3 y links directos**  
Interfaz grafica moderna. Funciona en Windows 10+. Rapido, facil y sin complicaciones.

![Python](https://img.shields.io/badge/Python-3.8+-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Version](https://img.shields.io/badge/Version-1.13.0-brightgreen)
![Status](https://img.shields.io/badge/Status-Active-success)

---

## ✨ Caracteristicas

- **📺 YouTube y mas**: YouTube, TikTok, Instagram, Threads, X/Twitter, Facebook, Vimeo, Twitch, SoundCloud, Reddit, Dailymotion, Bilibili, Pinterest, Bandcamp, Mixcloud, Kick, Rumble, Bluesky, Flickr, TED, Streamable, Imgur, LinkedIn, VK, Odysee, Newgrounds, Archive.org, NicoNico, Tumblr, BitChute, PeerTube, Mastodon, Gab, LBRY, Weibo, Youku, Loom, Snapchat, Douyin, Ixigua, Rutube, OK.ru, Dzen, Coub, Patreon, Substack, Apple Podcasts, Nebula, Floatplane, Aparat, Audiomack, HearThis, Podbean, CapCut, Likee, Weverse, CHZZK, SOOP, Trovo, AfreecaTV, Naver TV, media.ccc.de, CuriosityStream, Dropout, ESPN, BBC, CNN, NPR, Spotify, Deezer, Tidal, Apple Music, BandLab, Pixiv, Crunchyroll, Xiaohongshu, AbemaTV, ARTE, JioSaavn, Vocaroo, OPENREC, SHOWROOM, 17LIVE, AcFun, Google Drive, Dropbox, Al Jazeera y otros sitios compatibles con yt-dlp
- **📃 Playlists**: Descarga listas de reproduccion (`--no-playlist`, `--yes-playlist`, `--playlist-items`, `--max-downloads`)
- **🎵 Audio**: Extrae audio en mp3, m4a, opus, wav o flac (requiere ffmpeg). Opcional: `--embed-thumbnail`
- **🌐 Enlaces directos**: Descarga cualquier archivo desde un link directo (usa el nombre de `Content-Disposition` si existe). Reanuda si el archivo ya existe a medias
- **🎨 Interfaz moderna**: GUI estilo chat, intuitiva
- **💻 Multiplataforma**: Windows, Linux y macOS (configuracion en la carpeta de datos del sistema)
- **📜 Historial**: Ultimas descargas en `history.json`
- **🍪 Cookies**: `--cookies-from-browser chrome` o `--cookies cookies.txt`
- **🔒 Proxy**: `--proxy http://127.0.0.1:8080`
- **⛔ SponsorBlock**: `--sponsorblock` quita anuncios embebidos en YouTube
- **📋 Archivo de descargas**: `--download-archive ids.txt` evita repetir videos
- **🌍 Geo-bypass**: `--geo-bypass` intenta saltar bloqueos de region
- **🎬 Contenedor**: `--merge-format mp4|mkv|webm` y `--embed-subs`
- **🚪 Windows names**: `--windows-filenames` y `--no-overwrites`
- **📡 Red**: `--force-ipv4`, `--socket-timeout`, `--concurrent-fragments`
- **🎧 Keep video**: `--keep-video` conserva el original al extraer audio
- **🔓 Playlists robustas**: `--ignore-errors` y `--write-description`
- **💬 Comentarios y lives**: `--write-comments`, `--break-on-existing`, `--live-from-start`
- **🔓 Codigo abierto**: el motor GUI vive en `engine.py`

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
- ffmpeg en el PATH (para audio y para unir video+audio)

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
python main.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ" --format mp3 --audio-quality 320 -o ./Descargas
python main.py "URL" --format audio --audio-format m4a
python main.py "URL" --no-playlist
python main.py "URL" --yes-playlist
python main.py "URL" --cookies-from-browser chrome
python main.py "URL" --cookies cookies.txt
python main.py "URL" --subs --thumbnail
python main.py "URL" --format mp3 --embed-thumbnail
python main.py "URL" --embed-subs --merge-format mkv
python main.py "URL" --proxy http://127.0.0.1:8080
python main.py "URL" --restrict-filenames
python main.py "URL" --sponsorblock
python main.py "URL" --download-archive ids.txt
python main.py "URL" --write-info-json
python main.py "URL" --max-downloads 5 --playlist-items 1-3,8
python main.py "URL" --sleep-interval 2
python main.py "URL" --retries 20 --geo-bypass --no-mtime
python main.py "URL" --windows-filenames --no-overwrites
python main.py "URL" --format mp3 --keep-video
python main.py "URL" --force-ipv4 --socket-timeout 30
python main.py "URL" --concurrent-fragments 16
python main.py "URL" --ignore-errors --write-description
python main.py "URL" --write-comments --break-on-existing
python main.py "URL" --live-from-start
python main.py "URL" --list-formats
python main.py --version
```

Calidades de video: `360`, `480`, `720`, `1080`, `1440`, `2160`.  
Calidades de audio MP3: `128`, `192`, `256`, `320`.  
Formatos de audio: `mp3`, `m4a`, `opus`, `wav`, `flac`.  
Contenedores: `mp4`, `mkv`, `webm`.

---

## 📦 Dependencias

```
yt-dlp>=2026.8.19
requests>=2.31.0
customtkinter>=5.2.0
Pillow>=10.0.0
```

---

## 🐛 Solucionar Problemas

### "No se puede conectar a YouTube"
- Verifica tu conexion
- Actualiza yt-dlp: `pip install --upgrade yt-dlp`
- Si el video pide login o edad: `--cookies-from-browser chrome` o `--cookies cookies.txt`
- Si tu red bloquea el sitio: `--proxy http://127.0.0.1:8080`
- Si hay bloqueo de region: `--geo-bypass`

### El programa no abre
- `pip install --upgrade -r requirements.txt`
- Python 3.8+
- Abre un [Issue](https://github.com/Doriogamer/DownloaderMD/issues)

---

## 📜 Licencia

MIT. Autor: **Doriogamer** — [GitHub](https://github.com/Doriogamer)

Contacto: dalvarezwallace2@gmail.com
