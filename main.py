import random
from pyrogram import Client, filters, raw
from tl_definitions import InputRichMessageMarkdown, SendMessageLayer227
import config

# Inicializa o cliente PyroTGFork
app = Client(
    "rich_bot",
    api_id=config.API_ID,
    api_hash=config.API_HASH,
    bot_token=config.BOT_TOKEN
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
        # Envolvendo em InvokeWithLayer para garantir o processamento correto pelo servidor
        await client.invoke(
            raw.functions.InvokeWithLayer(
                layer=227,
                query=SendMessageLayer227(
                    peer=peer,
                    message="", # Texto visual vai no rich_message
                    random_id=random.getrandbits(63) - (1 << 63),
                    rich_message=rich_markdown
                )
            )
        )
    except Exception as e:
        print(f"Erro ao enviar Rich Message: {e}")
        # Fallback para mensagem normal se falhar (ex: servidor não suporta)
        try:
            await message.reply(message.text)
        except:
            pass

if __name__ == "__main__":
    print("Bot PyroTGFork iniciado no Layer 227...")
    app.run()
