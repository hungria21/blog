from telethon import TelegramClient, events
from telethon.tl.types import InputBotInlineResultArticle, InputWebDocument
import config
from rich_formatter import parse_rich_message
import logging

# Configuração de logs
logging.basicConfig(level=logging.INFO)

client = TelegramClient('rich_bot', config.API_ID, config.API_HASH)

@client.on(events.NewMessage(pattern='/start'))
async def start(event):
    welcome_text = (
        "Olá! Eu sou o Bot de Mensagens Ricas.\n\n"
        "Envie qualquer texto com formatação Markdown e eu responderei com a formatação aplicada.\n"
        "Também funciono via modo inline: basta digitar `@seu_bot_username texto` em qualquer chat.\n\n"
        "**Formatos Suportados:**\n"
        "- `**negrito**`, `*itálico*`, `~~riscado~~`, `__sublinhado__`, `||spoiler||`\n"
        "- `[link](url)`\n"
        "- `> Citação` (normal)\n"
        "- `>> Citação Expandível` (oculta por padrão)\n"
        "- `$$formula_latex$$` (renderizado via CodeCogs)\n"
        "- Blocos de código com diagramas:\n"
        "  ```mermaid\n"
        "  graph TD; A-->B;\n"
        "  ```\n"
        "  (Suporta: mermaid, plantuml, graphviz, etc.)"
    )
    # Parse welcome text too
    clean_text, entities = parse_rich_message(welcome_text)
    await event.respond(clean_text, formatting_entities=entities)

@client.on(events.NewMessage)
async def handle_message(event):
    if event.text.startswith('/'):
        return

    try:
        clean_text, entities = parse_rich_message(event.text)
        await event.respond(clean_text, formatting_entities=entities)
    except Exception as e:
        await event.respond(f"Erro ao processar mensagem: {str(e)}")

@client.on(events.InlineQuery)
async def handler(event):
    if not event.text:
        return

    try:
        clean_text, entities = parse_rich_message(event.text)

        # O modo inline requer que enviemos um resultado.
        # Usaremos InputBotInlineResultArticle para enviar o texto formatado.
        result = event.builder.article(
            title="Enviar Mensagem Rica",
            description=clean_text[:50] + "...",
            text=clean_text,
            formatting_entities=entities
        )
        await event.answer([result])
    except Exception as e:
        logging.error(f"Erro no modo inline: {e}")

if __name__ == '__main__':
    print("Bot iniciado...")
    client.start(bot_token=config.BOT_TOKEN)
    client.run_until_disconnected()
