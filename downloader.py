# -*- coding: utf-8 -*-
"""DownloaderMD v1.10.0 — motor abierto + CLI/GUI."""
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

APP_VERSION = "1.10.0"
HISTORY_FILE = os.path.join(SETTINGS_DIR, "history.json")
HTTP_UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36"

MEDIA_HOSTS = (
    "youtube.com", "youtu.be", "youtube-nocookie.com", "music.youtube.com",
    "m.youtube.com", "tv.youtube.com",
    "tiktok.com", "vm.tiktok.com", "vt.tiktok.com",
    "instagram.com", "instagr.am", "threads.net", "threads.com",
    "x.com", "twitter.com",
    "facebook.com", "fb.watch", "fb.com", "m.facebook.com",
    "vimeo.com", "twitch.tv", "clips.twitch.tv",
    "soundcloud.com", "reddit.com", "redd.it", "v.redd.it",
    "dailymotion.com", "dai.ly",
    "bilibili.com", "bilibili.tv", "b23.tv",
    "pinterest.com", "pin.it", "bandcamp.com", "mixcloud.com",
    "kick.com", "rumble.com", "bsky.app", "bsky.social",
    "flickr.com", "ted.com", "streamable.com", "imgur.com",
    "linkedin.com", "vk.com", "odysee.com", "newgrounds.com", "archive.org",
    "nicovideo.jp", "tumblr.com", "9gag.com", "truthsocial.com",
    "bitchute.com", "peertube.tv", "mastodon.social", "gab.com",
    "lbry.tv", "weibo.com", "youku.com", "loom.com",
    "snapchat.com", "douyin.com", "ixigua.com", "rutube.ru", "ok.ru",
    "dzen.ru", "vkvideo.ru", "coub.com",
    "patreon.com", "substack.com", "podcasts.apple.com", "nebula.tv",
    "floatplane.com", "aparat.com", "niconico.com",
    "audiomack.com", "hearthis.at", "podbean.com",
    "capcut.com", "likee.video", "weverse.io",
    "chzzk.naver.com", "soop.live",
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


def _filename_from_headers(url, headers):
    cd = headers.get("Content-Disposition") or headers.get("content-disposition") or ""
    match = re.search(r"filename\*=UTF-8''([^;]+)", cd, re.I)
    if match:
        return urllib.parse.unquote(match.group(1))
    match = re.search(r'filename="?([^";]+)"?', cd, re.I)
    if match:
        return match.group(1)
    name = os.path.basename(urllib.parse.urlparse(url).path) or "archivo"
    return name


def _http_download(url, outdir):
    headers = {"User-Agent": HTTP_UA}
    dest_name = None
    dest = None
    resume_from = 0
    head = requests.head(url, timeout=30, headers=headers, allow_redirects=True)
    final_url = head.url if head.ok else url
    dest_name = _filename_from_headers(final_url, head.headers if head.ok else {})
    dest_name = re.sub(r'[\\/*?:"<>|]', "", dest_name).strip() or "archivo"
    dest = os.path.join(outdir, dest_name)
    if os.path.exists(dest):
        resume_from = os.path.getsize(dest)
        headers["Range"] = "bytes=%d-" % resume_from
    try:
        response = requests.get(url, stream=True, timeout=45, headers=headers)
        if response.status_code == 416:
            print("[+] Ya estaba completo:", dest)
            return dest
        response.raise_for_status()
    except Exception as exc:
        print("[-] No se pudo descargar el archivo:", exc)
        sys.exit(1)
    if response.status_code != 206:
        resume_from = 0
        dest_name = _filename_from_headers(response.url, response.headers)
        dest_name = re.sub(r'[\\/*?:"<>|]', "", dest_name).strip() or "archivo"
        dest = os.path.join(outdir, dest_name)
    total = int(response.headers.get("content-length") or 0)
    if resume_from and response.status_code == 206:
        cr = response.headers.get("Content-Range") or ""
        m = re.search(r"/(\d+)", cr)
        if m:
            total = int(m.group(1))
        else:
            total += resume_from
    mode = "ab" if resume_from and response.status_code == 206 else "wb"
    done = resume_from
    with open(dest, mode) as f:
        for chunk in response.iter_content(chunk_size=65536):
            if chunk:
                f.write(chunk)
                done += len(chunk)
                if total:
                    print("\r    %.1f%%" % (100.0 * done / total), end="", flush=True)
    print()
    print("[+] Guardado:", dest)
    return dest


def run_cli_mode(url_input, fmt="video", quality="720", output=None, no_playlist=False, cookies_from_browser=None, audio_quality="192", write_subs=False, write_thumbnail=False, list_formats=False, proxy=None, restrict_filenames=False, embed_thumbnail=False, sponsorblock=False, download_archive=None, write_info_json=False, audio_format="mp3", cookies=None, max_downloads=None, playlist_items=None, sleep_interval=None, embed_subs=False, merge_format="mp4", retries=18, no_mtime=False, geo_bypass=False):
    print("DownloaderMD CLI v%s" % APP_VERSION)
    url = validate_url(url_input)
    if not url:
        print("[-] URL no valida.")
        sys.exit(1)
    outdir = output or os.getcwd()
    os.makedirs(outdir, exist_ok=True)
    if is_media_url(url) or is_youtube_url(url):
        qmap = {"360": 360, "480": 480, "720": 720, "1080": 1080, "1440": 1440, "2160": 2160}
        if fmt in ("mp3", "audio"):
            yfmt = "bestaudio/best"
        elif str(quality) in qmap:
            h = qmap[str(quality)]
            yfmt = "bestvideo[height<=%s]+bestaudio/best[height<=%s]/best" % (h, h)
        else:
            yfmt = "bestvideo+bestaudio/best"
        merge = merge_format if merge_format in ("mp4", "mkv", "webm") else "mp4"
        try:
            retries_n = int(retries)
        except (TypeError, ValueError):
            retries_n = 18
        ydl_opts = {
            "outtmpl": os.path.join(outdir, "%(title)s.%(ext)s"),
            "format": yfmt,
            "noplaylist": no_playlist,
            "merge_output_format": merge,
            "progress_hooks": [_progress_hook],
            "retries": retries_n,
            "fragment_retries": retries_n,
            "concurrent_fragment_downloads": 10,
            "ignoreerrors": False,
            "writethumbnail": write_thumbnail or embed_thumbnail,
            "writesubtitles": write_subs or embed_subs,
            "writeautomaticsub": write_subs,
            "subtitleslangs": ["es", "en", "es-orig", "en-orig"],
            "restrictfilenames": restrict_filenames,
            "writeinfojson": write_info_json,
            "updatetime": not no_mtime,
            "geo_bypass": geo_bypass,
        }
        if proxy:
            ydl_opts["proxy"] = proxy
        if list_formats:
            ydl_opts["listformats"] = True
        if cookies_from_browser:
            ydl_opts["cookiesfrombrowser"] = (cookies_from_browser,)
        if cookies:
            ydl_opts["cookiefile"] = cookies
        if download_archive:
            ydl_opts["download_archive"] = download_archive
        if max_downloads:
            ydl_opts["max_downloads"] = int(max_downloads)
        if playlist_items:
            ydl_opts["playlist_items"] = playlist_items
        if sleep_interval is not None:
            ydl_opts["sleep_interval"] = float(sleep_interval)
            ydl_opts["max_sleep_interval"] = float(sleep_interval) + 2
        if sponsorblock:
            ydl_opts["sponsorblock_remove"] = ["sponsor", "selfpromo", "interaction"]
        post = []
        if fmt in ("mp3", "audio") and not list_formats:
            codec = audio_format if audio_format in ("mp3", "m4a", "opus", "wav", "flac") else "mp3"
            post.append({
                "key": "FFmpegExtractAudio",
                "preferredcodec": codec,
                "preferredquality": str(audio_quality),
            })
        if embed_thumbnail and fmt in ("mp3", "audio") and not list_formats:
            post.append({"key": "FFmpegMetadata"})
            post.append({"key": "EmbedThumbnail"})
        if embed_subs and fmt == "video" and not list_formats:
            post.append({"key": "FFmpegEmbedSubtitle"})
        if post:
            ydl_opts["postprocessors"] = post
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=not list_formats)
                if list_formats:
                    print("[+] Formatos listados.")
                    return
                print("[+] Completado:", (info or {}).get("title", "download"))
                append_history(url, outdir, "media")
        except Exception as exc:
            print("[-] Error al descargar:", exc)
            print("    Prueba: pip install --upgrade yt-dlp")
            print("    Si pide login: --cookies-from-browser chrome  o  --cookies cookies.txt")
            sys.exit(1)
    else:
        dest = _http_download(url, outdir)
        append_history(url, dest, "http")


def main():
    import argparse
    parser = argparse.ArgumentParser(
        prog="downloadermd",
        description="DownloaderMD — YouTube, redes y links directos",
    )
    parser.add_argument("url", nargs="?", help="URL a descargar")
    parser.add_argument("--format", dest="fmt", choices=["video", "mp3", "audio"], default="video")
    parser.add_argument("--quality", default="720")
    parser.add_argument("--audio-quality", dest="audio_quality", default="192", help="bitrate MP3: 128, 192, 256, 320")
    parser.add_argument("--audio-format", dest="audio_format", default="mp3", choices=["mp3", "m4a", "opus", "wav", "flac"], help="Codec de audio si --format mp3/audio")
    parser.add_argument("--output", "-o", default=None)
    parser.add_argument("--no-playlist", action="store_true")
    parser.add_argument(
        "--cookies-from-browser",
        dest="cookies_from_browser",
        default=None,
        help="chrome, firefox, edge, brave, opera, chromium",
    )
    parser.add_argument("--cookies", default=None, help="Archivo Netscape de cookies")
    parser.add_argument("--subs", action="store_true", help="Descargar subtitulos si existen")
    parser.add_argument("--embed-subs", action="store_true", help="Embeber subtitulos en el video")
    parser.add_argument("--thumbnail", action="store_true", help="Guardar miniatura")
    parser.add_argument("--embed-thumbnail", action="store_true", help="Embeber miniatura en audio")
    parser.add_argument("--list-formats", action="store_true", help="Listar formatos sin descargar")
    parser.add_argument("--proxy", default=None, help="Proxy HTTP/SOCKS, ej. http://127.0.0.1:8080")
    parser.add_argument("--restrict-filenames", action="store_true", help="Nombres de archivo ASCII seguros")
    parser.add_argument("--sponsorblock", action="store_true", help="Quitar segmentos sponsor/selfpromo/interaction")
    parser.add_argument("--download-archive", dest="download_archive", default=None, help="Archivo de IDs ya descargados")
    parser.add_argument("--write-info-json", action="store_true", help="Guardar metadata .info.json")
    parser.add_argument("--max-downloads", dest="max_downloads", default=None, help="Limite de items en playlist")
    parser.add_argument("--playlist-items", dest="playlist_items", default=None, help="Items de playlist, ej. 1-5,8")
    parser.add_argument("--sleep-interval", dest="sleep_interval", default=None, help="Pausa entre items (segundos)")
    parser.add_argument("--merge-format", dest="merge_format", default="mp4", choices=["mp4", "mkv", "webm"], help="Contenedor al unir video+audio")
    parser.add_argument("--retries", default="18", help="Reintentos de red y fragmentos")
    parser.add_argument("--no-mtime", action="store_true", help="No usar fecha del servidor en el archivo")
    parser.add_argument("--geo-bypass", action="store_true", help="Intentar saltar bloqueos geograficos")
    parser.add_argument("--version", action="version", version="DownloaderMD %s" % APP_VERSION)
    args, extra = parser.parse_known_args()
    if args.url:
        run_cli_mode(
            args.url, args.fmt, args.quality, args.output, args.no_playlist,
            args.cookies_from_browser, args.audio_quality, args.subs, args.thumbnail,
            args.list_formats, args.proxy, args.restrict_filenames, args.embed_thumbnail,
            args.sponsorblock, args.download_archive, args.write_info_json, args.audio_format,
            args.cookies, args.max_downloads, args.playlist_items, args.sleep_interval,
            args.embed_subs, args.merge_format, args.retries, args.no_mtime, args.geo_bypass,
        )
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
