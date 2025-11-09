# coding: utf-8
from telethon import events
from userbot import client
from userbot.config import COMMAND_PREFIX
from userbot.utils.decorators import handle_errors

# Dicionário de ajuda
HELP_COMMANDS = {
    "alive": {
        "usage": ".alive",
        "desc": "Verifica se o userbot está ativo e exibe informações do sistema."
    },
    "stats": {
        "usage": ".stats [reset]",
        "desc": "Exibe estatísticas de uso. O argumento 'reset' zera as estatísticas."
    },
    "ytdl": {
        "usage": ".ytdl <URL>",
        "desc": "Baixa um vídeo da URL especificada."
    },
    "ytaudio": {
        "usage": ".ytaudio <URL>",
        "desc": "Extrai e baixa o áudio da URL especificada."
    },
    "gallery": {
        "usage": ".gallery <URL>",
        "desc": "Baixa uma galeria de imagens/vídeos da URL especificada."
    },
    "help": {
        "usage": ".help [comando]",
        "desc": "Mostra esta mensagem de ajuda ou a ajuda de um comando específico."
    }
}

@client.on(events.NewMessage(pattern=f"^{COMMAND_PREFIX}help(?: (.*))?$", from_me=True))
@handle_errors
async def help_command(event):
    """Exibe a ajuda dos comandos."""

    plugin = event.pattern_match.group(1)

    if plugin and plugin in HELP_COMMANDS:
        # Ajuda de um comando específico
        command_info = HELP_COMMANDS[plugin]
        response = (
            f"**Ajuda do comando `.{plugin}`**\n\n"
            f"**Uso**: `{command_info['usage']}`\n"
            f"**Descrição**: {command_info['desc']}"
        )
    else:
        # Lista todos os comandos
        response = "**Comandos Disponíveis**\n-------------------\n"

        # Agrupa por categoria
        categories = {
            "Sistema": ["alive", "stats", "help"],
            "Downloads": ["ytdl", "ytaudio", "gallery"]
        }

        for category, commands in categories.items():
            response += f"\n**{category}**:\n"
            for cmd_name in commands:
                cmd_info = HELP_COMMANDS[cmd_name]
                response += f"`{cmd_info['usage']}` - {cmd_info['desc']}\n"

        response += "\nUse `.help <comando>` para obter mais detalhes."

    await event.edit(response)
