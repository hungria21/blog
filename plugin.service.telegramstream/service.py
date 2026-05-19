import os
import sys
import xbmc
import xbmcaddon
import xbmcvfs
import asyncio
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
import socket
import time

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
        if not self.client or not self.message or not self.loop:
            self.send_error(404)
            return

        self.send_response(200)
        self.send_header('Content-Type', 'video/mp4')
        self.end_headers()

        async def stream_task():
            async for chunk in self.client.iter_download(self.message.media):
                self.wfile.write(chunk)

        future = asyncio.run_coroutine_threadsafe(stream_task(), self.loop)
        try:
            future.result()
        except Exception as e:
            xbmc.log(f"TelegramStream: Streaming error: {str(e)}", xbmc.LOGERROR)

class TelegramService(xbmc.Monitor):
    def __init__(self):
        super(TelegramService, self).__init__()
        self.client = None
        self.loop = asyncio.new_event_loop()
        self.server = None
        self.port = self.find_free_port()
        self.client_thread = None
        self.update_settings()

    def find_free_port(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(('', 0))
        port = s.getsockname()[1]
        s.close()
        return port

    def update_settings(self):
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
            if self.client_thread and self.client_thread.is_alive():
                self.stop_client()
            self.client_thread = threading.Thread(target=self.run_loop)
            self.client_thread.start()

    def run_loop(self):
        asyncio.set_event_loop(self.loop)
        self.loop.run_until_complete(self.start_client())

    async def start_client(self):
        self.client = TelegramClient(session_file, self.api_id, self.api_hash)
        StreamHandler.client = self.client
        StreamHandler.loop = self.loop

        @self.client.on(events.NewMessage)
        async def handler(event):
            if self.authorized_id != 0 and event.sender_id != self.authorized_id:
                return

            if event.message.video or (event.message.document and event.message.document.mime_type.startswith('video/')):
                StreamHandler.message = event.message
                url = f"http://localhost:{self.port}/play.mp4"
                xbmc.executebuiltin(f"PlayMedia({url})")
                await event.reply("Streaming iniciado...")

            elif event.message.text:
                text = event.message.text
                if text.startswith('http'):
                    xbmc.executebuiltin(f"PlayMedia({text})")
                    await event.reply("Reproduzindo link...")

        await self.client.start(bot_token=self.bot_token)
        await self.client.run_until_disconnected()

    def start_server(self):
        self.server = HTTPServer(('localhost', self.port), StreamHandler)
        t = threading.Thread(target=self.server.serve_forever)
        t.daemon = True
        t.start()

    def stop_client(self):
        if self.client:
            self.loop.call_soon_threadsafe(lambda: asyncio.create_task(self.client.disconnect()))

    def onSettingsChanged(self):
        self.update_settings()

    def stop(self):
        if self.server:
            self.server.shutdown()
        self.stop_client()
        self.loop.call_soon_threadsafe(self.loop.stop)

service = TelegramService()
service.start_server()

while not service.abortRequested():
    if service.waitForAbort(1):
        break

service.stop()
