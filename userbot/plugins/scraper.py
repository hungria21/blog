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
            await event.edit("Uso: `.search [ID/Username]`")
            return

        await event.edit(f"🔍 Iniciando busca em: {chat_input}")

        try:
            entity = await event.client.get_input_entity(chat_input)
        except Exception as e:
            await event.edit(f"❌ Erro ao encontrar chat: {e}")
            return

        url_regex = re.compile(r'(?:t\.me\/|telegram\.me\/)[\w\d\_]+', re.IGNORECASE)

        # Deduplicação
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
                            f"🔄 Processando...\n"
                            f"📩 Mensagens lidas: {total_messages}\n"
                            f"🔗 Links totais: {links_found}\n"
                            f"✨ Novos links: {len(new_links)}"
                        )
                    except FloodWaitError as e:
                        await asyncio.sleep(e.seconds)

                    await asyncio.sleep(1) # Delay inteligente

                if len(messages) < limit:
                    break

            except FloodWaitError as e:
                await asyncio.sleep(e.seconds)
                continue # Retenta a mesma requisição

        if not new_links:
            await event.edit(
                f"✅ Busca finalizada!\n"
                f"📩 Mensagens lidas: {total_messages}\n"
                f"🔗 Links totais: {links_found}\n"
                f"✨ Nenhum link novo encontrado."
            )
            return

        # Salvar novos links e enviar arquivo
        temp_file = "novos_links.txt"
        with open(temp_file, "w") as f:
            f.write("\n".join(new_links))

        # Atualizar database de forma segura
        mode = "a" if os.path.exists(db_file) else "w"
        with open(db_file, mode) as f:
            # Verifica se precisa de nova linha se o arquivo já existir e não terminar com uma
            if mode == "a":
                with open(db_file, "rb") as rb:
                    rb.seek(-1, 2)
                    if rb.read(1) != b"\n":
                        f.write("\n")
            f.write("\n".join(new_links) + "\n")

        await event.client.send_file(
            'me', # Envia para Mensagens Salvas
            temp_file,
            caption=f"📄 {len(new_links)} novos links extraídos de {chat_input}"
        )

        await event.edit(
            f"✅ Busca finalizada!\n"
            f"📩 Mensagens lidas: {total_messages}\n"
            f"🔗 Links totais: {links_found}\n"
            f"✨ {len(new_links)} novos links enviados para as Mensagens Salvas."
        )

        if os.path.exists(temp_file):
            os.remove(temp_file)
