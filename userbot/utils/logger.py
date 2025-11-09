# coding: utf-8
import logging
from logging.handlers import RotatingFileHandler
import os
from userbot.config import LOG_LEVEL

def setup_logger():
    """Configura um logger customizado com rotação de arquivos."""

    # Garante que o diretório de logs exista
    if not os.path.exists("userbot/logs"):
        os.makedirs("userbot/logs")

    # Formato do log
    log_format = logging.Formatter(
        "[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # Logger principal
    logger = logging.getLogger("Userbot")
    logger.setLevel(getattr(logging, LOG_LEVEL.upper(), logging.INFO))

    # Handler para console
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(log_format)
    logger.addHandler(console_handler)

    # Handler para arquivo com rotação
    file_handler = RotatingFileHandler(
        "userbot/logs/userbot.log",
        maxBytes=5 * 1024 * 1024,  # 5 MB
        backupCount=2,
        encoding='utf-8'
    )
    file_handler.setFormatter(log_format)
    logger.addHandler(file_handler)

    # Silencia o logger do Telethon para não poluir os logs
    logging.getLogger("telethon").setLevel(logging.WARNING)

    return logger

# Instância global do logger
logger = setup_logger()
