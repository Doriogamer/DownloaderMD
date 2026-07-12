
import os
import yt_dlp

url = input("Escribe la URL aquí: ")

if "youtube.com" in url or "youtu.be" in url:
    print("📺 Detectado: YouTube")

    opciones = {
        "format": "best[height<=720]",
        "outtmpl": "%(title)s.%(ext)s"
    }

    try:
        with yt_dlp.YoutubeDL(opciones) as ydl:
            ydl.download([url])
        print("✅ Descarga completada.")
    except Exception as e:
        print("❌ Error:", e)

else:
    print("🌐 Detectado: Enlace normal")

    codigo = os.system(f'wget "{url}"')

    if codigo == 0:
        print("✅ Descarga completada.")
    else:
        print("❌ No se pudo descargar el archivo.")