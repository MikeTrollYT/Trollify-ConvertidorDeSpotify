import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import yt_dlp as youtube_dl
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk
import requests
from io import BytesIO
import threading

# Leer credenciales desde el archivo
script_dir = os.path.dirname(os.path.abspath(__file__))  # Obtiene el directorio del script actual
credentials_path = os.path.join(script_dir, 'credentials.txt')  # Construye la ruta absoluta

with open(credentials_path, 'r') as file:
    CLIENT_ID = file.readline().strip()
    CLIENT_SECRET = file.readline().strip()

# Configuración de Spotify
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET))

# Variables globales
total_songs = 0
songs_downloaded = 0

def download_song(song_url):
    global total_songs, songs_downloaded
    try:
        total_songs = 1  # Solo una canción en este caso
        songs_downloaded = 0

        result = sp.track(song_url)
        song_name = result['name']
        artist_name = result['artists'][0]['name']
        video_url = search_youtube(f"{song_name} {artist_name}")

        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': f"Descargas/{song_name}.%(ext)s",
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '320',
            }],
            'postprocessor_args': ['-ar', '44100'],
            'prefer_ffmpeg': True,
            'ffmpeg_location': 'C:/ffmpeg/bin',
            'progress_hooks': [progress_hook]
        }

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])
            songs_downloaded += 1
            update_progress((songs_downloaded / total_songs) * 100)  # Actualizar progreso total

        show_completion_message("La descarga de la canción se ha completado exitosamente.")
    
    except Exception as e:
        progress_label.config(text=f"Error descargando la canción: {e}")

def download_playlist(playlist_url):
    global total_songs, songs_downloaded
    try:
        result = sp.playlist(playlist_url)
        playlist_name = result['name']
        songs = result['tracks']['items']
        total_songs = len(songs)
        songs_downloaded = 0
        os.makedirs('Descargas', exist_ok=True)

        for song in songs:
            song_url = song['track']['external_urls']['spotify']
            song_name = song['track']['name']
            artist_name = song['track']['artists'][0]['name']
            video_url = search_youtube(f"{song_name} {artist_name}")

            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': f"Descargas/{song_name}.%(ext)s",
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '320',
                }],
                'postprocessor_args': ['-ar', '44100'],
                'prefer_ffmpeg': True,
                'ffmpeg_location': 'C:/ffmpeg/bin',
                'progress_hooks': [progress_hook]
            }

            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download([video_url])
                songs_downloaded += 1
                # Calcular el progreso total
                percent = (songs_downloaded / total_songs) * 100
                update_progress(percent)

        show_completion_message(f"La descarga de la playlist '{playlist_name}' se ha completado exitosamente.")

    except Exception as e:
        progress_label.config(text=f"Error descargando la playlist: {e}")

def search_youtube(query):
    ydl_opts = {
        'quiet': True,
        'format': 'bestaudio/best',
        'noplaylist': True,
        'extract_flat': True
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(f"ytsearch:{query}", download=False)
        return info['entries'][0]['url']

def update_info(*args):
    url = url_entry.get()
    if url:
        if 'track' in url:
            show_track_info(url)
        elif 'playlist' in url:
            show_playlist_info(url)

def show_track_info(track_url):
    result = sp.track(track_url)
    song_name = result['name']
    artist_name = result['artists'][0]['name']
    duration = result['duration_ms'] // 1000
    minutes, seconds = divmod(duration, 60)
    duration_str = f"{minutes}m {seconds}s"
    image_url = result['album']['images'][0]['url']

    info_label.config(text=f"Title: {song_name}\nArtist: {artist_name}\nDuration: {duration_str}")

    # Mostrar la imagen
    try:
        response = requests.get(image_url)
        img_data = BytesIO(response.content)
        img = Image.open(img_data)
        img = img.resize((200, 200), Image.LANCZOS)  # Redimensionar imagen
        img = ImageTk.PhotoImage(img)
        image_label.config(image=img)
        image_label.image = img
    except Exception as e:
        image_label.config(text=f"No se pudo cargar la imagen: {e}")

def show_playlist_info(playlist_url):
    result = sp.playlist(playlist_url)
    playlist_name = result['name']
    owner_name = result['owner']['display_name']
    image_url = result['images'][0]['url']
    total_tracks = result['tracks']['total']
    duration_ms = sum(track['track']['duration_ms'] for track in result['tracks']['items'])
    duration = duration_ms // 1000
    minutes, seconds = divmod(duration, 60)
    duration_str = f"{minutes}m {seconds}s"

    info_label.config(text=f"Playlist: {playlist_name}\nOwner: {owner_name}\nTracks: {total_tracks}\nTotal Duration: {duration_str}")

    # Mostrar la imagen
    try:
        response = requests.get(image_url)
        img_data = BytesIO(response.content)
        img = Image.open(img_data)
        img = img.resize((200, 200), Image.LANCZOS)  # Redimensionar imagen
        img = ImageTk.PhotoImage(img)
        image_label.config(image=img)
        image_label.image = img
    except Exception as e:
        image_label.config(text=f"No se pudo cargar la imagen: {e}")

def update_progress(progress):
    progress_var.set(progress)
    root.update_idletasks()

def start_download():
    url = url_entry.get()
    if url:
        # Mostrar la barra de progreso y etiqueta de progreso solo cuando se inicia la descarga
        progress_bar.pack(pady=10)
        progress_label.pack(pady=5)
        # Ejecutar la descarga en un hilo separado
        download_thread = threading.Thread(target=download_in_background, args=(url,))
        download_thread.start()

def download_in_background(url):
    if 'playlist' in url:
        download_playlist(url)
    else:
        download_song(url)

def progress_hook(d):
    if d['status'] == 'downloading':
        # No actualizamos el progreso aquí para playlists
        pass

def show_completion_message(message):
    messagebox.showinfo("Descarga Completa", message)

# Configuración de la interfaz gráfica
root = tk.Tk()
root.title("Convertidor de Spotify")
root.geometry("650x600")
root.configure(bg="#181818")

# Crear y configurar el título
title_label = tk.Label(root, text="Trollify", font=("Helvetica", 24, "bold"), fg="#1DB954", bg="#181818")
title_label.pack(pady=20)  # Añadir espacio arriba y abajo

# Campo de entrada de URL
url_entry_frame = tk.Frame(root, bg="#282828")
url_entry_frame.pack(pady=20, padx=20, fill=tk.X)
url_entry = tk.Entry(url_entry_frame, font=("Helvetica", 12), relief=tk.FLAT, borderwidth=0, bg="#282828", fg="#ffffff")
url_entry.pack(padx=10, pady=5, fill=tk.X)

# Etiquetas de información
info_label = tk.Label(root, text="", bg="#181818", fg="#ffffff", font=("Helvetica", 12))
info_label.pack(pady=10)

image_label = tk.Label(root, bg="#181818")
image_label.pack(pady=10)

# Botón de descargar
button_frame = tk.Frame(root, bg="#181818")
button_frame.pack(pady=10)
download_button = tk.Button(button_frame, text="Descargar", command=start_download, font=("Helvetica", 12), bg="#1DB954", fg="#ffffff", relief=tk.FLAT, borderwidth=0)
download_button.pack(padx=10, pady=5)

# Barra de progreso (inicialmente oculta)
progress_frame = tk.Frame(root, bg="#181818")
progress_frame.pack(pady=10)
progress_var = tk.DoubleVar()
progress_bar = ttk.Progressbar(progress_frame, variable=progress_var, maximum=100, style='green.Horizontal.TProgressbar')
progress_label = tk.Label(progress_frame, text="", bg="#181818", fg="#ffffff", font=("Helvetica", 12))

# Estilo de la barra de progreso
style = ttk.Style()
style.configure('green.Horizontal.TProgressbar', foreground='#1DB954', background='#1DB954')

# Ocultar inicialmente la barra de progreso y la etiqueta de progreso
progress_bar.pack_forget()
progress_label.pack_forget()

url_entry.bind("<KeyRelease>", update_info)

root.mainloop()
