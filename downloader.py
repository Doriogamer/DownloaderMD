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
