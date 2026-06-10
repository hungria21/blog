import os
import random
from telethon import TelegramClient, events
from tl_definitions import InputRichMessageMarkdown, SendMessageLayer227Request

# Configurações do Bot (Substitua pelos seus valores ou use variáveis de ambiente)
API_ID = int(os.environ.get('TG_API_ID', '12345'))
API_HASH = os.environ.get('TG_API_HASH', 'your_api_hash')
BOT_TOKEN = os.environ.get('TG_BOT_TOKEN', 'your_bot_token')

client = TelegramClient('rich_bot', API_ID, API_HASH)

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
        # Usamos o cliente para enviar o request manual
        await client(SendMessageLayer227Request(
            peer=event.input_chat,
            message="", # O texto agora vai no rich_message
            random_id=random.getrandbits(63) - (1 << 63), # Garante que cabe em um long assinado de 8 bytes
            rich_message=rich_msg
        ))
    except Exception as e:
        await event.reply(f"Ocorreu um erro ao processar a Rich Message: {str(e)}\n\n"
                          "Certifique-se de que o servidor suporta Layer 227.")

if __name__ == "__main__":
    print("Bot de Rich Messages iniciado...")
    client.start(bot_token=BOT_TOKEN)
    client.run_until_disconnected()
