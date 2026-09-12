# Changelog

Todos los cambios notables en este proyecto seran documentados en este archivo.

## [1.2.1] - 2026-09-12

### Agregado / corregido
- downloader.py es codigo fuente legible (ya no depende de dl_part*.b64 para arrancar)
- Deteccion de TikTok, Instagram, X/Twitter, Facebook, Vimeo, Twitch, SoundCloud y Reddit
- Historial en history.json (carpeta de configuracion del sistema)
- CLI con --format, --quality, --output / -o y --no-playlist
- Ajuste allow_playlist (playlists activadas por defecto)

### Notas
- Sigue siendo necesario ffmpeg en el PATH para extraer MP3 de forma fiable
- Los dl_part*.b64 se conservan solo como respaldo del motor 1.1
