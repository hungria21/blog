import random
import pyrogram
from pyrogram import Client, filters, raw
from tl_definitions import InputRichMessageMarkdown, SendMessageLayer227
import config

# Forçar o layer globalmente no PyroTGFork antes de iniciar qualquer conexão
pyrogram.raw.all.layer = 227

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
    await message.reply(
        "Olá! Sou o conversor MTProto Rich Message (Layer 227).\n\n"
        "Envie qualquer texto Markdown (GFM) e eu converterei nativamente.\n"
        "Suporta: **Negrito**, *Itálico*, ||Spoilers||, `Code`, Tables e LaTeX ($x^2$)."
    )

@app.on_message(filters.private & ~filters.command("start"))
async def handle_rich(client, message):
    if not message.text:
        return

    # Converte o texto recebido em um objeto InputRichMessageMarkdown
    rich_markdown = InputRichMessageMarkdown(markdown=message.text)

    # Resolve o peer
    peer = await client.resolve_peer(message.chat.id)

    try:
        # Envia usando o request customizado para Layer 227
        # Como definimos pyrogram.raw.all.layer = 227, o handshake inicial
        # já usou este layer, então não precisamos de InvokeWithLayer manual aqui.
        await client.invoke(
            SendMessageLayer227(
                peer=peer,
                message="", # Texto visual vai no rich_message
                random_id=random.getrandbits(63) - (1 << 63),
                rich_message=rich_markdown
            )
        )
    except Exception as e:
        print(f"Erro ao enviar Rich Message: {e}")
        # Fallback simples
        try:
            await message.reply(message.text)
        except:
            pass

if __name__ == "__main__":
    print("Bot PyroTGFork iniciado nativamente no Layer 227...")
    app.run()
