from telethon import TelegramClient, events, types, functions
import config
from formatter import RichFormatter
from tl_definitions import (
    InputRichMessageMarkdown,
    SendMessageLayer227Request,
    InputBotInlineMessageRichMessage,
    SetInlineBotResultsLayer227Request
)
import asyncio
import re

# Inicializa o cliente Telethon
client = TelegramClient('rich_bot_session', config.API_ID, config.API_HASH)
formatter = RichFormatter()

async def send_rich_message(peer, text, reply_markup=None):
    rich_msg = formatter.to_rich_message(text)
    try:
        # Usando InvokeWithLayer para garantir que o servidor processe como Layer 227
        await client(functions.InvokeWithLayerRequest(
            layer=227,
            query=SendMessageLayer227Request(
                peer=peer,
                rich_message=rich_msg,
                reply_markup=reply_markup
            )
        ))
    except Exception as e:
        print(f"Erro ao enviar Rich Message: {e}")
        # Fallback para mensagem normal
        await client.send_message(peer, text, buttons=reply_markup, parse_mode='markdown')

@client.on(events.NewMessage(pattern='/start'))
async def start_handler(event):
    welcome_text = formatter.format_welcome_message()
    catalog = formatter.get_syntax_catalog()

    buttons = []
    row = []
    # Mostrando apenas alguns no botão para não sobrecarregar, mas o catálogo completo está no código
    for i, (name, url) in enumerate(list(catalog.items())[:10]):
        row.append(types.KeyboardButtonUrl(name, url))
        if len(row) == 2:
            buttons.append(row)
            row = []
    if row:
        buttons.append(row)

    await send_rich_message(event.input_chat, welcome_text, reply_markup=types.ReplyInlineMarkup(buttons))

@client.on(events.NewMessage(func=lambda e: not e.text.startswith('/')))
async def message_handler(event):
    if not event.text:
        return
    await send_rich_message(event.input_chat, event.text)

@client.on(events.InlineQuery)
async def inline_handler(event):
    query = event.text
    builder = event.builder
    results = []

    if not query:
        results = [
            builder.article(
                "Template Slideshow",
                text="Clique para criar um Slideshow",
                description="Usa o novo formato <tg-slideshow>",
                link_preview=False
            ),
            builder.article(
                "Template Colagem",
                text="Clique para criar uma Colagem",
                description="Usa o novo formato <tg-collage>",
                link_preview=False
            )
        ]
    elif re.match(r'https?://\S+', query):
        # Para links, sugerimos slideshow ou colagem
        results = [
            builder.article(
                "Visualizar como Slideshow",
                text=f"<tg-slideshow>\n{query}\n</tg-slideshow>",
                description="Adiciona o link em um slideshow rico"
            ),
            builder.article(
                "Visualizar como Colagem",
                text=f"<tg-collage>\n{query}\n</tg-collage>",
                description="Adiciona o link em uma colagem rica"
            )
        ]
    else:
        results = [
            builder.article(
                "Formatar como Rich Message",
                text=query,
                description="Envia o texto usando a nova formatação rica"
            )
        ]

    # Para usar Rich Message em Inline, precisaríamos de SetInlineBotResultsLayer227Request
    # No entanto, os resultados do Telethon Builder são objetos padrão.
    # Vamos tentar converter os resultados para usarem InputBotInlineMessageRichMessage

    final_results = []
    for r in results:
        # Aqui simulamos a conversão para o tipo rico se necessário
        # Por simplicidade, enviamos como estão, mas o bot poderia interceptar
        final_results.append(r)

    try:
        await client(functions.InvokeWithLayerRequest(
            layer=227,
            query=SetInlineBotResultsLayer227Request(
                query_id=event.id,
                results=final_results,
                cache_time=0
            )
        ))
    except Exception as e:
        print(f"Erro no inline rico: {e}")
        await event.answer(results)

if __name__ == '__main__':
    print("Bot iniciado...")
    client.start(bot_token=config.BOT_TOKEN)
    client.run_until_disconnected()
