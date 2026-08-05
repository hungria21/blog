import os
from dotenv import load_dotenv

# Carrega as variáveis do arquivo .env
load_dotenv()

API_ID = int(os.getenv("API_ID", "0"))
API_HASH = os.getenv("API_HASH", "")
BOT_TOKEN = os.getenv("BOT_TOKEN", "")

def validate_config():
    """Valida se as configurações básicas estão preenchidas."""
    if not API_ID:
        return False, "API_ID inválido ou ausente."
    if not API_HASH:
        return False, "API_HASH ausente."
    if not BOT_TOKEN:
        return False, "BOT_TOKEN ausente."
    return True, "Configuração carregada com sucesso."
