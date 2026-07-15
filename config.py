import os
from dotenv import load_dotenv

# Carrega variáveis do arquivo .env, se ele existir
load_dotenv()

# Credenciais de acesso à API do Telegram
API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")

# Canais de origem e destino (podem ser IDs numéricos ou usernames como @canal)
SOURCE_CHANNEL = os.getenv("SOURCE_CHANNEL")
DESTINATION_CHANNEL = os.getenv("DESTINATION_CHANNEL")

def get_credentials():
    """
    Retorna as credenciais configuradas. Se não estiverem no ambiente ou no .env,
    solicita ao usuário que as digite via terminal.
    """
    global API_ID, API_HASH, SOURCE_CHANNEL, DESTINATION_CHANNEL

    # Garante que API_ID seja um inteiro se disponível
    api_id_val = API_ID
    if api_id_val:
        try:
            api_id_val = int(api_id_val)
        except ValueError:
            pass

    api_hash_val = API_HASH
    source_val = SOURCE_CHANNEL
    destination_val = DESTINATION_CHANNEL

    # Pergunta via terminal se não estiverem definidas
    if not api_id_val:
        print("API_ID não encontrada nas variáveis de ambiente.")
        while True:
            try:
                api_id_val = int(input("Digite o seu API_ID (apenas números): ").strip())
                break
            except ValueError:
                print("Por favor, insira um ID de API válido (número inteiro).")

    if not api_hash_val:
        print("API_HASH não encontrada nas variáveis de ambiente.")
        api_hash_val = input("Digite o seu API_HASH: ").strip()
        while not api_hash_val:
            api_hash_val = input("API_HASH não pode ser vazia. Digite o seu API_HASH: ").strip()

    if not source_val:
        print("Canal de origem não configurado.")
        source_val = input("Digite o ID ou username do canal de ORIGEM (ex: @canal_origem ou -100123456789): ").strip()
        while not source_val:
            source_val = input("Canal de origem não pode ser vazio: ").strip()

    if not destination_val:
        print("Canal de destino não configurado.")
        destination_val = input("Digite o ID ou username do canal de DESTINO (ex: @canal_destino ou -100987654321): ").strip()
        while not destination_val:
            destination_val = input("Canal de destino não pode ser vazio: ").strip()

    # Função auxiliar para tratar IDs de canais que devem ser inteiros
    def parse_channel_identifier(val):
        val_str = str(val).strip()
        # Se começar com -100 ou - ou for puramente numérico, tenta converter para int
        if val_str.startswith("-") or val_str.isdigit():
            try:
                return int(val_str)
            except ValueError:
                pass
        return val_str

    return {
        "api_id": int(api_id_val),
        "api_hash": api_hash_val,
        "source": parse_channel_identifier(source_val),
        "destination": parse_channel_identifier(destination_val)
    }
