# coding: utf-8
import time
import platform
from telethon import events, __version__ as telethon_version
from telethon.tl.functions.users import GetFullUserRequest

from userbot import client
from userbot.config import COMMAND_PREFIX
from userbot.utils.decorators import handle_errors
from userbot.utils import db_manager

# --- Constantes ---
USERBOT_VERSION = "1.0.0"
START_TIME = time.time()

@client.on(events.NewMessage(pattern=f"^{COMMAND_PREFIX}alive$", from_me=True))
@handle_errors
async def alive(event):
    """Verifica se o userbot está ativo e exibe informações."""
    start_ping = time.time()
    await event.edit("`Calculando...`")
    end_ping = time.time()

    ping_ms = round((end_ping - start_ping) * 1000, 2)
    uptime_seconds = int(time.time() - START_TIME)

    # Formata o uptime
    days, rem = divmod(uptime_seconds, 86400)
    hours, rem = divmod(rem, 3600)
    minutes, seconds = divmod(rem, 60)
    uptime_str = ""
    if days:
        uptime_str += f"{days}d "
    if hours:
        uptime_str += f"{hours}h "
    if minutes:
        uptime_str += f"{minutes}m "
    uptime_str += f"{seconds}s"

    # Obtém informações do sistema
    python_version = platform.python_version()

    # Obtém informações do sistema
    python_version = platform.python_version()
    comandos_executados = db_manager.get_stat("comandos_executados")

    # Monta a mensagem de resposta
    response_message = (
        f"**Userbot Online**\n"
        "--------------\n"
        f"**Uptime**: `{uptime_str}`\n"
        f"**Comandos executados**: `{comandos_executados}`\n"
        f"**Ping**: `{ping_ms}ms`\n"
        f"**Versão**: `{USERBOT_VERSION}`\n"
        f"**Python**: `{python_version}`\n"
        f"**Telethon**: `{telethon_version}`\n"
    )

    await event.edit(response_message)
