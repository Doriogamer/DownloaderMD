# -*- coding: utf-8 -*-
"""DownloaderMD v1.23.0 — motor abierto + CLI/GUI."""
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

APP_VERSION = "1.23.0"
HISTORY_FILE = os.path.join(SETTINGS_DIR, "history.json")
HTTP_UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/154.0.0.0 Safari/537.36"

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
    "trovo.live", "afreecatv.com", "tv.naver.com", "naver.com",
    "media.ccc.de", "curiositystream.com", "dropout.tv",
    "espn.com", "bbc.co.uk", "cnn.com", "npr.org",
    "spotify.com", "open.spotify.com", "deezer.com",
    "tidal.com", "music.apple.com", "bandlab.com",
    "pixiv.net", "live.nicovideo.jp",
    "crunchyroll.com", "funimation.com",
    "xiaohongshu.com", "xhslink.com",
    "abema.tv", "abema.io",
    "arte.tv", "jiosaavn.com",
    "vocaroo.com", "openrec.tv",
    "showroom-live.com", "17.live",
    "acfun.cn", "drive.google.com",
    "dropbox.com", "aljazeera.com",
    "mega.nz", "mega.co.nz", "mediafire.com",
    "onedrive.live.com", "1drv.ms", "box.com",
    "deviantart.com", "artstation.com", "last.fm",
    "ivoox.com", "youtubekids.com", "music.amazon.com",
    "misskey.io", "kwai.com", "streamyard.com",
    "soundgasm.net", "wetransfer.com",
    "giphy.com", "tenor.com", "pbs.org", "nbc.com",
    "reuters.com", "nhk.or.jp", "music.yandex.ru", "yandex.ru",
    "anghami.com", "radiojavan.com", "discord.com", "cdn.discordapp.com",
    "streamja.com", "streamable.com",
    "peertube.fr", "spotify.link", "podcasts.google.com",
    "castbox.fm", "anchor.fm", "transistor.fm", "buzzsprout.com",
    "libsyn.com", "simplecast.com", "overcast.fm",
    "medal.tv", "hotstar.com", "viki.com", "iq.com", "iqiyi.com",
    "wetv.vip", "sonyliv.com", "zee5.com", "audius.co",
    "gaana.com", "hungama.com", "mxplayer.in", "boomplay.com",
    "resso.com", "piped.video", "rokfin.com", "brighteon.com",
    "kuaishou.com", "v.qq.com", "hidive.com", "jamendo.com",
    "twitcasting.tv", "fc2.com", "video.fc2.com",
    "rtve.es", "dw.com", "france24.com", "svtplay.se",
    "nrk.no", "cbc.ca", "raiplay.it", "music.163.com",
    "steamcommunity.com", "steampowered.com",
    "ign.com", "gamespot.com",
    "coursera.org", "udemy.com", "edx.org", "khanacademy.org",
    "theverge.com", "polygon.com", "vox.com",
    "bloomberg.com", "wsj.com", "ft.com",
    "nytimes.com", "washingtonpost.com",
    "pocketcasts.com", "scribd.com", "slideshare.net",
    "abc.com", "abcnews.go.com", "cbs.com", "cbsnews.com",
    "sky.com", "news.sky.com", "euronews.com", "theguardian.com",
    "lemonde.fr", "spiegel.de", "npo.nl", "npostart.nl",
    "stream.cz", "wistia.com", "wistia.net",
    "gofile.io", "pixeldrain.com", "catbox.moe", "4shared.com",
    "t.me", "telegram.me", "peertube.social", "video.ibm.com",
    "pan.baidu.com", "baidu.com",
    "commons.wikimedia.org", "wikimedia.org", "imdb.com",
    "foxnews.com", "fox.com", "msnbc.com", "apnews.com", "economist.com",
    "elpais.com", "elmundo.es", "globo.com", "globoplay.globo.com",
    "zdf.de", "ardmediathek.de", "france.tv", "itv.com", "channel4.com",
    "dr.dk", "yle.fi", "atresplayer.com", "tver.jp", "dlive.tv",
    "audioboom.com", "spreaker.com", "acast.com", "megaphone.fm", "omny.fm",
    "pandora.com", "qobuz.com", "freesound.org", "photos.google.com",
    "disk.yandex.ru", "yadi.sk", "cloud.mail.ru", "xbox.com",
    "redgifs.com", "joinpeertube.org",
    "bbc.com", "bbc.in", "abc.net.au", "sbs.com.au", "9now.com.au", "10play.com.au",
    "pluto.tv", "tubi.tv", "crackle.com", "vidyard.com", "sproutvideo.com",
    "gettr.com", "minds.com", "banned.video", "veoh.com",
    "snackvideo.com", "triller.co", "lemon8-app.com", "sharechat.com", "mojapp.in",
    "player.fm", "podcastaddict.com", "tunein.com", "iheart.com",
    "streamtape.com", "doodstream.com", "mixdrop.co", "streamwish.to",
    "tv.kakao.com", "kakao.com", "viu.com", "jiocinema.com",
    "rte.ie", "orf.at", "srf.ch", "rts.ch", "rsi.ch", "tvp.pl",
    "cctv.com", "video.sina.com.cn", "sina.com.cn", "sohu.com", "tv.sohu.com",
    "metacafe.com", "vevo.com", "vidlii.com", "clippituser.tv",
    "peertube.wtf", "niconico.jp",
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
    match = re.search(r'filename="?([^\";]+)"?', cd, re.I)
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


def run_cli_mode(url_input, fmt="video", quality="720", output=None, no_playlist=False, cookies_from_browser=None, audio_quality="192", write_subs=False, write_thumbnail=False, list_formats=False, proxy=None, restrict_filenames=False, embed_thumbnail=False, sponsorblock=False, download_archive=None, write_info_json=False, audio_format="mp3", cookies=None, max_downloads=None, playlist_items=None, sleep_interval=None, embed_subs=False, merge_format="mp4", retries=18, no_mtime=False, geo_bypass=False, windows_filenames=False, no_overwrites=False, keep_video=False, force_ipv4=False, socket_timeout=None, concurrent_fragments=12, ignore_errors=False, write_description=False, write_comments=False, break_on_existing=False, live_from_start=False, yes_playlist=False, add_metadata=False, no_part=False, prefer_free_formats=False, quiet=False, verbose=False, force_ipv6=False, no_check_certificates=False, age_limit=None, playlist_start=None, playlist_end=None, skip_unavailable_fragments=False, no_warnings=False, rate_limit=None, match_filter=None, embed_chapters=False, convert_subs=None, sub_langs=None, flat_playlist=False, min_filesize=None, max_filesize=None, sleep_requests=None, extractor_retries=None, dateafter=None, datebefore=None, match_title=None, reject_title=None, trim_filenames=None, lazy_playlist=False, impersonate=None, output_template=None, ffmpeg_location=None, by_uploader=False, referer=None, user_agent=None, extractor_args=None, playlist_reverse=False, download_sections=None, newline=False, write_link=False, mark_watched=False, wait_for_video=None, playlist_random=False, write_all_thumbnails=False, keep_fragments=False, max_sleep_interval=None, embed_info_json=False, simulate=False, write_auto_subs=False, xattrs=False, retry_sleep=None, fragment_retries=None, http_chunk_size=None, format_sort=None, break_on_reject=False, parse_metadata=None, abort_on_error=False, file_access_retries=None, sleep_subtitles=None, throttled_rate=None, buffer_size=None, no_cache_dir=False, compat_options=None, no_write_playlist_metafiles=False):
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
        if output_template:
            outtmpl = output_template
            if not os.path.isabs(outtmpl):
                outtmpl = os.path.join(outdir, outtmpl)
        elif by_uploader:
            outtmpl = os.path.join(outdir, "%(uploader|unknown)s", "%(title)s.%(ext)s")
        else:
            outtmpl = os.path.join(outdir, "%(title)s.%(ext)s")
        ydl_opts = {
            "outtmpl": outtmpl,
            "format": yfmt,
            "noplaylist": False if yes_playlist else no_playlist,
            "merge_output_format": merge,
            "progress_hooks": [_progress_hook],
            "retries": retries_n,
            "fragment_retries": retries_n,
            "concurrent_fragment_downloads": 12,
            "ignoreerrors": ignore_errors,
            "writedescription": write_description,
            "getcomments": write_comments,
            "break_on_existing": break_on_existing,
            "live_from_start": live_from_start,
            "nopart": no_part,
            "prefer_free_formats": prefer_free_formats,
            "quiet": quiet,
            "verbose": verbose,
            "nocheckcertificate": no_check_certificates,
            "no_warnings": no_warnings,
            "writethumbnail": write_thumbnail or embed_thumbnail,
            "writesubtitles": write_subs or embed_subs,
            "writeautomaticsub": write_subs,
            "subtitleslangs": ["es", "en", "es-orig", "en-orig"],
            "restrictfilenames": restrict_filenames,
            "windowsfilenames": windows_filenames,
            "nooverwrites": no_overwrites,
            "keepvideo": keep_video,
            "writeinfojson": write_info_json,
            "updatetime": not no_mtime,
            "geo_bypass": geo_bypass,
        }
        try:
            cf = int(concurrent_fragments)
            if cf >= 1:
                ydl_opts["concurrent_fragment_downloads"] = cf
        except (TypeError, ValueError):
            pass
        if force_ipv4:
            ydl_opts["source_address"] = "0.0.0.0"
        if force_ipv6:
            ydl_opts["source_address"] = "::"
        if age_limit not in (None, ""):
            try:
                ydl_opts["age_limit"] = int(age_limit)
            except (TypeError, ValueError):
                pass
        if playlist_start not in (None, ""):
            try:
                ydl_opts["playliststart"] = int(playlist_start)
            except (TypeError, ValueError):
                pass
        if playlist_end not in (None, ""):
            try:
                ydl_opts["playlistend"] = int(playlist_end)
            except (TypeError, ValueError):
                pass
        if skip_unavailable_fragments:
            ydl_opts["skip_unavailable_fragments"] = True
        if rate_limit:
            ydl_opts["ratelimit"] = rate_limit
        if match_filter:
            ydl_opts["match_filter"] = match_filter
        if embed_chapters:
            ydl_opts["embedchapters"] = True
        if flat_playlist:
            ydl_opts["extract_flat"] = "in_playlist"
        if min_filesize:
            ydl_opts["min_filesize"] = min_filesize
        if max_filesize:
            ydl_opts["max_filesize"] = max_filesize
        if sleep_requests is not None:
            try:
                ydl_opts["sleep_interval_requests"] = float(sleep_requests)
            except (TypeError, ValueError):
                pass
        if extractor_retries not in (None, ""):
            try:
                ydl_opts["extractor_retries"] = int(extractor_retries)
            except (TypeError, ValueError):
                pass
        if dateafter:
            ydl_opts["dateafter"] = str(dateafter)
        if datebefore:
            ydl_opts["datebefore"] = str(datebefore)
        if match_title:
            ydl_opts["matchtitle"] = match_title
        if reject_title:
            ydl_opts["rejecttitle"] = reject_title
        if trim_filenames not in (None, ""):
            try:
                ydl_opts["trim_file_name"] = int(trim_filenames)
            except (TypeError, ValueError):
                pass
        if lazy_playlist:
            ydl_opts["lazy_playlist"] = True
        if impersonate:
            ydl_opts["impersonate"] = impersonate
        if ffmpeg_location:
            ydl_opts["ffmpeg_location"] = ffmpeg_location
        if referer:
            ydl_opts["referer"] = referer
        if user_agent:
            ydl_opts.setdefault("http_headers", {})["User-Agent"] = user_agent
        if extractor_args:
            parsed = {}
            # formato yt-dlp: extractor:clave=valor;clave2=a,b
            for chunk in str(extractor_args).split(" "):
                if ":" not in chunk:
                    continue
                ext, rest = chunk.split(":", 1)
                opts = parsed.setdefault(ext, {})
                for pair in rest.split(";"):
                    if "=" not in pair:
                        continue
                    key, val = pair.split("=", 1)
                    opts[key] = [x for x in val.split(",") if x]
            if parsed:
                ydl_opts["extractor_args"] = parsed
        if playlist_reverse:
            ydl_opts["playlistreverse"] = True
        if download_sections:
            try:
                ydl_opts["download_ranges"] = yt_dlp.utils.download_range_func(None, [download_sections])
            except Exception:
                print("[-] --download-sections no se pudo aplicar:", download_sections)
        if newline:
            ydl_opts["progress_with_newline"] = True
        if write_link:
            ydl_opts["writelink"] = True
        if mark_watched:
            ydl_opts["mark_watched"] = True
        if wait_for_video not in (None, ""):
            try:
                ydl_opts["wait_for_video"] = int(wait_for_video)
            except (TypeError, ValueError):
                pass
        if playlist_random:
            ydl_opts["playlistrandom"] = True
        if write_all_thumbnails:
            ydl_opts["write_all_thumbnails"] = True
        if keep_fragments:
            ydl_opts["keep_fragments"] = True
        if max_sleep_interval not in (None, ""):
            try:
                ydl_opts["max_sleep_interval"] = float(max_sleep_interval)
            except (TypeError, ValueError):
                pass
        if embed_info_json:
            ydl_opts["embed_infojson"] = True
        if simulate:
            ydl_opts["skip_download"] = True
        if write_auto_subs:
            ydl_opts["writeautomaticsub"] = True
        if xattrs:
            ydl_opts["xattrs"] = True
        if break_on_reject:
            ydl_opts["break_on_reject"] = True
        if retry_sleep:
            ydl_opts["retry_sleep_functions"] = {"http": float(retry_sleep), "fragment": float(retry_sleep), "extractor": float(retry_sleep)}
        if fragment_retries not in (None, ""):
            try:
                ydl_opts["fragment_retries"] = int(fragment_retries)
            except (TypeError, ValueError):
                pass
        if http_chunk_size:
            ydl_opts["http_chunk_size"] = http_chunk_size
        if format_sort:
            ydl_opts["format_sort"] = [x.strip() for x in str(format_sort).split(",") if x.strip()]
        if parse_metadata:
            ydl_opts["parse_metadata"] = str(parse_metadata)
        if abort_on_error:
            ydl_opts["ignoreerrors"] = False
            ydl_opts["abort_on_error"] = True
        if file_access_retries not in (None, ""):
            try:
                ydl_opts["file_access_retries"] = int(file_access_retries)
            except (TypeError, ValueError):
                pass
        if sleep_subtitles not in (None, ""):
            try:
                ydl_opts["sleep_interval_subtitles"] = float(sleep_subtitles)
            except (TypeError, ValueError):
                pass
        if throttled_rate:
            ydl_opts["throttledratelimit"] = throttled_rate
        if buffer_size:
            ydl_opts["buffersize"] = buffer_size
        if no_cache_dir:
            ydl_opts["cachedir"] = False
        if compat_options:
            ydl_opts["compat_opts"] = [x.strip() for x in str(compat_options).split(",") if x.strip()]
        if no_write_playlist_metafiles:
            ydl_opts["allow_playlist_files"] = False
        if sub_langs:
            langs = [x.strip() for x in str(sub_langs).split(",") if x.strip()]
            if langs:
                ydl_opts["subtitleslangs"] = langs
        if convert_subs in ("srt", "vtt", "ass", "lrc"):
            ydl_opts["convertsubtitles"] = convert_subs
        if socket_timeout:
            try:
                ydl_opts["socket_timeout"] = float(socket_timeout)
            except (TypeError, ValueError):
                pass
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
        if fmt in ("mp3", "audio") and not list_formats:
            import shutil
            ffmpeg_ok = bool(ffmpeg_location) or shutil.which("ffmpeg")
            if not ffmpeg_ok:
                print("[-] ffmpeg no esta en el PATH. El audio no se puede extraer sin ffmpeg.")
                print("    Instalalo o pasa --ffmpeg-location RUTA")
                sys.exit(1)
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
        if embed_chapters and not list_formats:
            post.append({"key": "FFmpegEmbedChapter"})
        if add_metadata and not list_formats:
            post.append({"key": "FFmpegMetadata"})
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
    parser.add_argument("--windows-filenames", action="store_true", help="Nombres compatibles con Windows")
    parser.add_argument("--no-overwrites", action="store_true", help="No sobrescribir archivos existentes")
    parser.add_argument("--keep-video", action="store_true", help="Conservar el video original al extraer audio")
    parser.add_argument("--force-ipv4", action="store_true", help="Forzar conexiones IPv4")
    parser.add_argument("--socket-timeout", dest="socket_timeout", default=None, help="Timeout de socket en segundos")
    parser.add_argument("--concurrent-fragments", dest="concurrent_fragments", default="12", help="Fragmentos HLS/DASH en paralelo")
    parser.add_argument("--ignore-errors", action="store_true", help="Continuar si falla un item de playlist")
    parser.add_argument("--write-description", action="store_true", help="Guardar descripcion .description")
    parser.add_argument("--write-comments", action="store_true", help="Guardar comentarios si el extractor los ofrece")
    parser.add_argument("--break-on-existing", action="store_true", help="Parar si el archivo ya esta en el archive")
    parser.add_argument("--live-from-start", action="store_true", help="En lives, empezar desde el inicio si es posible")
    parser.add_argument("--yes-playlist", action="store_true", help="Forzar descarga de playlist completa")
    parser.add_argument("--add-metadata", action="store_true", help="Escribir metadatos en el archivo con ffmpeg")
    parser.add_argument("--no-part", action="store_true", help="No usar archivos .part temporales")
    parser.add_argument("--prefer-free-formats", action="store_true", help="Preferir formatos libres (webm/opus)")
    parser.add_argument("--quiet", action="store_true", help="Menos salida en consola")
    parser.add_argument("--verbose", action="store_true", help="Mas detalle de yt-dlp")
    parser.add_argument("--force-ipv6", action="store_true", help="Forzar conexiones IPv6")
    parser.add_argument("--no-check-certificates", action="store_true", help="No verificar certificados TLS")
    parser.add_argument("--age-limit", dest="age_limit", default=None, help="Limite de edad para contenido restringido")
    parser.add_argument("--playlist-start", dest="playlist_start", default=None, help="Primer item de playlist")
    parser.add_argument("--playlist-end", dest="playlist_end", default=None, help="Ultimo item de playlist")
    parser.add_argument("--skip-unavailable-fragments", action="store_true", help="Saltar fragmentos HLS/DASH faltantes")
    parser.add_argument("--no-warnings", action="store_true", help="Ocultar avisos de yt-dlp")
    parser.add_argument("--rate-limit", dest="rate_limit", default=None, help="Limite de velocidad, ej. 2M o 500K")
    parser.add_argument("--match-filter", dest="match_filter", default=None, help="Filtro yt-dlp, ej. duration < 600")
    parser.add_argument("--embed-chapters", action="store_true", help="Embeber capitulos si existen")
    parser.add_argument("--convert-subs", dest="convert_subs", default=None, choices=["srt", "vtt", "ass", "lrc"], help="Convertir subtitulos")
    parser.add_argument("--sub-langs", dest="sub_langs", default=None, help="Idiomas de subtitulos, separados por coma")
    parser.add_argument("--flat-playlist", action="store_true", help="No resolver cada item de la playlist")
    parser.add_argument("--min-filesize", dest="min_filesize", default=None, help="Tamano minimo, ej. 1M")
    parser.add_argument("--max-filesize", dest="max_filesize", default=None, help="Tamano maximo, ej. 500M")
    parser.add_argument("--sleep-requests", dest="sleep_requests", default=None, help="Pausa entre peticiones HTTP (segundos)")
    parser.add_argument("--extractor-retries", dest="extractor_retries", default=None, help="Reintentos del extractor")
    parser.add_argument("--dateafter", default=None, help="Solo videos posteriores a YYYYMMDD")
    parser.add_argument("--datebefore", default=None, help="Solo videos anteriores a YYYYMMDD")
    parser.add_argument("--match-title", dest="match_title", default=None, help="Regex de titulos a incluir")
    parser.add_argument("--reject-title", dest="reject_title", default=None, help="Regex de titulos a excluir")
    parser.add_argument("--trim-filenames", dest="trim_filenames", default=None, help="Recortar nombres a N caracteres")
    parser.add_argument("--lazy-playlist", action="store_true", help="Procesar la playlist de forma perezosa")
    parser.add_argument("--impersonate", default=None, help="Cliente a imitar, ej. chrome")
    parser.add_argument("--output-template", dest="output_template", default=None, help="Plantilla yt-dlp, ej. %(uploader)s/%(title)s.%(ext)s")
    parser.add_argument("--ffmpeg-location", dest="ffmpeg_location", default=None, help="Carpeta o binario de ffmpeg")
    parser.add_argument("--by-uploader", action="store_true", help="Guardar en una carpeta por autor/canal")
    parser.add_argument("--referer", default=None, help="Cabecera Referer para el sitio")
    parser.add_argument("--user-agent", dest="user_agent", default=None, help="User-Agent HTTP propio")
    parser.add_argument("--extractor-args", dest="extractor_args", default=None, help="Argumentos del extractor, ej. youtube:player_client=android")
    parser.add_argument("--playlist-reverse", action="store_true", help="Descargar la playlist al reves")
    parser.add_argument("--download-sections", dest="download_sections", default=None, help="Tramos, ej. *0:30-1:00")
    parser.add_argument("--newline", action="store_true", help="Progreso en lineas nuevas")
    parser.add_argument("--write-link", action="store_true", help="Guardar un .url con el enlace")
    parser.add_argument("--mark-watched", action="store_true", help="Marcar el video como visto en YouTube si hay cookies")
    parser.add_argument("--wait-for-video", dest="wait_for_video", default=None, help="Segundos a esperar si el video aun no esta disponible")
    parser.add_argument("--playlist-random", action="store_true", help="Descargar la playlist en orden aleatorio")
    parser.add_argument("--write-all-thumbnails", action="store_true", help="Guardar todas las miniaturas disponibles")
    parser.add_argument("--keep-fragments", action="store_true", help="Conservar fragmentos tras unir el video")
    parser.add_argument("--max-sleep-interval", dest="max_sleep_interval", default=None, help="Tope aleatorio de pausa entre items")
    parser.add_argument("--embed-info-json", action="store_true", help="Embeber metadata .info.json en el archivo")
    parser.add_argument("--simulate", action="store_true", help="Resolver el enlace sin descargar el archivo")
    parser.add_argument("--write-auto-subs", action="store_true", help="Guardar subtitulos automaticos")
    parser.add_argument("--xattrs", action="store_true", help="Escribir metadata en atributos extendidos del archivo")
    parser.add_argument("--retry-sleep", type=float, default=None, help="Segundos de espera entre reintentos")
    parser.add_argument("--fragment-retries", type=int, default=None, help="Reintentos por fragmento")
    parser.add_argument("--http-chunk-size", default=None, help="Tamano de chunk HTTP, p.ej. 10M")
    parser.add_argument("--format-sort", default=None, help="Orden de formatos, p.ej. res,fps,codec")
    parser.add_argument("--break-on-reject", action="store_true", help="Parar la playlist al primer video rechazado")
    parser.add_argument("--parse-metadata", default=None, help="Regla de metadata yt-dlp, p.ej. %(title)s:%(meta_title)s")
    parser.add_argument("--batch-file", "-a", default=None, help="Archivo con una URL por linea")
    parser.add_argument("--abort-on-error", action="store_true", help="Parar al primer error en vez de seguir")
    parser.add_argument("--file-access-retries", type=int, default=None, help="Reintentos si el archivo de salida esta ocupado")
    parser.add_argument("--sleep-subtitles", type=float, default=None, help="Pausa entre descargas de subtitulos (segundos)")
    parser.add_argument("--throttled-rate", default=None, help="Reintentar si la velocidad baja de este limite, p.ej. 100K")
    parser.add_argument("--buffer-size", default=None, help="Tamano del buffer de descarga, p.ej. 16K")
    parser.add_argument("--no-cache-dir", action="store_true", help="No usar la cache de yt-dlp")
    parser.add_argument("--compat-options", default=None, help="Opciones de compatibilidad, separadas por coma")
    parser.add_argument("--no-write-playlist-metafiles", action="store_true", help="No escribir .description/.info de la playlist")
    parser.add_argument("--show-history", action="store_true", help="Mostrar el historial local y salir")
    parser.add_argument("--clear-history", action="store_true", help="Borrar el historial local y salir")
    parser.add_argument("--version", action="version", version="DownloaderMD %s" % APP_VERSION)
    args, extra = parser.parse_known_args()
    if args.show_history or args.clear_history:
        if args.clear_history and os.path.exists(HISTORY_FILE):
            os.remove(HISTORY_FILE)
            print("[+] Historial borrado.")
        elif args.clear_history:
            print("[+] No habia historial.")
        if args.show_history:
            if not os.path.exists(HISTORY_FILE):
                print("[-] Sin historial.")
            else:
                with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                    items = json.load(f) or []
                for item in items[-50:]:
                    print("%s  %s  %s" % (item.get("ts", ""), item.get("kind", ""), item.get("url", "")))
        return
    if args.batch_file:
        batch = pathlib.Path(args.batch_file)
        if not batch.is_file():
            print("[-] No existe el archivo:", args.batch_file)
            sys.exit(1)
        urls = [ln.strip() for ln in batch.read_text(encoding="utf-8").splitlines() if ln.strip() and not ln.strip().startswith("#")]
        if not urls:
            print("[-] El archivo de lote no tiene URLs.")
            sys.exit(1)
        for url in urls:
            run_cli_mode(
            url, args.fmt, args.quality, args.output, args.no_playlist,
            args.cookies_from_browser, args.audio_quality, args.subs, args.thumbnail,
            args.list_formats, args.proxy, args.restrict_filenames, args.embed_thumbnail,
            args.sponsorblock, args.download_archive, args.write_info_json, args.audio_format,
            args.cookies, args.max_downloads, args.playlist_items, args.sleep_interval,
            args.embed_subs, args.merge_format, args.retries, args.no_mtime, args.geo_bypass,
            args.windows_filenames, args.no_overwrites, args.keep_video, args.force_ipv4,
            args.socket_timeout, args.concurrent_fragments, args.ignore_errors,
            args.write_description, args.write_comments, args.break_on_existing,
            args.live_from_start, args.yes_playlist, args.add_metadata, args.no_part,
            args.prefer_free_formats, args.quiet, args.verbose, args.force_ipv6,
            args.no_check_certificates, args.age_limit, args.playlist_start,
            args.playlist_end, args.skip_unavailable_fragments, args.no_warnings,
            args.rate_limit, args.match_filter, args.embed_chapters, args.convert_subs,
            args.sub_langs, args.flat_playlist, args.min_filesize, args.max_filesize,
            args.sleep_requests, args.extractor_retries, args.dateafter, args.datebefore,
            args.match_title, args.reject_title, args.trim_filenames, args.lazy_playlist,
            args.impersonate, args.output_template, args.ffmpeg_location, args.by_uploader, args.referer, args.user_agent, args.extractor_args, args.playlist_reverse, args.download_sections, args.newline, args.write_link, args.mark_watched, args.wait_for_video, args.playlist_random, args.write_all_thumbnails, args.keep_fragments, args.max_sleep_interval, args.embed_info_json, args.simulate, args.write_auto_subs, args.xattrs, args.retry_sleep, args.fragment_retries, args.http_chunk_size, args.format_sort, args.break_on_reject, args.parse_metadata, args.abort_on_error, args.file_access_retries, args.sleep_subtitles, args.throttled_rate, args.buffer_size, args.no_cache_dir, args.compat_options, args.no_write_playlist_metafiles,
            )
        return
    if args.url:
        run_cli_mode(
            args.url, args.fmt, args.quality, args.output, args.no_playlist,
            args.cookies_from_browser, args.audio_quality, args.subs, args.thumbnail,
            args.list_formats, args.proxy, args.restrict_filenames, args.embed_thumbnail,
            args.sponsorblock, args.download_archive, args.write_info_json, args.audio_format,
            args.cookies, args.max_downloads, args.playlist_items, args.sleep_interval,
            args.embed_subs, args.merge_format, args.retries, args.no_mtime, args.geo_bypass,
            args.windows_filenames, args.no_overwrites, args.keep_video, args.force_ipv4,
            args.socket_timeout, args.concurrent_fragments, args.ignore_errors,
            args.write_description, args.write_comments, args.break_on_existing,
            args.live_from_start, args.yes_playlist, args.add_metadata, args.no_part,
            args.prefer_free_formats, args.quiet, args.verbose, args.force_ipv6,
            args.no_check_certificates, args.age_limit, args.playlist_start,
            args.playlist_end, args.skip_unavailable_fragments, args.no_warnings,
            args.rate_limit, args.match_filter, args.embed_chapters, args.convert_subs,
            args.sub_langs, args.flat_playlist, args.min_filesize, args.max_filesize,
            args.sleep_requests, args.extractor_retries, args.dateafter, args.datebefore,
            args.match_title, args.reject_title, args.trim_filenames, args.lazy_playlist,
            args.impersonate, args.output_template, args.ffmpeg_location, args.by_uploader, args.referer, args.user_agent, args.extractor_args, args.playlist_reverse, args.download_sections, args.newline, args.write_link, args.mark_watched, args.wait_for_video, args.playlist_random, args.write_all_thumbnails, args.keep_fragments, args.max_sleep_interval, args.embed_info_json, args.simulate, args.write_auto_subs, args.xattrs, args.retry_sleep, args.fragment_retries, args.http_chunk_size, args.format_sort, args.break_on_reject, args.parse_metadata, args.abort_on_error, args.file_access_retries, args.sleep_subtitles, args.throttled_rate, args.buffer_size, args.no_cache_dir, args.compat_options, args.no_write_playlist_metafiles,
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
