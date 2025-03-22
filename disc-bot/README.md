# Discord Music Bot

A feature-rich Discord music bot that can play music from YouTube and Spotify.

## Features

- Play music from YouTube URLs or search queries
- Support for Spotify tracks, playlists, and albums
- Queue management system
- Multi-server support
- Basic music controls (play, pause, resume, stop)
- OpenAPI/Swagger documentation for commands

## Requirements

- Python 3.8 or higher
- FFmpeg installed on your system
- Discord Bot Token
- (Optional) Spotify API credentials for Spotify functionality

## Installation

1. Clone this repository:
   ```
   git clone <repository-url>
   cd disc-bot
   ```

2. Install required Python packages:
   ```
   pip install -r requirements.txt
   ```

3. Install FFmpeg:
   - **Windows**: Download from [ffmpeg.org](https://ffmpeg.org/download.html) and add it to your PATH
   - **Linux (Debian/Ubuntu)**: `sudo apt install ffmpeg`
   - **macOS**: `brew install ffmpeg`

4. Configure your bot:
   - Create a `.env` file in the project root (see `.env.example`)
   - Add your Discord Bot Token and Spotify credentials to the `.env` file
   - Get your Discord Bot Token from [Discord Developer Portal](https://discord.com/developers/applications)
   - (Optional) Get Spotify API credentials from [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/)

## Configuration

In your `.env` file, add the following:
```
DISCORD_TOKEN=your_discord_token_here
SPOTIFY_CLIENT_ID=your_spotify_client_id_here
SPOTIFY_CLIENT_SECRET=your_spotify_client_secret_here
```

You can also customize other settings in `config.py` such as the command prefix.

## Usage

1. Start the bot:
   ```
   python main.py
   ```

2. Invite the bot to your server using the OAuth2 URL from Discord Developer Portal

3. Use the following commands:
   - `!join` - Connect to your voice channel
   - `!leave` - Disconnect from voice channel
   - `!play <url or search query>` - Play from YouTube URL or search
   - `!play <spotify url>` - Play from Spotify URL (track, playlist, album)
   - `!pause` - Pause current playback
   - `!resume` - Resume paused playback
   - `!stop` - Stop playback and clear queue
   - `!skip` - Skip to next song
   - `!queue` - Show current queue
   - `!clear` - Clear the queue
   - `!ping` - Check bot latency

## API Documentation (Swagger/OpenAPI)

The bot comes with a Swagger/OpenAPI documentation file that describes all commands as if they were API endpoints. This provides a clear and visual representation of the available commands.

To view the documentation:

1. Copy the contents of `commands_api.yaml`
2. Paste them into an online Swagger UI editor like [Swagger Editor](https://editor.swagger.io/)
3. The documentation will render in a user-friendly interface, showing all commands, parameters, and responses

Alternatively, you can use tools like [Redocly](https://redocly.github.io/redoc/) or [SwaggerHub](https://app.swaggerhub.com/) to render the documentation.

This API documentation serves as a helpful reference for understanding:
- All available commands
- Required parameters
- Possible responses
- Command categorization

## Discord Permissions

The bot requires these permissions:
- View Channels
- Send Messages
- Read Message History
- Connect to Voice Channels
- Speak in Voice Channels

## Troubleshooting

- **Bot doesn't join voice channel**: Make sure it has permission to join voice channels
- **No sound**: Check if FFmpeg is properly installed
- **Spotify doesn't work**: Verify your Spotify API credentials in the `.env` file
- **Bot disconnects**: This could be due to internet connection issues or Discord API limitations
- **Token errors**: Make sure your `.env` file is set up correctly and the token is valid

## Security

- The `.env` file contains sensitive information and is included in `.gitignore`
- Never commit your tokens or API keys to version control
- If you accidentally expose your Discord token, regenerate it immediately in the Discord Developer Portal

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details. 