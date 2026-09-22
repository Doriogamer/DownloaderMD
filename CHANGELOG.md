# Changelog

Todos los cambios notables en este proyecto seran documentados en este archivo.

## [1.11.0] - 2026-09-22

### Agregado
- Sitios extra: Trovo, AfreecaTV, Naver TV, media.ccc.de, CuriosityStream, Dropout, ESPN, BBC, CNN, NPR, Spotify, Deezer
- CLI: `--windows-filenames`, `--no-overwrites`, `--keep-video`, `--force-ipv4`, `--socket-timeout`, `--concurrent-fragments`

### Cambiado
- Version 1.11.0
- User-Agent HTTP actualizado (Chrome 142)
- Requisito `yt-dlp>=2026.8.19`
- Fragmentos concurrentes por defecto a 12

## [1.10.0] - 2026-09-21

### Agregado
- Sitios extra: aliases de YouTube/Facebook/Reddit/Threads, Audiomack, HearThis, Podbean, CapCut, Likee, Weverse, CHZZK, SOOP
- CLI: `--embed-subs`, `--merge-format` (mp4/mkv/webm), `--retries`, `--no-mtime`, `--geo-bypass`

### Cambiado
- Version 1.10.0
- User-Agent HTTP actualizado (Chrome 141)
- Reintentos de media a 18 y 10 fragmentos concurrentes
