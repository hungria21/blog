import os
from dotenv import load_dotenv

load_dotenv()

API_ID = int(os.getenv("API_ID", 0))
API_HASH = os.getenv("API_HASH", "")
SESSION_NAME = os.getenv("SESSION_NAME", "userbot")
COMMAND_PREFIX = os.getenv("COMMAND_PREFIX", ".")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
MAX_DOWNLOAD_SIZE = int(os.getenv("MAX_DOWNLOAD_SIZE", 2000000000))
DOWNLOADS_PATH = os.getenv("DOWNLOADS_PATH", "/data/data/com.termux/files/home/userbot/downloads")
