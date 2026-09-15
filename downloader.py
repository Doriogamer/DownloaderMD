# -*- coding: utf-8 -*-
"""DownloaderMD v1.4.0 — motor abierto + CLI/GUI."""
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

# Preferir engine.py (fuente abierta). Fallback: dl_part*.b64 (motor 1.1 empaquetado).
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

APP_VERSION = "1.4.0"
HISTORY_FILE = os.path.join(SETTINGS_DIR, "history.json")

MEDIA_HOSTS = (
    "youtube.com", "youtu.be", "youtube-nocookie.com", "music.youtube.com",
    "tiktok.com", "instagram.com", "x.com", "twitter.com", "facebook.com",
    "fb.watch", "vimeo.com", "twitch.tv", "soundcloud.com", "reddit.com",
    "dailymotion.com", "bilibili.com", "pinterest.com", "pin.it",
    "bandcamp.com", "mixcloud.com", "kick.com", "rumble.com",
)


def is_media_url(url):
    try:
        domain = urllib.parse.urlparse(url).netloc.lower()
        return any(h in domain for h in MEDIA_HOSTS)
    except Exception:
        return False


def append_history(url, path, kind):
    try:
        os.makedirs(SETTINGS_DIR, exist_ok=True)
        data = []
        if os.path.exists(HISTORY_FILE):
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                data = json.load(f) or []
        data.append({
            "url": url,
            "path": path,
            "kind": kind,
            "ts": time.strftime("%Y-%m-%d %H:%M:%S"),
        })
        with open(HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump(data[-200:], f, indent=2, ensure_ascii=False)
    except Exception:
        pass


_orig_on_send = WhatsAppDownloaderApp.on_send


def _on_send(self):
    url_input = self.url_entry.get().strip()
    if not url_input:
        return
    self.url_entry.delete(0, "end")
    self.add_user_message(url_input)
    url = validate_url(url_input)
    if not url:
        self.add_system_message("URL no valida.")
        return
    if is_media_url(url):
        self.chat_list_items["downloader"].update_status("Analizando media...")
        process_youtube_url_gui(self, url)
    else:
        _orig_on_send(self)
        return


WhatsAppDownloaderApp.on_send = _on_send


def _progress_hook(d):
    if d.get("status") == "downloading":
        pct = d.get("_percent_str", "").strip()
        spd = d.get("_speed_str", "").strip()
        eta = d.get("_eta_str", "").strip()
        print("\r    %s  %s  ETA %s" % (pct, spd, eta), end="", flush=True)
    elif d.get("status") == "finished":
        print("\r    100%  procesando...                    ")


def run_cli_mode(url_input, fmt="video", quality="720", output=None, no_playlist=False, cookies_from_browser=None):
    print("DownloaderMD CLI v%s" % APP_VERSION)
    url = validate_url(url_input)
    if not url:
        print("[-] URL no valida.")
        sys.exit(1)
    outdir = output or os.getcwd()
    os.makedirs(outdir, exist_ok=True)
    if is_media_url(url) or is_youtube_url(url):
        qmap = {"360": 360, "480": 480, "720": 720, "1080": 1080, "1440": 1440, "2160": 2160}
        if fmt == "mp3":
            yfmt = "bestaudio/best"
        elif str(quality) in qmap:
            h = qmap[str(quality)]
            yfmt = "bestvideo[height<=%s]+bestaudio/best[height<=%s]/best" % (h, h)
        else:
            yfmt = "bestvideo+bestaudio/best"
        ydl_opts = {
            "outtmpl": os.path.join(outdir, "%(title)s.%(ext)s"),
            "format": yfmt,
            "noplaylist": no_playlist,
            "merge_output_format": "mp4",
            "progress_hooks": [_progress_hook],
            "retries": 5,
            "fragment_retries": 5,
        }
        if cookies_from_browser:
            ydl_opts["cookiesfrombrowser"] = (cookies_from_browser,)
        if fmt == "mp3":
            ydl_opts["postprocessors"] = [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }]
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            print("[+] Completado:", (info or {}).get("title", "download"))
            append_history(url, outdir, "media")
    else:
        response = requests.get(url, stream=True, timeout=30)
        response.raise_for_status()
        filename = os.path.basename(urllib.parse.urlparse(response.url).path) or "archivo"
        filename = re.sub(r'[\\/*?:"<>|]', "", filename)
        dest = os.path.join(outdir, filename)
        total = int(response.headers.get("content-length") or 0)
        done = 0
        with open(dest, "wb") as f:
            for chunk in response.iter_content(chunk_size=65536):
                if chunk:
                    f.write(chunk)
                    done += len(chunk)
                    if total:
                        print("\r    %.1f%%" % (100.0 * done / total), end="", flush=True)
        print()
        print("[+] Guardado:", dest)
        append_history(url, dest, "http")


def main():
    import argparse
    parser = argparse.ArgumentParser(
        prog="downloadermd",
        description="DownloaderMD — YouTube, redes y links directos",
    )
    parser.add_argument("url", nargs="?", help="URL a descargar")
    parser.add_argument("--format", dest="fmt", choices=["video", "mp3"], default="video")
    parser.add_argument("--quality", default="720")
    parser.add_argument("--output", "-o", default=None)
    parser.add_argument("--no-playlist", action="store_true")
    parser.add_argument(
        "--cookies-from-browser",
        dest="cookies_from_browser",
        default=None,
        help="chrome, firefox, edge, brave, opera, chromium",
    )
    args, extra = parser.parse_known_args()
    if args.url:
        run_cli_mode(args.url, args.fmt, args.quality, args.output, args.no_playlist, args.cookies_from_browser)
    elif extra:
        run_cli_mode(extra[0])
    else:
        run_gui_mode()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[-] Cancelado.")
        sys.exit(0)
