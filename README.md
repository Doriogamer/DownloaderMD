# 📥 DownloaderMD

**Descargador universal para YouTube, MP3 y links directos**  
Interfaz gráfica moderna. Funciona en Windows 10+. ¡Rápido, fácil y sin complicaciones!

![Python](https://img.shields.io/badge/Python-3.8+-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Version](https://img.shields.io/badge/Version-1.2.2-brightgreen)
![Status](https://img.shields.io/badge/Status-Active-success)

---

## ✨ Características

- **📺 YouTube y más**: YouTube, TikTok, Instagram, X/Twitter, Facebook, Vimeo y otros sitios compatibles con yt-dlp
- **📃 Playlists**: Descarga listas de reproducción (se puede desactivar en Ajustes / `--no-playlist`)
- **🎵 MP3**: Extrae solo el audio de YouTube con un click
- **🌐 Enlaces directos**: Descarga cualquier archivo desde un link directo
- **🎨 Interfaz moderna**: GUI estilo WhatsApp, intuitiva y bonita
- **⚡ Rápido**: Optimizado para descargas veloces
- **💻 Multiplataforma**: Windows, Linux y macOS (configuración guardada en la carpeta de datos del sistema)
- **📜 Historial**: Últimas descargas en `history.json`

---

## 📥 Instalación

### Opción 1: Descargar el instalador (Recomendado)

1. Ve a la sección **[Releases](https://github.com/Doriogamer/DownloaderMD/releases)**
2. Descarga `installer.exe` (versión más reciente)
3. Ejecuta el instalador
4. ¡Listo! La aplicación aparecerá en tu escritorio

### Opción 2: Instalación manual (Para desarrolladores)

**Requisitos previos:**
- Python 3.8 o superior
- pip (gestor de paquetes de Python)
- Git (opcional)

**Pasos:**

```bash
git clone https://github.com/Doriogamer/DownloaderMD.git
cd DownloaderMD
pip install -r requirements.txt
python main.py
```

---

## 🛠️ Requisitos del Sistema

| Requisito | Mínimo | Recomendado |
|-----------|--------|------------|
| **OS** | Windows 10 | Windows 10/11 |
| **Python** | 3.8 | 3.10+ |
| **RAM** | 512 MB | 2 GB |
| **Espacio** | 100 MB | 500 MB |
| **Internet** | Requerida | Requerida |

---

## 🚀 Cómo Usar

### Usar la interfaz gráfica:

1. **Abre la aplicación** DownloaderMD
2. **Pega un link** en la barra de entrada
3. **Selecciona el formato** en Ajustes (video o MP3)
4. **Elige la carpeta de destino** (opcional)
5. **Haz click en "DESCARGAR"** y espera

### Uso desde línea de comandos:

```bash
python main.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ" --format video --quality 720
python main.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ" --format mp3 -o ./Descargas
python main.py "URL" --no-playlist
```

---

## 📦 Dependencias

```
yt-dlp>=2025.1.0
requests>=2.31.0
customtkinter>=5.2.0
Pillow>=10.0.0
```

---

## 🐛 Solucionar Problemas

### "No se puede conectar a YouTube"
- Verifica tu conexión
- Actualiza yt-dlp: `pip install --upgrade yt-dlp`

### El programa no abre
- `pip install --upgrade -r requirements.txt`
- Python 3.8+
- Abre un [Issue](https://github.com/Doriogamer/DownloaderMD/issues)

---

## 📜 Licencia

MIT. Autor: **Doriogamer** — [GitHub](https://github.com/Doriogamer)

Contacto: dalvarezwallace2@gmail.com
