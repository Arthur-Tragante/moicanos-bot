# Discord Bot Configuration
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')

PREFIX = '!'

SPOTIFY_CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
SPOTIFY_CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')

YTDL_FORMAT_OPTIONS = {
    'format': 'bestaudio/best',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': False,
    'no_warnings': False,
    'default_search': 'auto',
    'source_address': '0.0.0.0',
    'cookiefile': 'cookies.txt',
    'extractor_args': {
        'youtube': {
            'nocheckcertificate': True,
            'no_verify': True,
        }
    },
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    'retries': 10,
    'fragment_retries': 10,
}

FFMPEG_OPTIONS = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options': '-vn'
}

SPOTIFY_TRACK_URL_REGEX = r'https://open\.spotify\.com/track/([a-zA-Z0-9]+)'
SPOTIFY_PLAYLIST_URL_REGEX = r'https://open\.spotify\.com/playlist/([a-zA-Z0-9]+)'
SPOTIFY_ALBUM_URL_REGEX = r'https://open\.spotify\.com/album/([a-zA-Z0-9]+)' 