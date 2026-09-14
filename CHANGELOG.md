# Changelog

Todos los cambios notables en este proyecto seran documentados en este archivo.

## [1.3.0] - 2026-09-14

### Agregado / corregido
- Version 1.3.0 en README, setup.py y CLI
- Mas sitios: Dailymotion y Bilibili (ademas de YT, TikTok, IG, X, Facebook, Vimeo, Twitch, SoundCloud, Reddit)
- CLI usa `merge_output_format=mp4` para unir video+audio de yt-dlp
- Selector de calidad CLI mas robusto (`bestvideo[height<=N]+bestaudio/best[height<=N]/best`)
- Historial en `history.json` y flags `--format`, `--quality`, `-o`, `--no-playlist`

### Notas
- El GUI sigue cargando el motor 1.1 desde `dl_part*.b64`
- ffmpeg en el PATH es necesario para MP3 y para merge de video

## [1.2.2] - 2026-09-13

### Agregado / corregido
- Deteccion de sitios de media e historial
- CLI basica

## [1.2.1] - 2026-09-12

### Notas
- Preparacion de la documentacion 1.2.1
