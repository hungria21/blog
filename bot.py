from pyrogram import Client, filters, idle
from pyrogram.types import Message
from langdetect import detect, LangDetectException
import os
import asyncio

# Assuming config.py exists in the same directory with:
# api_id = 123456
# api_hash = "your_api_hash"
# bot_token = "your_bot_token"
try:
    from config import api_id, api_hash, bot_token
except ImportError:
    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    print("!!! ERRO: O arquivo 'config.py' não foi encontrado.         !!!")
    print("!!! Por favor, crie um arquivo config.py com as variáveis   !!!")
    print("!!! api_id, api_hash, e bot_token.                          !!!")
    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    exit(1)


# Dicionário de idiomas
LANGUAGES = {
    'en': 'Inglês',
    'pt': 'Português',
    'es': 'Espanhol',
    'fr': 'Francês',
    'de': 'Alemão',
    'it': 'Italiano',
    'ru': 'Russo',
    'ja': 'Japonês',
    'zh-cn': 'Chinês',
    'ar': 'Árabe',
    'hi': 'Hindi',
    'ko': 'Coreano',
    'tr': 'Turco',
    'nl': 'Holandês',
    'pl': 'Polonês'
}

def detect_language(text):
    """Detecta o idioma do texto usando langdetect"""
    if not text:
        return "Não detectado"

    try:
        lang_code = detect(text)
        return LANGUAGES.get(lang_code, f"Outro ({lang_code})")
    except LangDetectException:
        return "Não detectado"

def create_caption(bot_info):
    """Cria a caption da postagem"""
    caption = f"""**{bot_info['name']}**
━━━━━━━━━━
➧ **Username:** {bot_info['username']}
➧ **Idioma:** {bot_info['language']}
➧ **Grupo:** {bot_info['can_join_groups']}
➧ **Tags:** {bot_info['tags']}

ℹ️ **Descrição:**
{bot_info['description']}

━━━━━━━━━━
**Link:** {bot_info['link']}"""

    return caption

async def main():
    app = Client("bot_session", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

    async def get_bot_info(username):
        """Obtém informações completas do bot"""
        try:
            # Remover @ se existir
            username = username.replace('@', '')

            # Obter informações do bot
            user = await app.get_users(username)

            # Verificar se é realmente um bot
            if not user.is_bot:
                return None

            # Extrair informações básicas
            bot_name = user.first_name or "Sem nome"
            bot_username = f"@{user.username}" if user.username else "Sem username"
            bot_description = user.bio or "Sem descrição"
            bot_link = f"t.me/{user.username}" if user.username else "Sem link"

            can_join_groups = "Yes" if not getattr(user, 'bot_nochats', False) else "Not"
            supports_inline = getattr(user, 'bot_inline_placeholder', None) is not None
            tags = "#inline" if supports_inline else ""
            language = detect_language(bot_description)

            photo_path = None
            if user.photo:
                try:
                    photo_path = await app.download_media(user.photo.big_file_id, file_name="bot_photo.jpg")
                except Exception as e:
                    print(f"Erro ao baixar foto: {e}")

            return {
                'name': bot_name,
                'username': bot_username,
                'description': bot_description,
                'language': language,
                'link': bot_link,
                'photo': photo_path,
                'can_join_groups': can_join_groups,
                'tags': tags
            }
        except Exception as e:
            print(f"Erro ao obter informações do bot: {e}")
            return None

    @app.on_message(filters.text & ~filters.command(['start', 'help']))
    async def post_bot(client: Client, message: Message):
        """Cria postagem ao receber username do bot"""
        try:
            bot_username = message.text.strip()

            if not bot_username or len(bot_username) < 2:
                return

            processing_msg = await message.reply("🔍 Buscando informações do bot...")

            bot_info = await get_bot_info(bot_username)

            if not bot_info:
                await processing_msg.edit("❌ Bot não encontrado ou não é um bot válido.")
                return

            caption = create_caption(bot_info)
            await processing_msg.delete()

            if bot_info['photo'] and os.path.exists(bot_info['photo']):
                await message.reply_photo(photo=bot_info['photo'], caption=caption)
                os.remove(bot_info['photo'])
            else:
                await message.reply(caption)

        except Exception as e:
            print(f"Erro no handler post_bot: {e}")
            try:
                await message.reply(f"❌ Erro ao processar: {str(e)}")
            except:
                pass

    @app.on_message(filters.command('start'))
    async def start(client: Client, message: Message):
        """Comando de início"""
        await message.reply(
            "👋 **Bem-vindo!**\n\n"
            "Envie o username de um bot para gerar a postagem.\n"
            "Exemplo: `@BotFather` ou `BotFather`"
        )

    @app.on_message(filters.command('help'))
    async def help_command(client: Client, message: Message):
        """Comando de ajuda"""
        help_text = """📖 **Como usar:**

1️⃣ Envie o username de qualquer bot
2️⃣ O bot irá buscar as informações
3️⃣ Receberá uma postagem formatada com:
   • Nome e username
   • Idioma da descrição
   • Se funciona em grupos
   • Se suporta modo inline
   • Descrição completa
   • Foto de perfil (se disponível)

**Exemplos:**
• `@BotFather`
• `album_makerBot`
• `@vote`

💡 **Comandos:**
/start - Iniciar o bot
/help - Mostrar esta ajuda"""

        await message.reply(help_text)

    await app.start()
    print("🤖 Bot iniciado com sucesso!")
    print("⏳ Aguardando comandos...")
    await idle()
    await app.stop()

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("\n👋 Bot encerrado!")
