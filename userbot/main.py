import os
import logging
import asyncio
import importlib
from telethon import TelegramClient, events
from config import API_ID, API_HASH, SESSION_NAME

logging.basicConfig(level=logging.INFO)

client = TelegramClient(SESSION_NAME, API_ID, API_HASH)

def load_plugins():
    plugins_path = os.path.join(os.path.dirname(__file__), 'plugins')
    if not os.path.exists(plugins_path):
        return

    for filename in os.listdir(plugins_path):
        if filename.endswith('.py') and not filename.startswith('__'):
            module_name = f'plugins.{filename[:-3]}'
            try:
                module = importlib.import_module(module_name)
                if hasattr(module, 'setup'):
                    module.setup(client)
                logging.info(f"Plugin carregado: {module_name}")
            except Exception as e:
                logging.error(f"Erro ao carregar plugin {module_name}: {e}")

async def main():
    print("Iniciando Userbot...")
    await client.start()
    print("Userbot conectado!")

    # Adiciona o diretório atual ao sys.path para importação correta dos plugins
    import sys
    sys.path.append(os.path.dirname(__file__))

    load_plugins()

    print("Userbot rodando. Pressione Ctrl+C para parar.")
    await client.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main())
