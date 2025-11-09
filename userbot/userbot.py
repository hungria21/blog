"""
Telegram Userbot usando Telethon
Estrutura modular com sistema de plugins
"""

import os
import sys
import time
import logging
from pathlib import Path
from datetime import datetime
from telethon import TelegramClient, events
from telethon.errors import FloodWaitError, SlowModeWaitError
import asyncio

# Configuração de logging
logging.basicConfig(
    format='[%(levelname)s] %(asctime)s - %(message)s',
    level=logging.INFO,
    handlers=[
        logging.FileHandler('userbot.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Configurações do bot
class Config:
    API_ID = int(os.getenv("API_ID", "0"))
    API_HASH = os.getenv("API_HASH", "")
    STRING_SESSION = os.getenv("STRING_SESSION", "")

    if API_ID == 0 or not API_HASH:
        logger.warning("API_ID ou API_HASH não encontrados no .env. Solicitando interativamente.")
        try:
            API_ID = int(input("Digite seu API_ID: "))
            API_HASH = input("Digite seu API_HASH: ")
        except ValueError:
            logger.error("API_ID deve ser um número inteiro.")
            sys.exit(1)

    # Diretórios
    DOWNLOAD_PATH = "./downloads"
    PLUGINS_PATH = "./plugins"

    # Prefixo de comandos
    CMD_PREFIX = "."

    # Anti-flood settings
    FLOOD_WAIT_TIME = 5  # segundos entre mensagens
    MAX_RETRIES = 3

# Estatísticas globais
class Stats:
    def __init__(self):
        self.start_time = datetime.now()
        self.commands_executed = 0
        self.messages_sent = 0
        self.files_downloaded = 0
        self.errors = 0

    def get_uptime(self):
        delta = datetime.now() - self.start_time
        days = delta.days
        hours, remainder = divmod(delta.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{days}d {hours}h {minutes}m {seconds}s"

# Inicializar estatísticas
stats = Stats()

# Criar diretórios necessários
Path(Config.DOWNLOAD_PATH).mkdir(exist_ok=True)
Path(Config.PLUGINS_PATH).mkdir(exist_ok=True)

# Inicializar cliente
if Config.STRING_SESSION:
    bot = TelegramClient(
        'userbot_session',
        Config.API_ID,
        Config.API_HASH
    ).start(session=Config.STRING_SESSION)
else:
    bot = TelegramClient(
        'userbot_session',
        Config.API_ID,
        Config.API_HASH
    )

# Função auxiliar para evitar flood
async def safe_send(event, message, **kwargs):
    """Enviar mensagem com proteção anti-flood"""
    for attempt in range(Config.MAX_RETRIES):
        try:
            await asyncio.sleep(Config.FLOOD_WAIT_TIME)
            msg = await event.respond(message, **kwargs)
            stats.messages_sent += 1
            return msg
        except FloodWaitError as e:
            logger.warning(f"FloodWait: aguardando {e.seconds}s")
            await asyncio.sleep(e.seconds)
        except SlowModeWaitError as e:
            logger.warning(f"SlowMode: aguardando {e.seconds}s")
            await asyncio.sleep(e.seconds)
        except Exception as e:
            logger.error(f"Erro ao enviar mensagem: {e}")
            stats.errors += 1
            if attempt == Config.MAX_RETRIES - 1:
                raise
    return None

async def safe_edit(message, text, **kwargs):
    """Editar mensagem com proteção anti-flood"""
    try:
        await asyncio.sleep(1)
        await message.edit(text, **kwargs)
        return True
    except Exception as e:
        logger.error(f"Erro ao editar mensagem: {e}")
        stats.errors += 1
        return False

# Comando básico: alive
@bot.on(events.NewMessage(outgoing=True, pattern=r'^\.alive$'))
async def alive_handler(event):
    """Verifica se o bot está online"""
    stats.commands_executed += 1

    me = await bot.get_me()
    uptime = stats.get_uptime()

    message = f"""
╔══════════════════════╗
║   🤖 **USERBOT ATIVO**   ║
╚══════════════════════╝

👤 **Usuário:** {me.first_name}
📱 **Telefone:** +{me.phone if me.phone else 'N/A'}
⏱️ **Uptime:** {uptime}
📊 **Comandos:** {stats.commands_executed}
💬 **Mensagens:** {stats.messages_sent}
📥 **Downloads:** {stats.files_downloaded}
❌ **Erros:** {stats.errors}

✅ Sistema operacional normalmente
"""

    await safe_edit(event, message.strip())

# Comando: ping
@bot.on(events.NewMessage(outgoing=True, pattern=r'^\.ping$'))
async def ping_handler(event):
    """Mede a latência do bot"""
    stats.commands_executed += 1

    start = time.time()
    msg = await event.edit("🏓 Pong!")
    end = time.time()

    latency = (end - start) * 1000
    await safe_edit(msg, f"🏓 **Pong!**\n⚡ Latência: `{latency:.2f}ms`")

# Comando: stats
@bot.on(events.NewMessage(outgoing=True, pattern=r'^\.stats$'))
async def stats_handler(event):
    """Exibe estatísticas detalhadas"""
    stats.commands_executed += 1

    uptime = stats.get_uptime()

    message = f"""
📊 **ESTATÍSTICAS DO USERBOT**

⏱️ **Tempo Online:** {uptime}
⚡ **Comandos Executados:** {stats.commands_executed}
💬 **Mensagens Enviadas:** {stats.messages_sent}
📥 **Arquivos Baixados:** {stats.files_downloaded}
❌ **Erros Registrados:** {stats.errors}

📅 **Iniciado em:** {stats.start_time.strftime('%d/%m/%Y %H:%M:%S')}
"""

    await safe_edit(event, message.strip())

# Comando: help
@bot.on(events.NewMessage(outgoing=True, pattern=r'^\.help$'))
async def help_handler(event):
    """Lista todos os comandos disponíveis"""
    stats.commands_executed += 1

    help_text = """
📚 **COMANDOS DISPONÍVEIS**

**Comandos Básicos:**
• `.alive` - Verifica status do bot
• `.ping` - Mede latência
• `.stats` - Estatísticas detalhadas
• `.help` - Esta mensagem

**Downloads:**
• `.ytdl <url>` - Download de vídeos/áudio (YouTube, etc)
• `.gdl <url>` - Download de galerias (Instagram, Twitter, etc)

**Informações:**
• Prefixo: `.`
• Anti-flood: Ativo
• Auto-retry: 3 tentativas
"""

    await safe_edit(event, help_text.strip())

# Carregador de plugins
def load_plugins():
    """Carrega todos os plugins da pasta plugins/"""
    plugin_path = Path(Config.PLUGINS_PATH)

    if not plugin_path.exists():
        logger.warning(f"Diretório de plugins não encontrado: {Config.PLUGINS_PATH}")
        return

    plugins_loaded = 0
    for plugin_file in plugin_path.glob("*.py"):
        if plugin_file.name.startswith("_"):
            continue

        try:
            plugin_name = plugin_file.stem
            spec = __import__(f"plugins.{plugin_name}", fromlist=[""])

            if hasattr(spec, 'setup'):
                spec.setup(bot, Config, stats, safe_send, safe_edit)

            plugins_loaded += 1
            logger.info(f"Plugin carregado: {plugin_name}")
        except Exception as e:
            logger.error(f"Erro ao carregar plugin {plugin_file.name}: {e}")
            stats.errors += 1

    logger.info(f"Total de plugins carregados: {plugins_loaded}")

# Inicialização
async def main():
    """Função principal"""
    logger.info("Iniciando Telegram Userbot...")

    # Conectar
    await bot.start()

    me = await bot.get_me()
    logger.info(f"Userbot iniciado como: {me.first_name} (@{me.username})")

    # Carregar plugins
    load_plugins()

    logger.info("Userbot está pronto! Use .help para ver os comandos.")
    logger.info("Pressione Ctrl+C para parar.")

    # Manter rodando
    await bot.run_until_disconnected()

if __name__ == "__main__":
    try:
        bot.loop.run_until_complete(main())
    except KeyboardInterrupt:
        logger.info("Userbot encerrado pelo usuário")
    except Exception as e:
        logger.error(f"Erro fatal: {e}")
        stats.errors += 1
    finally:
        logger.info(f"Estatísticas finais: {stats.commands_executed} comandos, {stats.messages_sent} mensagens")