# -*- coding: utf-8 -*-
"""DownloaderMD v1.1.0 — carga el código desde dl_part*.b64"""
import gzip, base64, pathlib

_here = pathlib.Path(__file__).resolve().parent
_parts = sorted(_here.glob("dl_part*.b64"))
if not _parts:
    raise RuntimeError("Faltan archivos dl_part*.b64 junto a downloader.py")
_payload = "".join(p.read_text(encoding="utf-8").strip() for p in _parts)
_src = gzip.decompress(base64.b64decode(_payload)).decode("utf-8")
exec(compile(_src, str(pathlib.Path(__file__).resolve()), "exec"), globals())
