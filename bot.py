from telethon import TelegramClient, events, types, functions
import config
from formatter import RichFormatter
from tl_definitions import (
    InputRichMessageHtml,
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
    # Usar HTML por padrão agora que temos InputRichMessageHtml
    rich_msg = formatter.to_rich_message(text)
    try:
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
        # Fallback para mensagem normal se falhar
        await client.send_message(peer, text, buttons=reply_markup, parse_mode='html')

@client.on(events.NewMessage(pattern='/start'))
async def start_handler(event):
    welcome_html = formatter.format_welcome_message()
    await send_rich_message(event.input_chat, welcome_html)

@client.on(events.NewMessage(pattern='/sintaxe'))
async def syntax_handler(event):
    catalog = formatter.get_syntax_catalog()
    rows = []
    row = []
    # Limitando a exibição no menu, mas o bot processa qualquer entrada
    for name, url in list(catalog.items())[:20]:
        row.append(types.KeyboardButtonUrl(name, url))
        if len(row) == 2:
            rows.append(types.KeyboardButtonRow(row))
            row = []
    if row:
        rows.append(types.KeyboardButtonRow(row))

    await client.send_message(
        event.input_chat,
        "<b>Catálogo de Sintaxes Suportadas:</b>\n(Exibindo as principais)",
        buttons=rows,
        parse_mode='html'
    )

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
        # Sugestões iniciais de templates
        results = [
            builder.article(
                "Template Slideshow",
                text="<tg-slideshow>\n<img src='https://telegram.org/img/t_logo.png'/>\n<img src='https://telegram.org/img/t_logo.png'/>\n<figcaption>Exemplo de Slideshow</figcaption>\n</tg-slideshow>",
                description="Cria um carrossel de imagens rico",
                parse_mode='html'
            ),
            builder.article(
                "Template Colagem",
                text="<tg-collage>\n<img src='https://telegram.org/img/t_logo.png'/>\n<img src='https://telegram.org/img/t_logo.png'/>\n<figcaption>Exemplo de Colagem</figcaption>\n</tg-collage>",
                description="Cria uma grade de imagens rica",
                parse_mode='html'
            )
        ]
    elif re.match(r'https?://\S+', query):
        # Reconhecimento de links para sugerir mídia rica
        results = [
            builder.article(
                "Visualizar como Slideshow",
                text=f"<tg-slideshow>\n<img src='{query}'/>\n<figcaption>Link visualizado como Slide</figcaption>\n</tg-slideshow>",
                description="Envolve o link em um carrossel rico",
                parse_mode='html'
            ),
            builder.article(
                "Visualizar como Colagem",
                text=f"<tg-collage>\n<img src='{query}'/>\n<figcaption>Link visualizado como Colagem</figcaption>\n</tg-collage>",
                description="Envolve o link em uma grade rica",
                parse_mode='html'
            )
        ]
    else:
        # Formatação genérica
        results = [
            builder.article(
                "Formatar como Rich Message",
                text=formatter.to_rich_html(query),
                description="Envia o texto formatado como Rich HTML",
                parse_mode='html'
            )
        ]

    try:
        # Tentar enviar via SetInlineBotResults rico se possível
        await client(functions.InvokeWithLayerRequest(
            layer=227,
            query=SetInlineBotResultsLayer227Request(
                query_id=event.id,
                results=results,
                cache_time=0
            )
        ))
    except Exception as e:
        print(f"Erro no inline rico: {e}")
        await event.answer(results)

if __name__ == '__main__':
    print("Bot iniciado com suporte a Rich HTML...")
    client.start(bot_token=config.BOT_TOKEN)
    client.run_until_disconnected()
