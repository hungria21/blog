import logging
import json
import uuid
import re
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InlineQueryResultArticle
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters, InlineQueryHandler
import httpx

import config
from rich_builder import RichMessageBuilder

# Setup logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

builder = RichMessageBuilder()

async def send_rich_message(chat_id, rich_payload, bot_token):
    """Custom function to send rich message using raw HTTP request."""
    # Split if too many blocks
    payloads = builder.split_rich_payload(rich_payload)

    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    results = []
    async with httpx.AsyncClient() as client:
        for p in payloads:
            data = {
                "chat_id": chat_id,
                "rich_message": p
            }
            response = await client.post(url, json=data)
            results.append(response.json())
    return results[0] if results else {"ok": False}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler for the /start command."""
    welcome_md = (
        "# Bem-vindo ao Bot de Mensagens Ricas (API 10.1)!\n\n"
        "Eu converto GFM, rST, AsciiDoc e LaTeX em mensagens estruturadas.\n\n"
        "### Comandos Disponíveis:\n"
        "• `/gfm <texto>` - Força GitHub Flavored Markdown\n"
        "• `/rst <texto>` - Força reStructuredText\n"
        "• `/asciidoc <texto>` - Força AsciiDoc\n"
        "• `/latex <texto>` - Força LaTeX/Markdown\n\n"
        "Ou apenas envie o texto e eu tentarei detectar o formato!"
    )
    rich_payload = builder.build_payload(welcome_md)

    keyboard = [
        [InlineKeyboardButton("Guia Markdown", url="https://github.com/adam-p/markdown-here/wiki/markdown-cheatsheet")],
        [InlineKeyboardButton("Docs Telegram Rich", url="https://core.telegram.org/bots/api#rich-message-formatting-options")],
        [InlineKeyboardButton("MathJax", url="https://www.mathjax.org/")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await send_rich_message(update.effective_chat.id, rich_payload, context.bot.token)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler for user messages and syntax commands."""
    text = update.message.text
    if not text:
        return

    syntax = None
    if text.startswith('/'):
        parts = text.split(maxsplit=1)
        potential_cmd = parts[0][1:].lower()
        if potential_cmd in ['gfm', 'rst', 'asciidoc', 'latex', 'md']:
            syntax = potential_cmd
            if len(parts) > 1:
                text = parts[1]
            else:
                await update.message.reply_text(f"Envie o texto após o comando /{syntax}")
                return

    rich_payload = builder.build_payload(text, syntax=syntax)
    res = await send_rich_message(update.effective_chat.id, rich_payload, context.bot.token)
    if not res.get("ok"):
        await update.message.reply_text(f"Erro: {res.get('description')}")

async def inline_query(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler for inline queries."""
    query = update.inline_query.query
    if not query:
        return

    results = []

    # Template 1: Auto-detected
    rich_payload = builder.build_payload(query)
    results.append(
        InlineQueryResultArticle(
            id=str(uuid.uuid4()),
            title="✨ Formatação Rica Automática",
            description="Detecta e formata usando API 10.1.",
            input_message_content={
                "type": "inputMessageContentRichMessage",
                "rich_message": rich_payload
            }
        )
    )

    # Template 2: Code Block
    code_payload = builder.build_payload(f"```\n{query}\n```", syntax='gfm')
    results.append(
        InlineQueryResultArticle(
            id=str(uuid.uuid4()),
            title="💻 Bloco de Código",
            description="Formata como código pré-formatado.",
            input_message_content={
                "type": "inputMessageContentRichMessage",
                "rich_message": code_payload
            }
        )
    )

    # Template 3: Elegant Quote
    quote_payload = builder.build_payload(f"> {query}", syntax='gfm')
    results.append(
        InlineQueryResultArticle(
            id=str(uuid.uuid4()),
            title="💬 Citação Elegante",
            description="Formata como um bloco de citação.",
            input_message_content={
                "type": "inputMessageContentRichMessage",
                "rich_message": quote_payload
            }
        )
    )

    await update.inline_query.answer(results)

if __name__ == '__main__':
    if config.BOT_TOKEN == "YOUR_BOT_TOKEN_HERE":
        print("Please set your BOT_TOKEN in config.py.")
    else:
        application = ApplicationBuilder().token(config.BOT_TOKEN).build()

        # Command handlers for forced syntax
        for cmd in ['gfm', 'rst', 'asciidoc', 'latex', 'md']:
            application.add_handler(CommandHandler(cmd, handle_message))

        application.add_handler(CommandHandler('start', start))
        application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
        application.add_handler(InlineQueryHandler(inline_query))

        print("Bot is running...")
        application.run_polling()
