# Spotify Downloader

## Descripción

Este proyecto es una aplicación de escritorio que te permite descargar canciones y playlists de Spotify como archivos MP3 utilizando `spotipy` para obtener la información de las pistas y `yt-dlp` para descargar el audio desde YouTube.

## Características

- Descarga canciones individuales desde Spotify en formato MP3.
- Descarga playlists completas de Spotify.
- Interfaz gráfica amigable construida con `Tkinter`.
- Muestra información relevante sobre la canción o playlist seleccionada, como título, artista, duración y portada.
- Barra de progreso para visualizar el estado de la descarga.

## Requisitos

Para ejecutar este proyecto, necesitas tener instalados los siguientes componentes:

- Python 3.6 o superior
- Paquetes Python:
  - `spotipy`
  - `yt-dlp`
  - `Pillow`
  - `requests`
- [FFmpeg](https://ffmpeg.org/download.html) (asegúrate de que `ffmpeg` esté disponible en tu variable de entorno PATH).

## Instalación

1. Clona este repositorio:
   ```bash
   git clone https://github.com/tu-usuario/spotify-downloader.git
   cd spotify-downloader
