import os
import random
import config
from telethon import TelegramClient, events, functions, types
from telethon.network import ConnectionTcpIntermediate
from tl_definitions import InputRichMessageMarkdown, SendMessageLayer227Request, register_layer_227_types

# Registrar tipos do Layer 227 para evitar TypeNotFoundError
register_layer_227_types()

# Configurações do Bot
client = TelegramClient(
    'rich_bot',
    config.API_ID,
    config.API_HASH,
    connection=ConnectionTcpIntermediate,
    device_model="Android Bot",
    system_version="Layer 227 Manager"
)

# Definir o layer globalmente no cliente
client.api_version = 227

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
    # Proteção: Se a mensagem recebida já for processada pelo nosso stub vazio
    # ou se for um comando, ignoramos.
    if not event.message or not hasattr(event.message, 'text') or event.message.text.startswith('/'):
        return

    # Usando o novo request do Layer 227 com rich_message
    rich_msg = InputRichMessageMarkdown(markdown=event.message.text)

    try:
        # Enviamos o request diretamente.
        # O Telethon usará client.api_version para o handshake inicial.
        await client(SendMessageLayer227Request(
            peer=event.input_chat,
            message="", # O conteúdo visual vai no rich_message
            random_id=random.getrandbits(63) - (1 << 63),
            rich_message=rich_msg
        ))
    except Exception as e:
        print(f"Erro no processamento: {e}")
        # Falha silenciosa para evitar loop infinito de erros se o stub falhar
        pass

if __name__ == "__main__":
    print("Bot de Rich Messages iniciado...")
    client.start(bot_token=config.BOT_TOKEN)
    client.run_until_disconnected()
