import logging
import os
from telegram import Update, ReplyKeyboardRemove
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters, ConversationHandler
from config import TOKEN

# Define states for conversation
COLLECTING_PHOTOS = 1

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    instructions = (
        f"Olá {user.first_name}! Eu sou o Bot de Mensagens Ricas (API 10.1).\n\n"
        "Envie qualquer texto formatado em Markdown para eu converter em Rich Message.\n\n"
        "**Suporte:**\n"
        "- # Cabeçalhos\n"
        "- | Tabelas | Colunas |\n"
        "- $ LaTeX $ ou $$ Bloco LaTeX $$\n"
        "- [ ] Checklists\n\n"
        "**Comandos Especiais:**\n"
        "/slideshow - Inicia a criação de um slide show\n"
        "/colagem - Inicia a criação de uma colagem\n"
        "/exemplo - Mostra um exemplo de Rich Message complexa"
    )
    await update.message.reply_text(instructions)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = (
        "Como usar:\n"
        "1. Digite seu texto com syntax Markdown.\n"
        "2. O bot usará o método `sendRichMessage` para enviar o resultado.\n"
        "3. Para LaTeX, use $ para inline e $$ para blocos.\n"
        "4. Para tabelas, use a syntax padrão do GitHub Flavored Markdown."
    )
    await update.message.reply_text(help_text)

async def handle_rich_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    chat_id = update.effective_chat.id

    # Payload para sendRichMessage (API 10.1)
    payload = {
        "chat_id": chat_id,
        "rich_message": {
            "markdown": text,
            "rtl": False
        }
    }

    try:
        await context.bot.do_api_request(
            "sendRichMessage",
            parameters=payload
        )
    except Exception as e:
        await update.message.reply_text(f"Erro ao enviar Rich Message: {str(e)}")

async def start_media_collection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    cmd = update.message.text.split()[0].replace('/', '')
    context.user_data['mode'] = cmd # 'slideshow' or 'colagem'
    context.user_data['photos'] = []

    await update.message.reply_text(
        f"Modo {cmd.capitalize()} ativado!\n"
        "Envie até 10 fotos. Quando terminar, envie /done"
    )
    return COLLECTING_PHOTOS

async def collect_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    photo_id = update.message.photo[-1].file_id
    if 'photos' not in context.user_data:
        context.user_data['photos'] = []

    context.user_data['photos'].append(photo_id)
    count = len(context.user_data['photos'])

    await update.message.reply_text(f"Foto {count} recebida. Envie mais ou /done.")

    if count >= 10:
        return await finish_collection(update, context)
    return COLLECTING_PHOTOS

async def finish_collection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    photos = context.user_data.get('photos', [])
    mode = context.user_data.get('mode', 'slideshow')

    if not photos:
        await update.message.reply_text("Nenhuma foto enviada. Cancelando.")
        return ConversationHandler.END

    tag = "tg-slideshow" if mode == "slideshow" else "tg-collage"

    # Criar o HTML que referencia as fotos pelo índice attach://index
    photo_refs = "".join([f'<tg-attachment index="{i}"/>' for i in range(len(photos))])
    html = f"<b>{mode.capitalize()}</b><br/>\n<{tag}>{photo_refs}</{tag}>"

    payload = {
        "chat_id": update.effective_chat.id,
        "rich_message": {
            "html": html,
            "photos": photos,
            "rtl": False
        }
    }

    try:
        await context.bot.do_api_request("sendRichMessage", parameters=payload)
    except Exception as e:
        await update.message.reply_text(f"Erro ao gerar {mode}: {str(e)}")

    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Cancelado.", reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END

async def show_example(update: Update, context: ContextTypes.DEFAULT_TYPE):
    example_html = (
        "<h1>Exemplo de Rich Message</h1>"
        "<p>Aqui está uma tabela:</p>"
        "<table>"
        "<tr><th>Item</th><th>Valor</th></tr>"
        "<tr><td>Produto A</td><td>$100</td></tr>"
        "<tr><td>Produto B</td><td>$200</td></tr>"
        "</table>"
        "<p>Matemática (LaTeX):</p>"
        "<tg-math-block>\\int_0^\\infty e^{-x^2} dx = \\frac{\\sqrt{\\pi}}{2}</tg-math-block>"
        "<p>Checklist:</p>"
        "<ul>"
        "<li><tg-marked checked=\"true\"/> Item Concluído</li>"
        "<li><tg-marked checked=\"false\"/> Item Pendente</li>"
        "</ul>"
    )

    payload = {
        "chat_id": update.effective_chat.id,
        "rich_message": {
            "html": example_html,
            "rtl": False
        }
    }

    try:
        await context.bot.do_api_request("sendRichMessage", parameters=payload)
    except Exception as e:
        await update.message.reply_text(f"Erro no exemplo: {str(e)}")

def main():
    if not TOKEN:
        print("Erro: TOKEN não encontrado no ambiente ou .env")
        return

    application = ApplicationBuilder().token(TOKEN).build()

    start_handler = CommandHandler('start', start)
    help_handler = CommandHandler('help', help_command)

    conv_handler = ConversationHandler(
        entry_points=[
            CommandHandler('slideshow', start_media_collection),
            CommandHandler('colagem', start_media_collection)
        ],
        states={
            COLLECTING_PHOTOS: [
                MessageHandler(filters.PHOTO, collect_photo),
                CommandHandler('done', finish_collection)
            ],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    application.add_handler(start_handler)
    application.add_handler(help_handler)
    application.add_handler(CommandHandler('exemplo', show_example))
    application.add_handler(conv_handler)

    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_rich_text))

    print("Bot iniciado...")
    application.run_polling()

if __name__ == '__main__':
    main()
