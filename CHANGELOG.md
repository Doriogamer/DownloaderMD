# Changelog

Todos los cambios notables en este proyecto seran documentados en este archivo.

## [1.3.0] - 2026-09-14

### Agregado / corregido
- `downloader.py` es ahora el motor completo y legible (ya no ejecuta `dl_part*.b64`)
- Deteccion de TikTok, Instagram, X/Twitter, Facebook, Vimeo, Twitch, SoundCloud, Reddit, Dailymotion y Bilibili
- Historial en `history.json` (carpeta de configuracion del sistema)
- CLI con `--format`, `--quality`, `--output` / `-o` y `--no-playlist`
- Ajuste `allow_playlist` (playlists activadas por defecto) aplicado tambien en la GUI
- Fusion MP4 (`merge_output_format`) para video+audio de yt-dlp
- Version alineada en setup.py, README y GUI

### Notas
- Sigue siendo necesario ffmpeg en el PATH para extraer MP3 y unir video+audio
- Los `dl_part*.b64` se conservan solo como respaldo historico del motor 1.1

## [1.2.2] - 2026-09-13

### Agregado / corregido
- Preparacion de CLI e historial (el arranque seguia dependiendo del payload)
- Deteccion extra de sitios de media

## [1.2.1] - 2026-09-12

### Notas
- Preparacion de la documentacion 1.2.1
