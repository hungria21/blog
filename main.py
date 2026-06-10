import random
import pyrogram
import logging
from pyrogram import Client, filters
from tl_definitions import InputRichMessageMarkdown, SendMessageLayer227, register_layer_227_types
import config

# Configuração de Logs
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bot_activity.log', mode='a', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Forçar o layer globalmente no PyroTGFork antes de iniciar qualquer conexão
pyrogram.raw.all.layer = 227
register_layer_227_types()

# Inicializa o cliente
app = Client(
    "rich_bot",
    api_id=config.API_ID,
    api_hash=config.API_HASH,
    bot_token=config.BOT_TOKEN,
    device_model="Android Bot",
    system_version="Layer 227 Manager"
)

@app.on_message(filters.command("start") & filters.private)
async def start(client, message):
    logger.info(f"Usuário {message.from_user.id} enviou /start")
    await message.reply(
        "Olá! Sou o conversor MTProto Rich Message (Layer 227).\n\n"
        "Envie qualquer texto Markdown (GFM) e eu converterei nativamente.\n"
        "Suporta: **Negrito**, *Itálico*, ||Spoilers||, `Code`, Tables e LaTeX ($x^2$)."
    )

@app.on_message(filters.private & ~filters.command("start"))
async def handle_rich(client, message):
    if not message.text:
        return

    logger.info(f"Formatando mensagem para o usuário {message.from_user.id}")

    # Converte o texto recebido em um objeto InputRichMessageMarkdown
    rich_markdown = InputRichMessageMarkdown(markdown=message.text)

    # Resolve o peer
    try:
        peer = await client.resolve_peer(message.chat.id)
    except Exception as e:
        logger.error(f"Erro ao resolver peer: {e}")
        return

    try:
        # Envia usando o request customizado para Layer 227
        await client.invoke(
            SendMessageLayer227(
                peer=peer,
                message="", # Texto visual vai no rich_message
                random_id=random.getrandbits(63) - (1 << 63),
                rich_message=rich_markdown
            )
        )
        logger.info(f"Sucesso ao enviar Rich Message para {message.from_user.id}")
    except Exception as e:
        logger.error(f"Erro ao enviar Rich Message: {e}")
        # Fallback para mensagem normal se falhar
        try:
            await message.reply(message.text)
            logger.info("Enviado fallback (mensagem normal)")
        except Exception as fe:
            logger.error(f"Falha no fallback: {fe}")

if __name__ == "__main__":
    logger.info("Bot PyroTGFork iniciado nativamente no Layer 227...")
    app.run()
