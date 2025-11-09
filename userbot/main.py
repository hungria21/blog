import os
import sys
import glob
import importlib

# Garante que a raiz do projeto esteja no sys.path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

import asyncio
import time

from userbot import client, logger
from userbot.config import DOWNLOADS_PATH

async def cleanup_downloads():
    """Limpa arquivos antigos da pasta de downloads periodicamente."""
    while True:
        try:
            for f in os.listdir(DOWNLOADS_PATH):
                file_path = os.path.join(DOWNLOADS_PATH, f)
                if os.path.getmtime(file_path) < time.time() - 3600: # 1 hora
                    os.remove(file_path)
                    logger.info(f"Arquivo antigo removido: {f}")
        except Exception as e:
            logger.error(f"Erro durante a limpeza de downloads: {e}")

        await asyncio.sleep(3600) # Executa a cada hora

def setup_environment():
    """Garante que os diretórios necessários existam."""
    if not os.path.exists(DOWNLOADS_PATH):
        os.makedirs(DOWNLOADS_PATH)
        logger.info(f"Diretório de downloads criado em: {DOWNLOADS_PATH}")

def load_plugins():
    """Carrega todos os plugins da pasta de plugins dinamicamente."""
    plugins_dir = os.path.join(os.path.dirname(__file__), "plugins")
    for plugin_file in os.listdir(plugins_dir):
        if plugin_file.endswith(".py") and not plugin_file.startswith("__"):
            plugin_name = plugin_file[:-3]
            try:
                importlib.import_module(f"userbot.plugins.{plugin_name}")
                logger.info(f"Plugin '{plugin_name}' carregado com sucesso.")
            except Exception as e:
                logger.error(f"Não foi possível carregar o plugin '{plugin_name}': {e}", exc_info=True)

async def start_userbot():
    """Função principal para iniciar o userbot."""
    logger.info("Iniciando o userbot...")
    setup_environment()
    load_plugins()

    if not client.api_id or not client.api_hash:
        logger.error("API_ID e API_HASH não encontrados. Verifique seu arquivo .env.")
        return

    try:
        await client.start()
        await client.send_message("me", "**Userbot iniciado com sucesso!**")
        logger.info("Userbot conectado com sucesso!")

        # Inicia a tarefa de limpeza em segundo plano
        client.loop.create_task(cleanup_downloads())

        await client.run_until_disconnected()
    except Exception as e:
        logger.critical(f"Ocorreu um erro crítico: {e}", exc_info=True)

if __name__ == "__main__":
    client.loop.run_until_complete(start_userbot())
