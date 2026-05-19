import os
import sys
import xbmc
import xbmcaddon
import time

# Add resources/lib to sys.path to find bundled dependencies
addon = xbmcaddon.Addon()
lib_path = os.path.join(addon.getAddonInfo('path'), 'resources', 'lib')
sys.path.append(lib_path)

try:
    import telebot
except ImportError:
    xbmc.log("TelegramStream: telebot not found in " + lib_path, xbmc.LOGERROR)

class TelegramService(xbmc.Monitor):
    def __init__(self):
        super(TelegramService, self).__init__()
        self.player = xbmc.Player()
        self.bot = None
        self.token = ""
        self.authorized_id = 0
        self.update_settings()

    def update_settings(self):
        new_token = addon.getSetting('bot_token')
        try:
            self.authorized_id = int(addon.getSetting('authorized_user_id') or 0)
        except ValueError:
            self.authorized_id = 0

        if new_token != self.token:
            self.token = new_token
            if self.token:
                self.bot = telebot.TeleBot(self.token)
                self.setup_handlers()
            else:
                self.bot = None

    def is_authorized(self, user_id):
        if self.authorized_id == 0:
            xbmc.log(f"TelegramStream: Unauthorized attempt by {user_id}. No authorized_user_id set.", xbmc.LOGWARNING)
            return False
        if user_id != self.authorized_id:
            xbmc.log(f"TelegramStream: Unauthorized attempt by {user_id}. Expected {self.authorized_id}.", xbmc.LOGWARNING)
            return False
        return True

    def setup_handlers(self):
        @self.bot.message_handler(content_types=['video', 'document'])
        def handle_video(message):
            if not self.is_authorized(message.from_user.id):
                self.bot.reply_to(message, "Você não tem permissão para controlar este Kodi.")
                return

            file_id = None
            if message.content_type == 'video':
                file_id = message.video.file_id
            elif message.content_type == 'document' and message.document.mime_type.startswith('video/'):
                file_id = message.document.file_id

            if file_id:
                try:
                    file_info = self.bot.get_file(file_id)
                    # Note: Direct API links only work for files < 20MB
                    file_url = f"https://api.telegram.org/file/bot{self.token}/{file_info.file_path}"
                    self.play_url(file_url)
                    self.bot.reply_to(message, "Reproduzindo vídeo no Kodi...")
                except Exception as e:
                    xbmc.log(f"TelegramStream: Error getting file: {str(e)}", xbmc.LOGERROR)

        @self.bot.message_handler(func=lambda message: True)
        def handle_text(message):
            if not self.is_authorized(message.from_user.id):
                self.bot.reply_to(message, "Você não tem permissão para controlar este Kodi.")
                return

            text = message.text or ""
            if text.startswith('http://') or text.startswith('https://'):
                self.play_url(text)
                self.bot.reply_to(message, "Reproduzindo link no Kodi...")
            elif text.lower() == '/start' or text.lower() == '/id':
                self.bot.reply_to(message, f"Seu ID de usuário é: {message.from_user.id}. Configure-o no Kodi.")

    def play_url(self, url):
        xbmc.log(f"TelegramStream: Attempting to play {url}", xbmc.LOGINFO)
        self.player.play(url)

    def onSettingsChanged(self):
        xbmc.log("TelegramStream: Settings changed, updating...", xbmc.LOGINFO)
        self.update_settings()

service = TelegramService()

def run():
    xbmc.log("TelegramStream: Service starting", xbmc.LOGINFO)

    offset = 0
    while not service.abortRequested():
        if service.bot:
            try:
                updates = service.bot.get_updates(offset=offset, timeout=5)
                for update in updates:
                    service.bot.process_new_updates([update])
                    offset = update.update_id + 1
            except Exception as e:
                xbmc.log(f"TelegramStream: Error in bot loop: {str(e)}", xbmc.LOGERROR)
                time.sleep(5)
        else:
            # Check for settings periodically if bot is not configured
            if service.waitForAbort(10):
                break
            continue

        if service.waitForAbort(1):
            break

    xbmc.log("TelegramStream: Service stopping", xbmc.LOGINFO)

if __name__ == '__main__':
    run()
