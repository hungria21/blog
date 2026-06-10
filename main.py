import os
import random
from telethon import TelegramClient, events, functions, types
from telethon.network import ConnectionTcpIntermediate
from tl_definitions import InputRichMessageMarkdown, SendMessageLayer227Request, register_layer_227_types
import config

# Configurações do Bot
API_ID = config.API_ID
API_HASH = config.API_HASH
BOT_TOKEN = config.BOT_TOKEN

# Registrar tipos do Layer 227 para evitar TypeNotFoundError ao ler respostas do servidor
register_layer_227_types()

# Melhorar estabilidade da conexão para ambientes mobile (Pydroid 3 / Termux)
client = TelegramClient(
    'rich_bot',
    API_ID,
    API_HASH,
    connection=ConnectionTcpIntermediate,
    device_model="Android Bot",
    system_version="Layer 227 Manager"
)

@client.on(events.NewMessage(pattern='/start'))
async def start_handler(event):
    await event.reply("Olá! Eu sou o Bot conversor de 'Rich Messages' (Layer 227).\n\n"
                      "Envie-me qualquer texto com formatação Markdown e eu o enviarei de volta "
                      "usando o novo sistema nativo do Telegram.\n\n"
                      "Exemplo:\n"
                      "# Título\n"
                      "| Tabela | Coluna |\n"
                      "| --- | --- |\n"
                      "| Linha 1 | Dado |")

@client.on(events.NewMessage)
async def rich_handler(event):
    if event.message.text.startswith('/'):
        return

    # Usando o novo request do Layer 227 com rich_message
    rich_msg = InputRichMessageMarkdown(markdown=event.message.text)

    try:
        # Envolvendo o request em InvokeWithLayer para garantir que o servidor entenda o Layer 227
        # e retorne objetos compatíveis (que registramos no início)
        await client(functions.InvokeWithLayerRequest(
            layer=227,
            query=SendMessageLayer227Request(
                peer=event.input_chat,
                message="", # O texto agora vai no rich_message
                random_id=random.getrandbits(63) - (1 << 63),
                rich_message=rich_msg
            )
        ))
    except Exception as e:
        # Se falhar, tentamos responder normalmente mas informamos o erro
        print(f"Erro: {e}")
        await event.reply(f"Ocorreu um erro ao processar a Rich Message: {str(e)}\n\n"
                          "Certifique-se de que o servidor suporta Layer 227.")

if __name__ == "__main__":
    print("Bot de Rich Messages iniciado...")
    client.start(bot_token=BOT_TOKEN)
    client.run_until_disconnected()
