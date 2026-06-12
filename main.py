import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters, InlineQueryHandler
from telegram.constants import ParseMode
import config
from formatter import format_message, detect_format
from utils import escape_markdown_v2
from splitter import split_message
import uuid

# Setup logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler for the /start command."""
    welcome_text = (
        "Olá! Eu sou o Bot de Formatação Rica do Telegram.\n\n"
        "Envie-me qualquer texto (Markdown, rST, AsciiDoc, LaTeX) e eu o converterei "
        "para o formato rico nativo do Telegram.\n\n"
        "Você também pode forçar uma sintaxe usando comandos como /gfm, /rst, /asciidoc, /latex.\n\n"
        "Experimente o modo inline digitando @nomedobot <seu texto> em qualquer chat!"
    )

    keyboard = [
        [InlineKeyboardButton(name, url=url)] for name, url in config.SUPPORT_LINKS
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(welcome_text, reply_markup=reply_markup)

async def process_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler for normal text messages."""
    text = update.message.text
    if not text:
        return

    # Check if it's a command to force syntax
    command = None
    if text.startswith('/'):
        parts = text.split(maxsplit=1)
        potential_command = parts[0][1:].lower()
        if potential_command in ['gfm', 'rst', 'asciidoc', 'latex', 'md', 'commonmark']:
            command = potential_command
            if len(parts) > 1:
                text = parts[1]
            else:
                await update.message.reply_text(f"Por favor, envie o texto após o comando /{command}")
                return

    formatted = format_message(text, syntax=command)
    parts = split_message(formatted)

    try:
        for part in parts:
            await update.message.reply_text(
                part,
                parse_mode=ParseMode.MARKDOWN_V2
            )
    except Exception as e:
        logging.error(f"Error sending message: {e}")
        await update.message.reply_text(
            f"Erro ao formatar mensagem. Certifique-se de que a sintaxe está correta.\n\nErro: {escape_markdown_v2(str(e))}",
            parse_mode=ParseMode.MARKDOWN_V2
        )

async def inline_query(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler for inline queries."""
    query = update.inline_query.query
    if not query:
        return

    results = []

    # Auto-detect format for the query
    syntax = detect_format(query)
    formatted = format_message(query, syntax=syntax)

    # Suggestion 1: Detected/Standard Formatting
    results.append(
        InlineQueryResultArticle(
            id=str(uuid.uuid4()),
            title=f"Formatação {syntax.upper()}",
            description="Envia o texto formatado usando a sintaxe detectada.",
            input_message_content=InputTextMessageContent(
                formatted,
                parse_mode=ParseMode.MARKDOWN_V2
            )
        )
    )

    # Suggestion 2: Code Block
    code_formatted = f"```\n{escape_markdown_v2(query, is_code=True)}\n```"
    results.append(
        InlineQueryResultArticle(
            id=str(uuid.uuid4()),
            title="Bloco de Código",
            description="Envia o texto dentro de um bloco de código.",
            input_message_content=InputTextMessageContent(
                code_formatted,
                parse_mode=ParseMode.MARKDOWN_V2
            )
        )
    )

    # Content-based suggestions
    if "http" in query:
        # SlideShow Suggestion (using URLs)
        results.append(
            InlineQueryResultArticle(
                id=str(uuid.uuid4()),
                title="SlideShow",
                description="Formata URLs como um SlideShow.",
                input_message_content=InputTextMessageContent(
                    f"🎞️ *SlideShow*\n\n{formatted}",
                    parse_mode=ParseMode.MARKDOWN_V2
                )
            )
        )
        # Collage Suggestion
        results.append(
            InlineQueryResultArticle(
                id=str(uuid.uuid4()),
                title="Collage",
                description="Formata URLs como uma Colagem.",
                input_message_content=InputTextMessageContent(
                    f"🖼️ *Collage*\n\n{formatted}",
                    parse_mode=ParseMode.MARKDOWN_V2
                )
            )
        )
        # Link Preview Suggestion
        results.append(
            InlineQueryResultArticle(
                id=str(uuid.uuid4()),
                title="Link Preview",
                description="Envia o texto com pré-visualização de link.",
                input_message_content=InputTextMessageContent(
                    formatted,
                    parse_mode=ParseMode.MARKDOWN_V2,
                    disable_web_page_preview=False
                )
            )
        )

    # Elegant Quote
    results.append(
        InlineQueryResultArticle(
            id=str(uuid.uuid4()),
            title="Citação Elegante",
            description="Formata o texto como uma citação em bloco.",
            input_message_content=InputTextMessageContent(
                f">{formatted}",
                parse_mode=ParseMode.MARKDOWN_V2
            )
        )
    )

    await update.inline_query.answer(results)

if __name__ == '__main__':
    if config.BOT_TOKEN == "YOUR_BOT_TOKEN_HERE":
        print("Please set your BOT_TOKEN in config.py or as an environment variable.")
    else:
        application = ApplicationBuilder().token(config.BOT_TOKEN).build()

        start_handler = CommandHandler('start', start)
        application.add_handler(start_handler)

        # Handlers for forced syntax
        for cmd in ['gfm', 'rst', 'asciidoc', 'latex', 'md', 'commonmark']:
            application.add_handler(CommandHandler(cmd, process_text))

        # Default message handler
        application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), process_text))

        # Inline query handler
        application.add_handler(InlineQueryHandler(inline_query))

        application.run_polling()
