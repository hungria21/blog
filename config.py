import os
from dotenv import load_dotenv

# Carrega variáveis do arquivo .env, se ele existir
load_dotenv()

# =====================================================================
# CONFIGURAÇÃO DAS CREDENCIAIS E CANAIS
# Substitua os valores abaixo pelos seus dados ou utilize um arquivo .env
# =====================================================================

API_ID = 0  # Cole aqui o seu API_ID (número inteiro), ex: 1234567
API_HASH = ""  # Cole aqui o seu API_HASH (string), ex: "abcdef1234567890abcdef1234567890"

SOURCE_CHANNEL = ""  # ID (ex: -100xxx) ou @username do canal de origem
DESTINATION_CHANNEL = ""  # ID (ex: -100xxx) ou @username do canal de destino

# =====================================================================

def get_credentials():
    """
    Retorna as credenciais configuradas de forma estática no arquivo config.py
    ou através do arquivo .env / variáveis de ambiente.
    """
    # 1. Tenta carregar das variáveis de ambiente / .env
    api_id_env = os.getenv("API_ID")
    api_hash_env = os.getenv("API_HASH")
    source_env = os.getenv("SOURCE_CHANNEL")
    dest_env = os.getenv("DESTINATION_CHANNEL")

    # 2. Usa os valores estáticos definidos acima se os do ambiente não existirem
    api_id_val = api_id_env if api_id_env is not None else API_ID
    api_hash_val = api_hash_env if api_hash_env is not None else API_HASH
    source_val = source_env if source_env is not None else SOURCE_CHANNEL
    destination_val = dest_env if dest_env is not None else DESTINATION_CHANNEL

    # Converte api_id para int se possível
    if api_id_val:
        try:
            api_id_val = int(api_id_val)
        except ValueError:
            pass

    # Se as credenciais estiverem vazias ou com valores padrão, avisa o usuário e encerra
    if not api_id_val or api_id_val == 0 or not api_hash_val:
        print("\n" + "=" * 60)
        print(" [!] ERRO: Credenciais não configuradas!")
        print("=" * 60)
        print("Por favor, abra o arquivo 'config.py' e insira seu API_ID e API_HASH.")
        print("Ou configure as variáveis de ambiente API_ID e API_HASH.")
        print("=" * 60 + "\n")
        import sys
        sys.exit(1)

    if not source_val or not destination_val:
        print("\n" + "=" * 60)
        print(" [!] ERRO: Canais de origem ou destino não configurados!")
        print("=" * 60)
        print("Por favor, abra o arquivo 'config.py' e insira os canais.")
        print("Ou configure as variáveis de ambiente SOURCE_CHANNEL e DESTINATION_CHANNEL.")
        print("=" * 60 + "\n")
        import sys
        sys.exit(1)

    # Função auxiliar para tratar IDs de canais que devem ser inteiros
    def parse_channel_identifier(val):
        val_str = str(val).strip()
        if val_str.startswith("-") or val_str.isdigit():
            try:
                return int(val_str)
            except ValueError:
                pass
        return val_str

    return {
        "api_id": int(api_id_val),
        "api_hash": api_hash_val.strip(),
        "source": parse_channel_identifier(source_val),
        "destination": parse_channel_identifier(destination_val)
    }
