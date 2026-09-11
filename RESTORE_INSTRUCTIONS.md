# Cómo funciona downloader.py

`downloader.py` es un bootstrap que carga el motor desde `dl_part0.b64`, `dl_part1.b64` y `dl_part2.b64` (gzip + base64).

```bash
pip install -r requirements.txt
python main.py
```

La documentación (README / CHANGELOG) describe la línea 1.2: más sitios, playlists, historial y CLI con flags.
El payload empaquetado en `dl_part*.b64` todavía corresponde al motor 1.1 hasta que se suba el código fuente completo en un siguiente commit.
