# Changelog

Todos los cambios notables en este proyecto seran documentados en este archivo.

## [1.6.0] - 2026-09-17

### Agregado
- Sitios extra: LinkedIn, VK, Odysee, Newgrounds, Archive.org, NicoNico, Tumblr, 9GAG, Truth Social
- CLI: `--subs`, `--thumbnail` y `--list-formats`
- User-Agent de navegador en descargas HTTP directas

### Cambiado
- Version 1.6.0
- Reintentos de media subidos a 10

## [1.5.0] - 2026-09-16

### Agregado
- Script `unpack_engine.py` para generar `engine.py` desde `dl_part*.b64`
- Sitios extra: Threads, Bluesky, Flickr, TED, Streamable, Imgur
- CLI: `--audio-quality` (128/192/256/320) y `--version`
- Mensajes de error mas claros si yt-dlp o el link fallan
- Archivo LICENSE (MIT)

### Cambiado
- Version 1.5.0
- Mas reintentos en descargas de media (8)

## [1.4.0] - 2026-09-15

### Agregado
- Mas sitios: Pinterest, Bandcamp, Mixcloud, Kick, Rumble
- CLI: barra de progreso, reintentos, calidades 1440p y 2160p
- CLI: `--cookies-from-browser` (chrome, firefox, edge, brave, opera, chromium)
- Progreso en descargas HTTP directas
- `downloader.py` puede cargar `engine.py` si existe; si no, usa `dl_part*.b64`

### Cambiado
- Version 1.4.0 en README, setup, landing y CLI

## [1.3.0] - 2026-09-14

### Agregado / corregido
- Version 1.3.0 en README, setup.py y CLI
- Mas sitios: Dailymotion y Bilibili
- CLI usa `merge_output_format=mp4`
- Selector de calidad CLI mas robusto
- Historial en `history.json` y flags `--format`, `--quality`, `-o`, `--no-playlist`

### Notas
- ffmpeg en el PATH es necesario para MP3 y para merge de video

## [1.2.2] - 2026-09-13

### Agregado / corregido
- Deteccion de sitios de media e historial
- CLI basica

## [1.2.1] - 2026-09-12

### Notas
- Preparacion de la documentacion 1.2.1
