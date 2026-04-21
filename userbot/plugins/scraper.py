import re
import os
import asyncio
from telethon import events, functions, types
from telethon.errors import FloodWaitError

def setup(client):
    @client.on(events.NewMessage(pattern=r'\.search(?:\s+(.+))?'))
    async def search_handler(event):
        if not event.out:
            return

        chat_input = event.pattern_match.group(1)
        if not chat_input:
            await event.edit("Uso: .search [ID/Username]")
            return

        await event.edit(f"Buscando em: {chat_input}")

        try:
            entity = await event.client.get_input_entity(chat_input)
        except Exception as e:
            await event.edit(f"Erro: {e}")
            return

        # Obter contagem total de mensagens com links no servidor
        try:
            search_result = await event.client(functions.messages.SearchRequest(
                peer=entity,
                q='',
                filter=types.InputMessagesFilterUrl(),
                min_date=None,
                max_date=None,
                offset_id=0,
                add_offset=0,
                limit=1,
                max_id=0,
                min_id=0,
                hash=0
            ))
            total_on_server = getattr(search_result, 'count', 0)
        except Exception:
            total_on_server = "Indisponível"

        url_regex = re.compile(r'(?:t\.me\/|telegram\.me\/)[\w\d\_]+', re.IGNORECASE)

        db_file = "database.txt"
        database = set()
        if os.path.exists(db_file):
            with open(db_file, "r") as f:
                database = {line.strip() for line in f if line.strip()}

        total_messages = 0
        links_found = 0
        new_links = []

        offset_id = 0
        limit = 100

        while True:
            try:
                messages = await event.client.get_messages(
                    entity,
                    limit=limit,
                    offset_id=offset_id,
                    filter=types.InputMessagesFilterUrl()
                )

                if not messages:
                    break

                for message in messages:
                    total_messages += 1
                    if message.text:
                        found = url_regex.findall(message.text)
                        for link in found:
                            links_found += 1
                            if link not in database and link not in new_links:
                                new_links.append(link)
                    offset_id = message.id

                if total_messages % 100 == 0 or len(messages) < limit:
                    try:
                        await event.edit(
                            f"CANAL: {chat_input}\n"
                            f"Mensagens: {total_on_server}\n"
                            f"Processando mensagens: {total_messages}"
                        )
                    except FloodWaitError as e:
                        await asyncio.sleep(e.seconds)

                    await asyncio.sleep(1)

                if len(messages) < limit:
                    break

            except FloodWaitError as e:
                await asyncio.sleep(e.seconds)
                continue

        if not new_links:
            await event.edit(
                f"Busca finalizada\n"
                f"CANAL: {chat_input}\n"
                f"Lidas: {total_messages}\n"
                f"Novos: 0"
            )
            return

        temp_file = "novos_links.txt"
        with open(temp_file, "w") as f:
            f.write("\n".join(new_links))

        mode = "a" if os.path.exists(db_file) else "w"
        with open(db_file, mode) as f:
            if mode == "a" and os.path.getsize(db_file) > 0:
                with open(db_file, "rb") as rb:
                    rb.seek(-1, 2)
                    if rb.read(1) != b"\n":
                        f.write("\n")
            f.write("\n".join(new_links) + "\n")

        await event.client.send_file(
            'me',
            temp_file,
            caption=f"Links: {len(new_links)}\nChat: {chat_input}"
        )

        await event.edit(
            f"Busca finalizada\n"
            f"CANAL: {chat_input}\n"
            f"Novos: {len(new_links)}\n"
            f"Arquivo enviado para Mensagens Salvas"
        )

        if os.path.exists(temp_file):
            os.remove(temp_file)
