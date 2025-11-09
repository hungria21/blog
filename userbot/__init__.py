from telethon import TelegramClient
from .config import API_ID, API_HASH, SESSION_NAME
from .utils.logger import logger

# Inicialização do cliente
client = TelegramClient(SESSION_NAME, API_ID, API_HASH)
