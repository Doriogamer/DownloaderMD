# Cómo funciona downloader.py (v1.2.0)

A partir de la v1.2 el código fuente completo vive otra vez en `downloader.py`.
Los archivos `dl_part*.b64` de la v1.1 ya no se usan.

## Ejecutar

```bash
pip install -r requirements.txt
python main.py
```

CLI:

```bash
python main.py "https://www.youtube.com/watch?v=..." --format mp3 --output ./Descargas
```

El historial se guarda en la carpeta de configuración del sistema (`history.json`).
