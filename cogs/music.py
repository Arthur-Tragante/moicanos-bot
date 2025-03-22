import discord
from discord.ext import commands
import yt_dlp as youtube_dl
import asyncio
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import re
import logging
from config import (
    SPOTIFY_CLIENT_ID, 
    SPOTIFY_CLIENT_SECRET,
    YTDL_FORMAT_OPTIONS,
    FFMPEG_OPTIONS,
    SPOTIFY_TRACK_URL_REGEX,
    SPOTIFY_PLAYLIST_URL_REGEX,
    SPOTIFY_ALBUM_URL_REGEX
)

logger = logging.getLogger('musicbot.music')

class YTDLSource(discord.PCMVolumeTransformer):
    """Audio source for yt-dlp extracted content"""
    
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)
        self.data = data
        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        ytdl = youtube_dl.YoutubeDL(YTDL_FORMAT_OPTIONS)
        
        if not url.startswith('http'):
            url = f"ytsearch:{url}"
        
        try:
            data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))
            
            if data is None:
                raise Exception("Não foi possível obter informações do vídeo.")
            
            if 'entries' in data:
                data = data['entries'][0]
            
            filename = data['url'] if stream else ytdl.prepare_filename(data)
            return cls(discord.FFmpegPCMAudio(filename, **FFMPEG_OPTIONS), data=data)
        except Exception as e:
            logger.error(f"Erro ao extrair informações: {str(e)}")
            if "uploader id" in str(e):
                search_url = f"ytsearch:{url}"
                data = await loop.run_in_executor(None, lambda: ytdl.extract_info(search_url, download=not stream))
                if 'entries' in data:
                    data = data['entries'][0]
                filename = data['url'] if stream else ytdl.prepare_filename(data)
                return cls(discord.FFmpegPCMAudio(filename, **FFMPEG_OPTIONS), data=data)
            raise e

class MusicQueue:
    """Music queue manager for each server"""
    
    def __init__(self):
        self.queue = []
        self.current = None
        self.playing = False
        self.loop = asyncio.get_event_loop()
    
    def add_to_queue(self, item):
        self.queue.append(item)
    
    def clear_queue(self):
        self.queue.clear()
    
    def get_next(self):
        if len(self.queue) > 0:
            return self.queue.pop(0)
        return None
    
    def is_empty(self):
        return len(self.queue) == 0

class Music(commands.Cog):
    """Music commands and functionality"""
    
    def __init__(self, bot):
        self.bot = bot
        self.music_queues = {}
        try:
            auth_manager = SpotifyClientCredentials(
                client_id=SPOTIFY_CLIENT_ID,
                client_secret=SPOTIFY_CLIENT_SECRET
            )
            self.sp = spotipy.Spotify(auth_manager=auth_manager)
        except Exception as e:
            logger.warning(f"Spotify credentials not set up properly: {e}")
            self.sp = None
    
    def get_queue(self, guild_id):
        """Get or create queue for a guild"""
        if guild_id not in self.music_queues:
            self.music_queues[guild_id] = MusicQueue()
        return self.music_queues[guild_id]
    
    async def play_next(self, ctx):
        """Play the next song in the queue"""
        guild_id = ctx.guild.id
        queue = self.get_queue(guild_id)
        
        if queue.is_empty():
            queue.playing = False
            return
        
        queue.playing = True
        next_item = queue.get_next()
        
        async with ctx.typing():
            try:
                player = await YTDLSource.from_url(next_item, loop=self.bot.loop, stream=True)
                ctx.voice_client.play(
                    player, 
                    after=lambda e: self.bot.loop.create_task(self.handle_playback_finish(ctx, e))
                )
                await ctx.send(f'🎵 Tocando agora: {player.title}')
            except Exception as e:
                logger.error(f"Erro ao reproduzir música: {e}")
                await ctx.send(f'Erro ao reproduzir música: {str(e)}')
                await self.play_next(ctx)
    
    async def handle_playback_finish(self, ctx, error):
        """Handle when a song finishes playing"""
        if error:
            logger.error(f'Player error: {error}')
        await self.play_next(ctx)
    
    def is_spotify_url(self, url):
        """Check if URL is from Spotify"""
        return (re.match(SPOTIFY_TRACK_URL_REGEX, url) or 
                re.match(SPOTIFY_PLAYLIST_URL_REGEX, url) or 
                re.match(SPOTIFY_ALBUM_URL_REGEX, url))
    
    async def get_spotify_track_info(self, url):
        """Get track info from Spotify URL"""
        if not self.sp:
            return None, "Erro: Credenciais do Spotify não configuradas."
        
        match = re.match(SPOTIFY_TRACK_URL_REGEX, url)
        if match:
            try:
                track_id = match.group(1)
                track_info = self.sp.track(track_id)
                
                artist = track_info['artists'][0]['name']
                title = track_info['name']
                search_query = f"{artist} - {title}"
                
                return search_query, None
            except Exception as e:
                return None, f"Erro ao processar track do Spotify: {str(e)}"
        return None, "URL de track do Spotify inválida."
    
    async def get_spotify_playlist_tracks(self, url, limit=10):
        """Get tracks from Spotify playlist"""
        if not self.sp:
            return [], "Erro: Credenciais do Spotify não configuradas."
        
        match = re.match(SPOTIFY_PLAYLIST_URL_REGEX, url)
        if match:
            try:
                playlist_id = match.group(1)
                tracks = []
                results = self.sp.playlist_tracks(playlist_id, limit=limit)
                
                for item in results['items']:
                    if 'track' in item and item['track']:
                        track = item['track']
                        artist = track['artists'][0]['name']
                        title = track['name']
                        search_query = f"{artist} - {title}"
                        tracks.append(search_query)
                
                return tracks, None
            except Exception as e:
                return [], f"Erro ao processar playlist do Spotify: {str(e)}"
        return [], "URL de playlist do Spotify inválida."
    
    async def get_spotify_album_tracks(self, url, limit=10):
        """Get tracks from Spotify album"""
        if not self.sp:
            return [], "Erro: Credenciais do Spotify não configuradas."
        
        match = re.match(SPOTIFY_ALBUM_URL_REGEX, url)
        if match:
            try:
                album_id = match.group(1)
                tracks = []
                results = self.sp.album_tracks(album_id, limit=limit)
                
                for track in results['items']:
                    artist = track['artists'][0]['name']
                    title = track['name']
                    search_query = f"{artist} - {title}"
                    tracks.append(search_query)
                
                return tracks, None
            except Exception as e:
                return [], f"Erro ao processar álbum do Spotify: {str(e)}"
        return [], "URL de álbum do Spotify inválida."
    
    @commands.command(name='join', help='Connect the bot to a voice channel')
    async def join(self, ctx):
        """Join command to connect to the user's voice channel"""
        if not ctx.message.author.voice:
            await ctx.send('Você não está conectado a um canal de voz!')
            return
        
        channel = ctx.message.author.voice.channel
        await channel.connect()
        await ctx.send(f"Conectado ao canal {channel.name}")
    
    @commands.command(name='leave', help='Disconnect from the voice channel')
    async def leave(self, ctx):
        """Leave command to disconnect from voice and clear queue"""
        voice_client = ctx.message.guild.voice_client
        if voice_client and voice_client.is_connected():
            guild_id = ctx.guild.id
            queue = self.get_queue(guild_id)
            queue.clear_queue()
            
            await voice_client.disconnect()
            await ctx.send("Desconectado do canal de voz.")
        else:
            await ctx.send("O bot não está conectado a um canal de voz.")
    
    @commands.command(name='play', help='Play music from YouTube or Spotify')
    async def play(self, ctx, *, url):
        """Play command to add songs to queue and start playback"""
        if not ctx.message.guild.voice_client:
            await self.join(ctx)
        
        guild_id = ctx.guild.id
        queue = self.get_queue(guild_id)
        
        if self.is_spotify_url(url):
            await ctx.send(f"🔍 Processando conteúdo do Spotify...")
            
            if re.match(SPOTIFY_TRACK_URL_REGEX, url):
                search_query, error = await self.get_spotify_track_info(url)
                if error:
                    await ctx.send(error)
                    return
                
                await ctx.send(f"🎵 Adicionado à fila: {search_query}")
                queue.add_to_queue(search_query)
                
                if not queue.playing:
                    await self.play_next(ctx)
                    
            elif re.match(SPOTIFY_PLAYLIST_URL_REGEX, url):
                tracks, error = await self.get_spotify_playlist_tracks(url)
                if error:
                    await ctx.send(error)
                    return
                
                if not tracks:
                    await ctx.send("Não foi possível encontrar faixas na playlist.")
                    return
                
                for track in tracks:
                    queue.add_to_queue(track)
                
                await ctx.send(f"🎵 Adicionadas {len(tracks)} músicas da playlist à fila")
                
                if not queue.playing:
                    await self.play_next(ctx)
                    
            elif re.match(SPOTIFY_ALBUM_URL_REGEX, url):
                tracks, error = await self.get_spotify_album_tracks(url)
                if error:
                    await ctx.send(error)
                    return
                
                if not tracks:
                    await ctx.send("Não foi possível encontrar faixas no álbum.")
                    return
                
                for track in tracks:
                    queue.add_to_queue(track)
                
                await ctx.send(f"🎵 Adicionadas {len(tracks)} músicas do álbum à fila")
                
                if not queue.playing:
                    await self.play_next(ctx)
                    
        else:
            queue.add_to_queue(url)
            await ctx.send(f"🎵 Adicionado à fila: {url}")
            
            if not queue.playing:
                await self.play_next(ctx)
    
    @commands.command(name='queue', help='Display the current queue')
    async def show_queue(self, ctx):
        """Show the current music queue"""
        guild_id = ctx.guild.id
        queue = self.get_queue(guild_id)
        
        if queue.is_empty():
            await ctx.send("📋 A fila de reprodução está vazia.")
            return
        
        queue_list = "\n".join([f"{i+1}. {item}" for i, item in enumerate(queue.queue)])
        await ctx.send(f"📋 **Fila de reprodução:**\n{queue_list}")
    
    @commands.command(name='skip', help='Skip to the next song')
    async def skip(self, ctx):
        """Skip the current song"""
        if not ctx.voice_client or not ctx.voice_client.is_playing():
            await ctx.send("Não há música tocando para pular.")
            return
        
        ctx.voice_client.stop()
        await ctx.send("⏭️ Pulando para a próxima música...")
    
    @commands.command(name='clear', help='Clear the music queue')
    async def clear(self, ctx):
        """Clear the entire music queue"""
        guild_id = ctx.guild.id
        queue = self.get_queue(guild_id)
        
        queue.clear_queue()
        await ctx.send("🧹 Fila de reprodução limpa.")
    
    @commands.command(name='pause', help='Pause the current song')
    async def pause(self, ctx):
        """Pause the current playback"""
        if ctx.voice_client and ctx.voice_client.is_playing():
            ctx.voice_client.pause()
            await ctx.send("Música pausada.")
        else:
            await ctx.send("Não há música tocando.")
    
    @commands.command(name='resume', help='Resume the paused song')
    async def resume(self, ctx):
        """Resume paused playback"""
        if ctx.voice_client and ctx.voice_client.is_paused():
            ctx.voice_client.resume()
            await ctx.send("Música resumida.")
        else:
            await ctx.send("Não há música pausada.")
    
    @commands.command(name='stop', help='Stop the music and clear the queue')
    async def stop(self, ctx):
        """Stop playback and clear queue"""
        guild_id = ctx.guild.id
        queue = self.get_queue(guild_id)
        
        if ctx.voice_client and ctx.voice_client.is_playing():
            ctx.voice_client.stop()
            queue.clear_queue()
            queue.playing = False
            await ctx.send("⏹️ Reprodução parada e fila limpa.")
        else:
            await ctx.send("Não há música tocando.")

async def setup(bot):
    await bot.add_cog(Music(bot))
