import yt_dlp as youtube_dl

def test_download():
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'test_download.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '320',
        }],
        'postprocessor_args': ['-ar', '44100'],
        'prefer_ffmpeg': True,
        'ffmpeg_location': 'C:/ffmpeg/bin',  # Cambia esto a la ruta correcta
    }

    url = 'https://www.youtube.com/watch?v=MhKD3ERzdlk'  # Prueba con un URL de YouTube
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

if __name__ == "__main__":
    test_download()
