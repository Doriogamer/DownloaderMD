# 📥 DownloaderMD

**Descargador universal para YouTube, MP3 y links directos**  
Interfaz gráfica moderna. Funciona en Windows 10+. ¡Rápido, fácil y sin complicaciones!

![Python](https://img.shields.io/badge/Python-3.8+-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Version](https://img.shields.io/badge/Version-1.0-brightgreen)
![Status](https://img.shields.io/badge/Status-Active-success)

---

## ✨ Características

- **📺 YouTube**: Descarga videos en 360p, 480p, 720p, 1080p
- **🎵 MP3**: Extrae solo el audio de YouTube con un click
- **🌐 Enlaces directos**: Descarga cualquier archivo desde un link directo
- **🎨 Interfaz moderna**: GUI estilo WhatsApp, intuitiva y bonita
- **⚡ Rápido**: Optimizado para descargas veloces
- **💻 Multiplataforma**: Windows 10+ (Linux y macOS en desarrollo)

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
# Clonar el repositorio
git clone https://github.com/Doriogamer/DownloaderMD.git
cd DownloaderMD

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar la aplicación
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
2. **Pega un link** en la barra de entrada:
   - Para YouTube: `https://www.youtube.com/watch?v=...`
   - Para archivos: cualquier link directo (`https://ejemplo.com/archivo.zip`)
3. **Selecciona el formato:**
   - 📹 Video (elige resolución: 360p, 480p, 720p, 1080p)
   - 🎵 MP3 (solo audio)
4. **Elige la carpeta de destino** (opcional)
5. **Haz click en "DESCARGAR"** y espera
6. ✅ ¡Tu archivo estará listo en la carpeta especificada!

### Uso desde línea de comandos:

```bash
# Descargar video de YouTube
python main.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ" --format video --quality 720

# Descargar como MP3
python main.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ" --format mp3

# Descargar archivo directo
python main.py "https://ejemplo.com/archivo.zip" --output "./Descargas"
```

---

## 📦 Dependencias

```
yt-dlp>=2024.1.0     # Para descargas de YouTube
requests>=2.28.0     # Para descargas HTTP
```

Todas se instalan automáticamente con:
```bash
pip install -r requirements.txt
```

---

## 🎨 Interfaz

La interfaz está diseñada con inspiración en **WhatsApp** para máxima familiaridad:

- ✅ Diseño limpio y minimalista
- ✅ Controles intuitivos
- ✅ Indicador de progreso en tiempo real
- ✅ Notificaciones de éxito/error claras
- ✅ Temas oscuro y claro

---

## 🐛 Solucionar Problemas

### "No se puede conectar a YouTube"
- ✅ Verifica tu conexión a internet
- ✅ Intenta con otro video
- ✅ Actualiza yt-dlp: `pip install --upgrade yt-dlp`

### "La descarga es muy lenta"
- ✅ Esto depende de tu conexión y el servidor
- ✅ Intenta con una resolución menor
- ✅ Descarga en horarios menos congestionados

### "Error de permisos al descargar"
- ✅ Asegúrate de tener permisos de escritura en la carpeta
- ✅ Intenta guardar en una carpeta diferente (ej: Documentos)

### El programa no abre
- ✅ Reinstala: `pip install --upgrade -r requirements.txt`
- ✅ Asegúrate de tener Python 3.8+
- ✅ Abre un [Issue](https://github.com/Doriogamer/DownloaderMD/issues)

---

## 🤝 Contribuir

¡Las contribuciones son bienvenidas! Lee [CONTRIBUIR.md](CONTRIBUIR.md) para saber cómo:

- 🐛 Reportar bugs
- 💡 Sugerir mejoras
- 🔧 Hacer Pull Requests

---

## 📜 Licencia

Este proyecto está bajo la licencia **MIT**. Ver [LICENSE](LICENSE) para más detalles.

---

## 🙋 Soporte

¿Tienes problemas o preguntas?

- 📖 Lee la [documentación](https://github.com/Doriogamer/DownloaderMD/wiki)
- 🐛 Abre un [Issue](https://github.com/Doriogamer/DownloaderMD/issues)
- 💬 Revisa las [Discussions](https://github.com/Doriogamer/DownloaderMD/discussions)
- 📧 Contacta: dalvarezwallace2@gmail.com

---

## ⭐ Dale una estrella

Si DownloaderMD te sirvió, **dame una estrella** ⭐ en GitHub. ¡Te motiva a seguir mejorando!

---

## 🎯 Roadmap (Próximas versiones)

- [ ] Soporte para TikTok, Instagram, Twitter
- [ ] Descarga de playlists completas de YouTube
- [ ] Soporte para Linux y macOS
- [ ] Modo oscuro/claro configurable
- [ ] Historial de descargas
- [ ] Descargas múltiples simultáneas
- [ ] Conversión de formatos

---

## 📝 Changelog

Ver [CHANGELOG.md](CHANGELOG.md) para el historial de versiones.

---

## 👨‍💻 Autor

**Doriogamer** - [GitHub](https://github.com/Doriogamer)

Hecho con ❤️ en Python

---

**¡Gracias por usar DownloaderMD! 🎉**
