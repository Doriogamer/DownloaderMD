# -*- coding: utf-8 -*-
"""DownloaderMD v1.2.2 — carga el motor 1.1 y aplica mejoras 1.2."""
import gzip, base64, pathlib, os, sys, re, time, json, urllib.parse

_here = pathlib.Path(__file__).resolve().parent
_parts = sorted(_here.glob("dl_part*.b64"))
if not _parts:
    raise RuntimeError("Faltan archivos dl_part*.b64 junto a downloader.py")
_payload = "".join(p.read_text(encoding="utf-8").strip() for p in _parts)
_src = gzip.decompress(base64.b64decode(_payload)).decode("utf-8")
exec(compile(_src, str(_here / "engine_legacy.py"), "exec"), globals())

APP_VERSION = "1.2.2"
HISTORY_FILE = os.path.join(SETTINGS_DIR, "history.json")

MEDIA_HOSTS = (
    "youtube.com", "youtu.be", "youtube-nocookie.com", "music.youtube.com",
    "tiktok.com", "instagram.com", "x.com", "twitter.com", "facebook.com",
    "fb.watch", "vimeo.com", "twitch.tv", "soundcloud.com", "reddit.com",
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
        data.append({"url": url, "path": path, "kind": kind, "ts": time.strftime("%Y-%m-%d %H:%M:%S")})
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

def run_cli_mode(url_input, fmt="video", quality="720", output=None, no_playlist=False):
    print("DownloaderMD CLI v%s" % APP_VERSION)
    url = validate_url(url_input)
    if not url:
        print("[-] URL no valida.")
        sys.exit(1)
    outdir = output or os.getcwd()
    os.makedirs(outdir, exist_ok=True)
    if is_media_url(url) or is_youtube_url(url):
        qmap = {"360": 360, "480": 480, "720": 720, "1080": 1080}
        if fmt == "mp3":
            yfmt = "bestaudio/best"
        elif str(quality) in qmap:
            yfmt = "bestvideo[height<=%s]+bestaudio/best" % qmap[str(quality)]
        else:
            yfmt = "bestvideo+bestaudio/best"
        ydl_opts = {"outtmpl": os.path.join(outdir, "%(title)s.%(ext)s"), "format": yfmt, "noplaylist": no_playlist}
        if fmt == "mp3":
            ydl_opts["postprocessors"] = [{"key": "FFmpegExtractAudio", "preferredcodec": "mp3", "preferredquality": "192"}]
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
        with open(dest, "wb") as f:
            for chunk in response.iter_content(chunk_size=65536):
                if chunk:
                    f.write(chunk)
        print("[+] Guardado:", dest)
        append_history(url, dest, "http")

def main():
    import argparse
    parser = argparse.ArgumentParser(prog="downloadermd")
    parser.add_argument("url", nargs="?", help="URL a descargar")
    parser.add_argument("--format", dest="fmt", choices=["video", "mp3"], default="video")
    parser.add_argument("--quality", default="720")
    parser.add_argument("--output", "-o", default=None)
    parser.add_argument("--no-playlist", action="store_true")
    args, extra = parser.parse_known_args()
    if args.url:
        run_cli_mode(args.url, args.fmt, args.quality, args.output, args.no_playlist)
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
