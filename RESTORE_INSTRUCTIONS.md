# Como funciona downloader.py

`downloader.py` es el codigo fuente completo y legible (v1.3.0).

Los archivos `dl_part*.b64` quedan como respaldo del motor 1.1. Ya no son necesarios para ejecutar la app.

```bash
pip install -r requirements.txt
python main.py
```

CLI:

```bash
python main.py "https://www.youtube.com/watch?v=..." --format video --quality 720
python main.py "https://www.youtube.com/watch?v=..." --format mp3 --output ./Descargas
python main.py "URL" --no-playlist
```
