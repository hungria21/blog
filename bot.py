import os
import asyncio
from telethon import TelegramClient, events
from pymediainfo import MediaInfo

# Remember to replace these with your own values
API_ID = os.environ.get('API_ID')
API_HASH = os.environ.get('API_HASH')
BOT_TOKEN = os.environ.get('BOT_TOKEN')

# We need to use a session file to save the bot's state
SESSION_FILE = 'bot.session'

# Create the client and connect
client = TelegramClient(SESSION_FILE, API_ID, API_HASH)


def format_duration(milliseconds):
    """Formats duration from milliseconds to HH:MM:SS."""
    if milliseconds is None:
        return "N/A"
    try:
        seconds = int(milliseconds) // 1000
    except (ValueError, TypeError):
        return "N/A"
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f'{hours:02}:{minutes:02}:{seconds:02}'


@client.on(events.NewMessage(pattern='/start'))
async def start(event):
    """Send a message when the command /start is issued."""
    await event.respond('Olá! Envie-me um arquivo de vídeo (.mp4 ou .mkv) para que eu possa extrair os metadados.')
    raise events.StopPropagation


@client.on(events.NewMessage(func=lambda e: e.file and e.file.mime_type in ('video/mp4', 'video/x-matroska')))
async def get_media_metadata(event):
    """Handle incoming video files and extract metadata."""
    file_name = event.file.name

    # Inform the user
    response_msg = await event.respond(f'Baixando os primeiros 20MB de `{file_name}` para análise...')

    # Download only the first 20MB
    chunk_size = 20 * 1024 * 1024  # 20MB
    downloaded_file_path = f"partial_{file_name}"

    with open(downloaded_file_path, 'wb') as fd:
        async for chunk in client.iter_download(event.media, request_size=chunk_size):
            fd.write(chunk)
            break  # Stop after the first chunk

    await response_msg.edit('Analisando metadados...')

    try:
        media_info = MediaInfo.parse(downloaded_file_path)
        metadata = ""
        for track in media_info.tracks:
            if track.track_type == 'Video':
                metadata += f"**Vídeo:**\n"
                metadata += f"  - Qualidade: {track.height}p\n"
                metadata += f"  - Duração: {format_duration(track.duration)}\n"
                metadata += f"  - Codec: {track.codec_id}\n"
            elif track.track_type == 'Audio':
                metadata += f"**Áudio ({track.language or 'desconhecido'}):**\n"
                metadata += f"  - Idioma: {track.language or 'N/A'}\n"
                metadata += f"  - Codec: {track.format}\n"
            elif track.track_type == 'Text':
                metadata += f"**Legenda ({track.language or 'desconhecida'}):**\n"
                metadata += f"  - Idioma: {track.language or 'N/A'}\n"
                metadata += f"  - Formato: {track.format}\n"

        if not metadata:
            await response_msg.edit("Não foi possível extrair metadados do arquivo.")
        else:
            await response_msg.edit(metadata, parse_mode='md')

    except Exception as e:
        await response_msg.edit(f"Ocorreu um erro ao analisar o arquivo: {e}")
    finally:
        # Clean up the downloaded file
        if os.path.exists(downloaded_file_path):
            os.remove(downloaded_file_path)

    raise events.StopPropagation


async def main():
    """Main function to start the bot."""
    # Connect to Telegram
    await client.start(bot_token=BOT_TOKEN)
    print("Bot started!")
    await client.run_until_disconnected()


if __name__ == '__main__':
    # It's recommended to run the bot in an asyncio event loop
    asyncio.run(main())
