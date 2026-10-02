# Changelog

Todos los cambios notables en este proyecto seran documentados en este archivo.

## [1.18.0] - 2026-10-02

### Agregado
- Sitios extra: Kuaishou, Tencent Video (v.qq.com), HIDIVE, Jamendo, TwitCasting, FC2, RTVE, DW, France 24, SVT Play, NRK, CBC, RaiPlay, NetEase Cloud Music
- CLI: `--dateafter`, `--datebefore`, `--match-title`, `--reject-title`, `--trim-filenames`, `--lazy-playlist`, `--impersonate`

### Cambiado
- Version 1.18.0
- User-Agent HTTP actualizado (Chrome 149)
- setup.py y pagina de GitHub Pages alineados a 1.18.0

## [1.17.0] - 2026-10-01

### Agregado
- Sitios que faltaban en el motor de 1.16.0: PeerTube.fr, Spotify.link, Google Podcasts, Castbox, Anchor, Transistor, Buzzsprout, Libsyn, Simplecast, Overcast
- Sitios extra: Medal.tv, Hotstar, Viki, iQiyi, WeTV, SonyLIV, ZEE5, Audius, Gaana, Hungama, MX Player, Boomplay, Resso, Piped, Rokfin, Brighteon
- CLI: `--rate-limit`, `--match-filter`, `--embed-chapters`, `--convert-subs`, `--sub-langs`, `--flat-playlist`, `--min-filesize`, `--max-filesize`, `--sleep-requests`, `--extractor-retries`

### Cambiado
- Version del motor alineada a 1.17.0 (downloader.py seguia en 1.15.0)
- User-Agent HTTP actualizado (Chrome 148)
- Requisito `yt-dlp>=2026.9.27`
- setup.py alineado a 1.17.0

## [1.16.0] - 2026-09-30

### Agregado
- Sitios extra: PeerTube.fr, Spotify.link, Google Podcasts, Castbox, Anchor, Transistor, Buzzsprout, Libsyn, Simplecast, Overcast, Pocket Casts, Scribd, SlideShare
- Dependencias: `requests>=2.32.0`, `Pillow>=10.4.0`

### Cambiado
- Version 1.16.0
- User-Agent HTTP actualizado (Chrome 147)
- setup.py alineado a 1.16.0

## [1.15.0] - 2026-09-29

### Agregado
- Sitios extra: Giphy, Tenor, PBS, NBC, Reuters, NHK, Yandex Music, Anghami, Radio Javan, Discord CDN, Streamja
- CLI: `--no-check-certificates`, `--age-limit`, `--playlist-start`, `--playlist-end`, `--skip-unavailable-fragments`, `--no-warnings`

### Cambiado
- Version 1.15.0
- User-Agent HTTP actualizado (Chrome 146)
- setup.py alineado a 1.15.0

## [1.14.0] - 2026-09-28

### Agregado
- Sitios extra: Mega, MediaFire, OneDrive, Box, DeviantArt, ArtStation, Last.fm, iVoox, YouTube Kids, Amazon Music, Misskey, Kwai, StreamYard, Soundgasm, WeTransfer
- CLI: `--add-metadata`, `--no-part`, `--prefer-free-formats`, `--quiet`, `--verbose`, `--force-ipv6`

### Cambiado
- Version 1.14.0
- User-Agent HTTP actualizado (Chrome 145)
- setup.py alineado a 1.14.0

## [1.13.0] - 2026-09-26

### Agregado
- Sitios extra: Xiaohongshu, AbemaTV, ARTE, JioSaavn, Vocaroo, OPENREC, SHOWROOM, 17LIVE, AcFun, Google Drive, Dropbox, Al Jazeera
- CLI: `--write-comments`, `--break-on-existing`, `--live-from-start`, `--yes-playlist`

### Cambiado
- Version 1.13.0
- User-Agent HTTP actualizado (Chrome 144)

## [1.12.0] - 2026-09-25

### Agregado
- Sitios extra: Tidal, Apple Music, BandLab, Pixiv, live.nicovideo.jp, Crunchyroll
- CLI: `--ignore-errors`, `--write-description`

### Cambiado
- Version 1.12.0
- User-Agent HTTP actualizado (Chrome 143)

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
