# 📥 DownloaderMD

**Descargador universal para YouTube, MP3 y links directos**  
Interfaz grafica moderna. Funciona en Windows 10+. Rapido, facil y sin complicaciones.

![Python](https://img.shields.io/badge/Python-3.8+-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Version](https://img.shields.io/badge/Version-1.21.0-brightgreen)
![Status](https://img.shields.io/badge/Status-Active-success)

---

## ✨ Caracteristicas

- **📺 YouTube y mas**: YouTube, TikTok, Instagram, Threads, X/Twitter, Facebook, Vimeo, Twitch, SoundCloud, Reddit, Dailymotion, Bilibili, Pinterest, Bandcamp, Mixcloud, Kick, Rumble, Bluesky, Flickr, TED, Streamable, Imgur, LinkedIn, VK, Odysee, Newgrounds, Archive.org, NicoNico, Tumblr, BitChute, PeerTube, Mastodon, Gab, LBRY, Weibo, Youku, Loom, Snapchat, Douyin, Ixigua, Rutube, OK.ru, Dzen, Coub, Patreon, Substack, Apple Podcasts, Nebula, Floatplane, Aparat, Audiomack, HearThis, Podbean, CapCut, Likee, Weverse, CHZZK, SOOP, Trovo, AfreecaTV, Naver TV, media.ccc.de, CuriosityStream, Dropout, ESPN, BBC, CNN, NPR, Spotify, Deezer, Tidal, Apple Music, BandLab, Pixiv, Crunchyroll, Xiaohongshu, AbemaTV, ARTE, JioSaavn, Vocaroo, OPENREC, SHOWROOM, 17LIVE, AcFun, Google Drive, Dropbox, Al Jazeera, Mega, MediaFire, OneDrive, Box, DeviantArt, ArtStation, Last.fm, iVoox, YouTube Kids, Amazon Music, Misskey, Kwai, StreamYard, Soundgasm, WeTransfer, Giphy, Tenor, PBS, NBC, Reuters, NHK, Yandex Music, Anghami, Radio Javan, Discord, Streamja, Anchor, Castbox, Pocket Casts, Scribd, SlideShare, PeerTube.fr, Google Podcasts, Transistor, Buzzsprout, Libsyn, Simplecast, Overcast, Medal.tv, Hotstar, Viki, iQiyi, WeTV, SonyLIV, ZEE5, Audius, Gaana, Hungama, MX Player, Boomplay, Resso, Piped, Rokfin, Brighteon, Kuaishou, Tencent Video, HIDIVE, Jamendo, TwitCasting, FC2, RTVE, DW, France 24, SVT, NRK, CBC, RaiPlay, NetEase Cloud Music, Steam, IGN, GameSpot, Coursera, Udemy, edX, Khan Academy, The Verge, Polygon, Vox, Bloomberg, WSJ, FT, NYT, Washington Post, Pocket Casts, Scribd, SlideShare, ABC, CBS, Sky News, Euronews, The Guardian, Le Monde, Der Spiegel, NPO, Stream.cz, Wistia, Gofile, Pixeldrain, Telegram, Baidu Pan, Wikimedia Commons, IMDb, Fox News, MSNBC, AP News, The Economist, El Pais, El Mundo, Globo, ZDF, ARD Mediathek, France TV, ITV, Channel 4, DR, Yle, Atresplayer, TVer, DLive, Audioboom, Spreaker, Acast, Megaphone, Omny, Pandora, Qobuz, Freesound, Google Photos, Yandex Disk, Mail.ru Cloud, Xbox, RedGIFs y otros sitios compatibles con yt-dlp
- **📃 Playlists**: Descarga listas de reproduccion (`--no-playlist`, `--yes-playlist`, `--playlist-items`, `--max-downloads`, `--flat-playlist`)
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
- **📡 Red**: `--force-ipv4`, `--force-ipv6`, `--socket-timeout`, `--concurrent-fragments`, `--rate-limit`, `--sleep-requests`
- **🎧 Keep video**: `--keep-video` conserva el original al extraer audio
- **🔓 Playlists robustas**: `--ignore-errors`, `--write-description`, `--match-filter`, `--min-filesize`, `--max-filesize`
- **💬 Comentarios y lives**: `--write-comments`, `--break-on-existing`, `--live-from-start`
- **🧳 Extra CLI**: `--add-metadata`, `--embed-chapters`, `--no-part`, `--prefer-free-formats`, `--quiet`, `--verbose`, `--convert-subs`, `--sub-langs`, `--extractor-retries`
- **📅 Filtros**: `--dateafter`, `--datebefore`, `--match-title`, `--reject-title`, `--trim-filenames`, `--lazy-playlist`, `--impersonate`
- **📁 Salida**: `--output-template`, `--by-uploader` y `--ffmpeg-location`
- **🧭 Red y recortes**: `--referer`, `--user-agent`, `--extractor-args`, `--playlist-reverse`, `--download-sections`, `--newline`, `--write-link`
- **🛡️ TLS y playlists**: `--no-check-certificates`, `--age-limit`, `--playlist-start`, `--playlist-end`, `--skip-unavailable-fragments`, `--no-warnings`
- **🎲 Cola y metadata**: `--mark-watched`, `--wait-for-video`, `--playlist-random`, `--write-all-thumbnails`, `--keep-fragments`, `--max-sleep-interval`, `--embed-info-json`, `--simulate`
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
python main.py "URL" --add-metadata --no-part
python main.py "URL" --prefer-free-formats --quiet
python main.py "URL" --verbose --force-ipv6
python main.py "URL" --no-check-certificates --no-warnings
python main.py "URL" --age-limit 18
python main.py "URL" --playlist-start 2 --playlist-end 10
python main.py "URL" --skip-unavailable-fragments
python main.py "URL" --rate-limit 2M --sleep-requests 1
python main.py "URL" --match-filter "duration < 600"
python main.py "URL" --embed-chapters --convert-subs srt --sub-langs es,en
python main.py "URL" --flat-playlist --extractor-retries 5
python main.py "URL" --min-filesize 1M --max-filesize 500M
python main.py "URL" --dateafter 20260101 --datebefore 20261002
python main.py "URL" --match-title "live" --reject-title "trailer"
python main.py "URL" --trim-filenames 80 --lazy-playlist
python main.py "URL" --impersonate chrome
python main.py "URL" --by-uploader
python main.py "URL" --output-template "%(uploader)s/%(title)s.%(ext)s"
python main.py "URL" --format mp3 --ffmpeg-location "C:\\ffmpeg\\bin"
python main.py "URL" --referer "https://example.com" --user-agent "Mozilla/5.0"
python main.py "URL" --extractor-args "youtube:player_client=android"
python main.py "URL" --playlist-reverse --newline
python main.py "URL" --download-sections "*0:30-1:00" --write-link
python main.py "URL" --mark-watched --cookies-from-browser chrome
python main.py "URL" --wait-for-video 30
python main.py "URL" --playlist-random --max-sleep-interval 5
python main.py "URL" --write-all-thumbnails --embed-info-json
python main.py "URL" --keep-fragments
python main.py "URL" --simulate
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
yt-dlp>=2026.9.27
requests>=2.32.0
customtkinter>=5.2.0
Pillow>=10.4.0
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
