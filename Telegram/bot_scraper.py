import re
import os
import asyncio
from telethon import events, types
from telethon.errors import FloodWaitError
from config import client

# ---------------------------------------------------------------------------
# Comando (funciona a partir de QUALQUER chat, o comando só precisa ser
# digitado pelo dono da conta, o "peer" da busca é sempre o @username alvo):
#
#   .bot @username termo
#   .bot @username + termo   (o "+" é opcional, só um separador visual)
#
# Não é necessário o userbot ser membro do canal/grupo: o Telethon resolve
# o @username publicamente (ResolveUsername) e a API do Telegram permite
# consultar/pesquisar mensagens de canais e grupos públicos sem estar
# inscrito neles.
#
# A busca usa o parâmetro "search" (equivalente a messages.search com
# q=termo no servidor do Telegram), que retorna só as mensagens que já
# contêm o termo — ou seja, não raspamos o chat inteiro, só o resultado
# da pesquisa.
#
# Em cada mensagem retornada, procuramos usernames nos formatos @username
# e t.me/username, e ao final enviamos um .txt com a lista de usernames
# únicos coletados.
# ---------------------------------------------------------------------------

# @username  (regra do Telegram: começa com letra, 5 a 32 caracteres no total)
MENTION_REGEX = re.compile(r'(?<![\w@])@([a-zA-Z][a-zA-Z0-9_]{4,31})')

# t.me/username  |  telegram.me/username  |  telegram.dog/username
TELEGRAM_DOMAINS = r'(?:https?://)?(?:t\.me|telegram\.me|telegram\.dog)'
LINK_USERNAME_REGEX = re.compile(
    rf'{TELEGRAM_DOMAINS}/(?!joinchat(?:/|$))(?!\+)([a-zA-Z][a-zA-Z0-9_]{{4,31}})',
    re.IGNORECASE
)

DB_FILE = "usernames_database.txt"
PAGE_LIMIT = 100     # mensagens por página
MAX_PAGES = 2000        # limite de segurança (evita loop infinito em chats gigantes)

COMMAND_REGEX = re.compile(r'\.bot\s+(@?\S+)\s*\+?\s*(.+)', re.IGNORECASE)


def extract_usernames(text: str) -> set[str]:
    found = set()
    if not text:
        return found
    for m in MENTION_REGEX.finditer(text):
        username = m.group(1).lower()
        if username.endswith("bot"):
            found.add(f"@{username}")
    for m in LINK_USERNAME_REGEX.finditer(text):
        username = m.group(1).lower()
        if username.endswith("bot"):
            found.add(f"@{username}")
    return found


# Handler registrado direto na importação do módulo — este main.py só faz
# exec_module nos arquivos de plugins/, ele NÃO chama nenhum setup(client).
# Por isso o "client" precisa ser o mesmo objeto global importado de config.py.
@client.on(events.NewMessage(pattern=COMMAND_REGEX))
async def bot_search_handler(event):
    if not event.out:
        return

    alvo = event.pattern_match.group(1)
    termo = event.pattern_match.group(2)
    if not alvo or not termo:
        await event.edit("uso: .bot @username termo")
        return

    alvo = alvo.strip()
    termo = termo.strip()

    await event.edit(f"canal: {alvo}\ntermo: {termo}\nresolvendo...")

    # Resolve o @username publicamente, sem precisar ser membro do chat
    try:
        entity = await client.get_input_entity(alvo)
    except Exception as e:
        await event.edit(f"erro ao resolver {alvo}: {e}")
        return

    # Carrega banco de dados existente (evita repetir username já coletado antes)
    database: set[str] = set()
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r", encoding="utf-8") as f:
            database = {line.strip().lower() for line in f if line.strip()}

    collected: set[str] = set()
    total_messages = 0
    offset_id = 0
    page = 0

    while page < MAX_PAGES:
        page += 1
        try:
            # search=termo -> pesquisa feita no servidor (messages.search),
            # só traz mensagens que batem com o termo, não o chat inteiro
            messages = await client.get_messages(
                entity,
                limit=PAGE_LIMIT,
                offset_id=offset_id,
                search=termo
            )
        except FloodWaitError as e:
            await asyncio.sleep(e.seconds)
            continue
        except Exception as e:
            await event.edit(f"erro na busca: {e}")
            return

        if not messages:
            break

        for message in messages:
            total_messages += 1

            texts_to_scan = []
            if message.text:
                texts_to_scan.append(message.text)
            if message.reply_markup:
                try:
                    for row in message.reply_markup.rows:
                        for btn in row.buttons:
                            if hasattr(btn, "url") and btn.url:
                                texts_to_scan.append(btn.url)
                except AttributeError:
                    pass

            for txt in texts_to_scan:
                for username in extract_usernames(txt):
                    if username not in database and username not in collected:
                        collected.add(username)

            offset_id = message.id

        try:
            await event.edit(
                f"canal: {alvo}\n"
                f"termo: {termo}\n"
                f"mensagens verificadas: {total_messages}\n"
                f"usernames novos: {len(collected)}"
            )
        except FloodWaitError as e:
            await asyncio.sleep(e.seconds)

        if len(messages) < PAGE_LIMIT:
            break

        await asyncio.sleep(1)

    # --- Resultado final ---
    if not collected:
        await event.edit(
            f"canal: {alvo}\n"
            f"termo: {termo}\n"
            f"mensagens verificadas: {total_messages}\n"
            f"usernames novos: 0"
        )
        return

    temp_file = "usernames_encontrados.txt"
    with open(temp_file, "w", encoding="utf-8") as f:
        for username in sorted(collected):
            f.write(f"{username}\n")

    # Atualiza banco de dados persistente
    mode = "a" if os.path.exists(DB_FILE) else "w"
    with open(DB_FILE, mode, encoding="utf-8") as f:
        if mode == "a" and os.path.getsize(DB_FILE) > 0:
            with open(DB_FILE, "rb") as rb:
                rb.seek(-1, 2)
                if rb.read(1) != b"\n":
                    f.write("\n")
        f.write("\n".join(sorted(collected)) + "\n")

    caption = (
        f"canal: {alvo}\n"
        f"termo: {termo}\n"
        f"mensagens verificadas: {total_messages}\n"
        f"usernames coletados: {len(collected)}"
    )

    await client.send_file('me', temp_file, caption=caption)

    await event.edit(
        f"canal: {alvo}\n"
        f"termo: {termo}\n"
        f"mensagens verificadas: {total_messages}\n"
        f"usernames coletados: {len(collected)}\n"
        f"arquivo enviado."
    )

    if os.path.exists(temp_file):
        os.remove(temp_file)
