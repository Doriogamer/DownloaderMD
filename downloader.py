# -*- coding: utf-8 -*-
"""DownloaderMD v1.12.0 — motor abierto + CLI/GUI."""
import gzip
import base64
import pathlib
import os
import sys
import re
import time
import json
import urllib.parse

_here = pathlib.Path(__file__).resolve().parent

_engine_path = _here / "engine.py"
if _engine_path.exists():
    import engine as _engine
    globals().update({k: getattr(_engine, k) for k in dir(_engine) if not k.startswith("__")})
else:
    _parts = sorted(_here.glob("dl_part*.b64"))
    if not _parts:
        raise RuntimeError("Faltan engine.py y archivos dl_part*.b64")
    _payload = "".join(p.read_text(encoding="utf-8").strip() for p in _parts)
    _src = gzip.decompress(base64.b64decode(_payload)).decode("utf-8")
    exec(compile(_src, str(_here / "engine_legacy.py"), "exec"), globals())

APP_VERSION = "1.12.0"
HISTORY_FILE = os.path.join(SETTINGS_DIR, "history.json")
HTTP_UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36"
