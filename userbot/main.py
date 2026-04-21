import os
import logging
import asyncio
import importlib
from telethon import TelegramClient, events

# Configurações básicas
API_ID = 1234567  # Substitua pelo seu API_ID
API_HASH = 'sua_api_hash'  # Substitua pela sua API_HASH
SESSION_NAME = 'userbot_session'

logging.basicConfig(level=logging.INFO)

client = TelegramClient(SESSION_NAME, API_ID, API_HASH)

def load_plugins():
    plugins_path = os.path.join(os.path.dirname(__file__), 'plugins')
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

    load_plugins()

    print("Userbot rodando. Pressione Ctrl+C para parar.")
    await client.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main())
