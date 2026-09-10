# Cómo funciona downloader.py (v1.1.0)

El archivo `downloader.py` es un **bootstrap** ligero que carga el código completo desde los archivos `dl_part0.b64`, `dl_part1.b64` y `dl_part2.b64` (gzip + base64).

## Por qué está así

GitHub tiene límites de tamaño en algunas operaciones de API. Para poder subir el código completo de ~55 KB se dividió en partes.

## Cómo obtener el código fuente completo

```bash
# Desde el repositorio clonado:
python3 -c "
import gzip, base64, pathlib, glob
parts = sorted(glob.glob('dl_part*.b64'))
payload = ''.join(pathlib.Path(p).read_text().strip() for p in parts)
data = gzip.decompress(base64.b64decode(payload))
pathlib.Path('downloader_full.py').write_bytes(data)
print('Escrito downloader_full.py (' + str(len(data)) + ' bytes)')
"
```

O simplemente ejecuta:

```bash
python main.py
```

El bootstrap carga y ejecuta el código completo en memoria.

## Contenido de la v1.1.0

- Rutas de configuración portables (Windows / Linux / macOS)
- Soporte para `music.youtube.com` y `m.youtube.com`
- `main.py` como punto de entrada
- Dependencias actualizadas
