# Como funciona DownloaderMD

`downloader.py` anade deteccion de sitios, historial, CLI y version 1.10.
El motor GUI esta en `engine.py`. Si no existe, se decodifican `dl_part*.b64`.

```bash
pip install -r requirements.txt
python main.py
```

CLI:

```bash
python main.py "https://www.youtube.com/watch?v=..." --format video --quality 720
python main.py "https://www.youtube.com/watch?v=..." --format mp3 --audio-quality 320 -o ./Descargas
python main.py "URL" --no-playlist
python main.py "URL" --cookies-from-browser chrome
python main.py "URL" --cookies cookies.txt
python main.py "URL" --subs --thumbnail
python main.py "URL" --embed-subs --merge-format mkv
python main.py "URL" --list-formats
python main.py "URL" --max-downloads 5 --playlist-items 1-3
python main.py "URL" --retries 20 --geo-bypass
python main.py --version
```
