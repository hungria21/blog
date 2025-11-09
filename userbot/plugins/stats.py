# coding: utf-8
import time
from telethon import events
from userbot import client
from userbot.config import COMMAND_PREFIX
from userbot.utils import db_manager
from userbot.utils.decorators import handle_errors

# --- Constantes ---
START_TIME = time.time()

@client.on(events.NewMessage(pattern=f"^{COMMAND_PREFIX}stats(?: (reset))?$", from_me=True))
@handle_errors
async def stats(event):
    """Exibe estatísticas de uso do userbot."""

    # Processa o subcomando 'reset'
    if event.pattern_match.group(1) == "reset":
        db_manager.reset_stats()
        await event.edit("`Estatísticas resetadas com sucesso!`")
        return

    # Inicia a coleta de dados
    await event.edit("`Coletando estatísticas...`")

    # Uptime
    uptime_seconds = int(time.time() - START_TIME)
    days, rem = divmod(uptime_seconds, 86400)
    hours, rem = divmod(rem, 3600)
    minutes, seconds = divmod(rem, 60)
    uptime_str = ""
    if days: uptime_str += f"{days}d "
    if hours: uptime_str += f"{hours}h "
    if minutes: uptime_str += f"{minutes}m "
    uptime_str += f"{seconds}s"

    # Estatísticas do banco de dados
    total_commands = db_manager.get_stat("comandos_executados")
    downloads = db_manager.get_stat("downloads_realizados")
    uploads = db_manager.get_stat("uploads_realizados")
    space_used_bytes = db_manager.get_stat("espaco_usado")

    # Formata o espaço usado
    if space_used_bytes > 1024 * 1024 * 1024:
        space_used_str = f"{space_used_bytes / (1024**3):.2f} GB"
    elif space_used_bytes > 1024 * 1024:
        space_used_str = f"{space_used_bytes / (1024**2):.2f} MB"
    else:
        space_used_str = f"{space_used_bytes / 1024:.2f} KB"

    # Comandos mais usados
    command_usage = db_manager.get_command_usage()
    top_commands_str = "\n".join([f"`{cmd}`: {count}x" for cmd, count in command_usage[:5]])

    # Monta a mensagem de resposta
    response_message = (
        f"**Estatísticas do Userbot**\n"
        "----------------------\n"
        f"**Tempo online**: `{uptime_str}`\n"
        f"**Total de comandos**: `{total_commands}`\n"
        f"**Downloads realizados**: `{downloads}`\n"
        f"**Uploads realizados**: `{uploads}`\n"
        f"**Espaço usado**: `{space_used_str}`\n\n"
        f"**Comandos mais usados**:\n{top_commands_str}"
    )

    await event.edit(response_message)

# Hook para registrar todos os comandos
@client.on(events.NewMessage(outgoing=True))
async def log_all_commands(event):
    if event.text.startswith(COMMAND_PREFIX):
        command = event.text.split(' ')[0]
        db_manager.log_command(command)
