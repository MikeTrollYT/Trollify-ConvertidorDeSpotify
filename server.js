const express = require('express');
const ytDlp = require('yt-dlp');
const axios = require('axios');
const qs = require('querystring');
const app = express();
const port = 3000;

// Configuración para Spotify (puedes usar las credenciales de Spotify como variables de entorno)
const CLIENT_ID = 'YOUR_SPOTIFY_CLIENT_ID';
const CLIENT_SECRET = 'YOUR_SPOTIFY_CLIENT_SECRET';

// Middleware para interpretar el cuerpo de la solicitud como JSON
app.use(express.json());

// Ruta para generar un código QR (por ejemplo, si quieres hacerlo para cada canción o playlist)
app.post('/generateQR', async (req, res) => {
    const { spotifyUrl } = req.body; // La URL de Spotify desde la web

    try {
        // Simular la obtención de la URL de YouTube para la canción
        const videoUrl = await searchYouTubeForSong(spotifyUrl);

        // Usar yt-dlp para descargar la canción
        await downloadSongFromYouTube(videoUrl);
        res.status(200).send("Canción descargada exitosamente");

    } catch (error) {
        console.error(error);
        res.status(500).send("Error al descargar la canción");
    }
});

// Función para buscar la canción en YouTube
async function searchYouTubeForSong(spotifyUrl) {
    // Aquí usaremos la API de Spotify para obtener la información de la canción
    const track = await getSpotifyTrack(spotifyUrl);
    const { name, artists } = track;

    // Usar yt-dlp para buscar en YouTube
    const query = `${name} ${artists[0].name}`;
    const result = await ytDlp.getInfo(`ytsearch:${query}`);

    return result.entries[0].url;
}

// Función para obtener información de la canción desde Spotify
async function getSpotifyTrack(url) {
    const response = await axios.get(`https://api.spotify.com/v1/me/top/artists`, {
        headers: {
            'Authorization': `Bearer YOUR_SPOTIFY_ACCESS_TOKEN`
        }
    });
    return response.data;
}

// Función para descargar la canción usando yt-dlp
async function downloadSongFromYouTube(url) {
    const options = {
        format: 'bestaudio/best',
        outtmpl: 'Descargas/%(title)s.%(ext)s',
        postprocessors: [{
            key: 'FFmpegExtractAudio',
            preferredcodec: 'mp3',
            preferredquality: '320',
        }],
    };

    // Descargar la canción
    await ytDlp.exec([url], options);
}

app.listen(port, () => {
    console.log(`Server is running at http://localhost:${port}`);
});
