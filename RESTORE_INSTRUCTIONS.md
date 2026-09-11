# Cómo funciona downloader.py (v1.2.0)

El archivo `downloader.py` es un bootstrap que carga el código desde `dl_part0.b64` … `dl_part3.b64` (gzip + base64).

## Ejecutar

```bash
pip install -r requirements.txt
python main.py
```

CLI:

```bash
python main.py "https://www.youtube.com/watch?v=..." --format mp3 --output ./Descargas
```

Novedades 1.2: TikTok/Instagram/X, playlists, historial (`history.json`) y CLI con `--format` / `--quality` / `--output` / `--no-playlist`.
