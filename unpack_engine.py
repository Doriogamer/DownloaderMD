#!/usr/bin/env python3
"""Genera engine.py decodificando dl_part*.b64."""
import base64
import gzip
import pathlib

here = pathlib.Path(__file__).resolve().parent
parts = sorted(here.glob("dl_part*.b64"))
if not parts:
    raise SystemExit("No hay archivos dl_part*.b64")
payload = "".join(p.read_text(encoding="utf-8").strip() for p in parts)
src = gzip.decompress(base64.b64decode(payload)).decode("utf-8")
src = src.replace('APP_VERSION = "1.1.0"', 'APP_VERSION = "1.6.0"', 1)
out = here / "engine.py"
out.write_text(src, encoding="utf-8")
print("Escrito", out, "(%s caracteres)" % len(src))
