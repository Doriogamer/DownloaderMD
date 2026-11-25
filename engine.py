#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""DownloaderMD engine - GUI + CLI downloader based on yt-dlp."""

import argparse
import json
import os
import sys
import threading
from datetime import datetime
from pathlib import Path

try:
    import customtkinter as ctk
    from tkinter import filedialog, messagebox
    HAS_GUI = True
except ImportError:
    HAS_GUI = False

import requests
import yt_dlp

APP_VERSION = "1.63.0"
SETTINGS_DIR = Path.home() / ".downloadermd"
SETTINGS_DIR.mkdir(exist_ok=True)
HISTORY_FILE = SETTINGS_DIR / "history.json"
CONFIG_FILE = SETTINGS_DIR / "config.json"

DEFAULT_UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"

def load_config():
    if CONFIG_FILE.exists():
        try:
            return json.loads(CONFIG_FILE.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {"output_dir": str(Path.home() / "Downloads"), "format": "video", "quality": "720"}

def save_config(cfg):
    CONFIG_FILE.write_text(json.dumps(cfg, indent=2), encoding="utf-8")

def load_history():
    if HISTORY_FILE.exists():
        try:
            return json.loads(HISTORY_FILE.read_text(encoding="utf-8"))
        except Exception:
            pass
    return []

def save_history(entry):
    hist = load_history()
    hist.insert(0, entry)
    hist = hist[:50]
    HISTORY_FILE.write_text(json.dumps(hist, indent=2), encoding="utf-8")

class Downloader:
    def __init__(self, url, output_dir, format_="video", quality="720", audio_format="mp3", audio_quality="320",
                 cookies=None, proxy=None, extra_opts=None):
        self.url = url
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.format = format_
        self.quality = quality
        self.audio_format = audio_format
        self.audio_quality = audio_quality
        self.cookies = cookies
        self.proxy = proxy
        self.extra_opts = extra_opts or {}

    def is_direct_link(self):
        video_sites = ("youtube", "youtu.be", "tiktok", "instagram", "twitter", "x.com", "facebook", "vimeo")
        return not any(s in self.url.lower() for s in video_sites) and any(self.url.lower().endswith(ext) for ext in (".mp4", ".mkv", ".webm", ".mp3", ".zip", ".rar", ".pdf", ".exe"))

    def download(self, progress_callback=None):
        if self.is_direct_link():
            return self._download_direct(progress_callback)
        else:
            return self._download_ytdlp(progress_callback)

    def _download_direct(self, progress_callback):
        headers = {"User-Agent": DEFAULT_UA}
        local_filename = self.output_dir / self.url.split("/")[-1].split("?")[0]
        mode = "ab" if local_filename.exists() else "wb"
        resume_pos = local_filename.stat().st_size if local_filename.exists() else 0
        if resume_pos:
            headers["Range"] = f"bytes={resume_pos}-"
        try:
            with requests.get(self.url, headers=headers, stream=True, timeout=30) as r:
                r.raise_for_status()
                total = int(r.headers.get("content-length", 0)) + resume_pos
                downloaded = resume_pos
                with open(local_filename, mode) as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
                            downloaded += len(chunk)
                            if progress_callback and total:
                                progress_callback(downloaded / total * 100)
            return str(local_filename)
        except Exception as e:
            raise RuntimeError(f"Direct download failed: {e}")

    def _download_ytdlp(self, progress_callback):
        ydl_opts = {
            "outtmpl": str(self.output_dir / "%(title)s.%(ext)s"),
            "quiet": True,
            "no_warnings": True,
            "http_headers": {"User-Agent": DEFAULT_UA},
        }
        if self.proxy:
            ydl_opts["proxy"] = self.proxy
        if self.cookies:
            ydl_opts["cookiefile"] = self.cookies

        if self.format == "audio":
            ydl_opts["format"] = "bestaudio/best"
            ydl_opts["postprocessors"] = [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": self.audio_format,
                "preferredquality": self.audio_quality,
            }]
        else:
            if self.quality.isdigit():
                ydl_opts["format"] = f"bestvideo[height<={self.quality}]+bestaudio/best[height<={self.quality}]"
            else:
                ydl_opts["format"] = "best"

        ydl_opts.update(self.extra_opts)

        def hook(d):
            if d["status"] == "downloading" and progress_callback:
                total = d.get("total_bytes") or d.get("total_bytes_estimate") or 0
                downloaded = d.get("downloaded_bytes", 0)
                if total:
                    progress_callback(downloaded / total * 100)

        ydl_opts["progress_hooks"] = [hook]

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(self.url, download=True)
            return ydl.prepare_filename(info)

class DownloaderGUI(ctk.CTk if HAS_GUI else object):
    def __init__(self):
        if not HAS_GUI:
            print("customtkinter no instalado. Usa la CLI.")
            return
        super().__init__()
        self.title(f"DownloaderMD v{APP_VERSION}")
        self.geometry("700x500")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.cfg = load_config()
        self.protocol("WM_DELETE_WINDOW", self.on_close)

        self.url_entry = ctk.CTkEntry(self, placeholder_text="Pega el link aquí...", width=500)
        self.url_entry.pack(pady=10, padx=20)

        opts = ctk.CTkFrame(self)
        opts.pack(pady=5, fill="x", padx=20)

        self.format_var = ctk.StringVar(value=self.cfg.get("format", "video"))
        ctk.CTkRadioButton(opts, text="Video", variable=self.format_var, value="video").pack(side="left", padx=10)
        ctk.CTkRadioButton(opts, text="Audio (MP3)", variable=self.format_var, value="audio").pack(side="left", padx=10)

        self.quality_var = ctk.StringVar(value=self.cfg.get("quality", "720"))
        ctk.CTkComboBox(opts, values=["360", "480", "720", "1080", "best"], variable=self.quality_var).pack(side="left", padx=10)

        self.folder_btn = ctk.CTkButton(opts, text="Carpeta", command=self.choose_folder)
        self.folder_btn.pack(side="left", padx=10)
        self.folder_label = ctk.CTkLabel(opts, text=self.cfg.get("output_dir", "Downloads")[-30:])
        self.folder_label.pack(side="left", padx=5)

        self.dl_btn = ctk.CTkButton(self, text="DESCARGAR", command=self.start_download, height=40)
        self.dl_btn.pack(pady=15)

        self.progress = ctk.CTkProgressBar(self)
        self.progress.pack(pady=5, padx=20, fill="x")
        self.progress.set(0)
        self.status = ctk.CTkLabel(self, text="Listo")
        self.status.pack(pady=5)

        self.history_box = ctk.CTkTextbox(self, height=150)
        self.history_box.pack(pady=10, padx=20, fill="both", expand=True)
        self.refresh_history()

    def choose_folder(self):
        folder = filedialog.askdirectory(initialdir=self.cfg.get("output_dir"))
        if folder:
            self.cfg["output_dir"] = folder
            self.folder_label.configure(text=folder[-40:])
            save_config(self.cfg)

    def refresh_history(self):
        hist = load_history()
        self.history_box.delete("1.0", "end")
        for h in hist[:10]:
            self.history_box.insert("end", f"{h.get('time', '')} - {h.get('title', h.get('url', ''))[:60]}\n")

    def start_download(self):
        url = self.url_entry.get().strip()
        if not url:
            messagebox.showwarning("Error", "Pega un link primero")
            return
        self.dl_btn.configure(state="disabled")
        self.status.configure(text="Descargando...")
        self.progress.set(0)
        threading.Thread(target=self._do_download, args=(url,), daemon=True).start()

    def _do_download(self, url):
        try:
            dl = Downloader(
                url=url,
                output_dir=self.cfg.get("output_dir", str(Path.home() / "Downloads")),
                format_=self.format_var.get(),
                quality=self.quality_var.get(),
            )
            def cb(p):
                self.after(0, lambda: self.progress.set(p / 100))
            result = dl.download(cb)
            entry = {
                "time": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "url": url,
                "title": Path(result).stem if result else url,
                "path": result
            }
            save_history(entry)
            self.after(0, lambda: self.status.configure(text=f"Completado: {Path(result).name}"))
            self.after(0, self.refresh_history)
        except Exception as e:
            self.after(0, lambda: messagebox.showerror("Error", str(e)))
            self.after(0, lambda: self.status.configure(text="Error"))
        finally:
            self.after(0, lambda: self.dl_btn.configure(state="normal"))

    def on_close(self):
        self.cfg["format"] = self.format_var.get()
        self.cfg["quality"] = self.quality_var.get()
        save_config(self.cfg)
        self.destroy()

def main():
    parser = argparse.ArgumentParser(description=f"DownloaderMD v{APP_VERSION}")
    parser.add_argument("url", nargs="?", help="URL a descargar")
    parser.add_argument("-o", "--output", default=None, help="Carpeta de salida")
    parser.add_argument("--format", choices=["video", "audio", "mp3"], default="video")
    parser.add_argument("--quality", default="720")
    parser.add_argument("--audio-quality", default="320")
    parser.add_argument("--cookies", default=None)
    parser.add_argument("--proxy", default=None)
    parser.add_argument("--show-history", action="store_true")
    args = parser.parse_args()

    if args.show_history:
        for h in load_history():
            print(h)
        return

    if not args.url:
        if HAS_GUI:
            app = DownloaderGUI()
            app.mainloop()
        else:
            parser.print_help()
        return

    cfg = load_config()
    out = args.output or cfg.get("output_dir")
    dl = Downloader(
        url=args.url,
        output_dir=out,
        format_="audio" if args.format in ("audio", "mp3") else "video",
        quality=args.quality,
        audio_quality=args.audio_quality,
        cookies=args.cookies,
        proxy=args.proxy,
    )
    print(f"Descargando {args.url} ...")
    try:
        result = dl.download()
        print(f"Completado: {result}")
        save_history({
            "time": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "url": args.url,
            "title": Path(result).stem,
            "path": result
        })
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
