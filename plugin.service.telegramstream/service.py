import os
import sys
import xbmc
import xbmcaddon
import xbmcvfs
import asyncio
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
import socket
import re

# Add resources/lib to sys.path
addon = xbmcaddon.Addon()
lib_path = os.path.join(addon.getAddonInfo('path'), 'resources', 'lib')
sys.path.append(lib_path)

try:
    from telethon import TelegramClient, events
except ImportError:
    xbmc.log("TelegramStream: Telethon not found in " + lib_path, xbmc.LOGERROR)

# Profile directory for session file
profile_path = xbmcvfs.translatePath(addon.getAddonInfo('profile'))
if not os.path.exists(profile_path):
    os.makedirs(profile_path)
session_file = os.path.join(profile_path, 'telegram_stream')

class StreamHandler(BaseHTTPRequestHandler):
    client = None
    message = None
    loop = None

    def do_GET(self):
        if not self.client or not self.loop:
            self.send_error(503, "Service unavailable")
            return

        if not self.message:
            self.send_error(404, "No media selected")
            return

        try:
            media = self.message.media
            if hasattr(media, 'document'):
                file_size = media.document.size
                mime_type = media.document.mime_type
            elif hasattr(media, 'video'):
                file_size = media.video.size
                mime_type = media.video.mime_type
            else:
                self.send_error(400, "Invalid media type")
                return

            range_header = self.headers.get('Range')
            start_byte = 0
            end_byte = file_size - 1

            if range_header:
                match = re.search(r'bytes=(\d+)-(\d*)', range_header)
                if match:
                    start_byte = int(match.group(1))
                    if match.group(2):
                        end_byte = int(match.group(2))

                self.send_response(206)
                self.send_header('Content-Range', f'bytes {start_byte}-{end_byte}/{file_size}')
                content_length = end_byte - start_byte + 1
            else:
                self.send_response(200)
                content_length = file_size

            self.send_header('Content-Type', mime_type)
            self.send_header('Content-Length', str(content_length))
            self.send_header('Accept-Ranges', 'bytes')
            self.end_headers()

            if self.command == 'HEAD':
                return

            # Iterator to bridge async generator to sync thread
            async def get_next_chunk(aiter):
                try:
                    return await aiter.__anext__()
                except StopAsyncIteration:
                    return None

            # Telethon's iter_download supports offset and length
            aiter = self.client.iter_download(
                media,
                offset=start_byte,
                request_size=1024*1024 # 1MB chunks
            ).__aiter__()

            bytes_sent = 0
            while bytes_sent < content_length:
                future = asyncio.run_coroutine_threadsafe(get_next_chunk(aiter), self.loop)
                chunk = future.result()
                if chunk is None:
                    break

                # Truncate chunk if it goes beyond requested range
                if bytes_sent + len(chunk) > content_length:
                    chunk = chunk[:content_length - bytes_sent]

                try:
                    self.wfile.write(chunk)
                    bytes_sent += len(chunk)
                except Exception:
                    # Connection closed by client
                    break

        except Exception as e:
            xbmc.log(f"TelegramStream: Streaming error: {str(e)}", xbmc.LOGERROR)

class TelegramService(xbmc.Monitor):
    def __init__(self):
        super(TelegramService, self).__init__()
        self.client = None
        self.loop = asyncio.new_event_loop()
        self.server = None
        self.port = self.find_free_port()

        # Start the event loop thread
        self.loop_thread = threading.Thread(target=self._run_event_loop, daemon=True)
        self.loop_thread.start()

        # Start the HTTP server
        self.start_server()

        # Initial settings load and client start
        self.update_settings()

    def _run_event_loop(self):
        asyncio.set_event_loop(self.loop)
        self.loop.run_forever()

    def find_free_port(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(('', 0))
        port = s.getsockname()[1]
        s.close()
        return port

    def update_settings(self):
        xbmc.log("TelegramStream: Updating settings...", xbmc.LOGINFO)
        try:
            self.api_id = int(addon.getSetting('api_id') or 0)
        except ValueError:
            self.api_id = 0
        self.api_hash = addon.getSetting('api_hash')
        self.bot_token = addon.getSetting('bot_token')
        try:
            self.authorized_id = int(addon.getSetting('authorized_user_id') or 0)
        except ValueError:
            self.authorized_id = 0

        if self.api_id and self.api_hash and self.bot_token:
            asyncio.run_coroutine_threadsafe(self.restart_client(), self.loop)
        else:
            xbmc.log("TelegramStream: Missing credentials in settings.", xbmc.LOGWARNING)

    async def restart_client(self):
        if self.client:
            xbmc.log("TelegramStream: Disconnecting previous client...", xbmc.LOGINFO)
            await self.client.disconnect()
            self.client = None

        xbmc.log("TelegramStream: Starting Telethon client...", xbmc.LOGINFO)
        try:
            self.client = TelegramClient(session_file, self.api_id, self.api_hash)
            StreamHandler.client = self.client
            StreamHandler.loop = self.loop

            @self.client.on(events.NewMessage)
            async def handler(event):
                if self.authorized_id != 0 and event.sender_id != self.authorized_id:
                    return

                text = (event.message.text or "").strip().lower()

                if text.startswith('/start'):
                    await event.reply("Bem-vindo ao Telegram Stream para Kodi!\n\nEnvie um vídeo ou arquivo de vídeo para reproduzir automaticamente.\n\nComandos:\n/start - Iniciar\n/stream - Continuar reprodução\n/pause - Pausar reprodução")

                elif text.startswith('/pause'):
                    xbmc.executebuiltin("PlayerControl(Pause)")
                    await event.reply("Comando de pause enviado ao Kodi.")

                elif text.startswith('/stream'):
                    # Check if something is playing and paused
                    if xbmc.getCondVisibility("Player.Paused"):
                        xbmc.executebuiltin("PlayerControl(Play)")
                        await event.reply("Retomando reprodução no Kodi.")
                    elif not xbmc.getCondVisibility("Player.HasMedia"):
                        await event.reply("Nada para reproduzir no momento.")
                    else:
                        await event.reply("O vídeo já está sendo reproduzido.")

                elif event.message.video or (event.message.document and event.message.document.mime_type and event.message.document.mime_type.startswith('video/')):
                    StreamHandler.message = event.message
                    url = f"http://localhost:{self.port}/play.mp4"
                    xbmc.log(f"TelegramStream: Starting playback of {url}", xbmc.LOGINFO)
                    xbmc.executebuiltin(f"PlayMedia({url})")
                    await event.reply("Recebido! Iniciando a reprodução no Kodi...")

                elif text.startswith('http'):
                    xbmc.executebuiltin(f"PlayMedia({text})")
                    await event.reply("Reproduzindo link no Kodi...")

            await self.client.start(bot_token=self.bot_token)
            xbmc.log("TelegramStream: Client started successfully.", xbmc.LOGINFO)
        except Exception as e:
            xbmc.log(f"TelegramStream: Error starting client: {str(e)}", xbmc.LOGERROR)

    def start_server(self):
        self.server = HTTPServer(('localhost', self.port), StreamHandler)
        t = threading.Thread(target=self.server.serve_forever, daemon=True)
        t.start()
        xbmc.log(f"TelegramStream: Local server started on port {self.port}", xbmc.LOGINFO)

    def onSettingsChanged(self):
        self.update_settings()

    def stop(self):
        xbmc.log("TelegramStream: Stopping service...", xbmc.LOGINFO)
        if self.server:
            self.server.shutdown()

        # Disconnect client and stop loop
        if self.client:
            asyncio.run_coroutine_threadsafe(self.client.disconnect(), self.loop)

        self.loop.call_soon_threadsafe(self.loop.stop)

service = TelegramService()

# Main loop to keep the service running
while not service.abortRequested():
    if service.waitForAbort(1):
        break

service.stop()
