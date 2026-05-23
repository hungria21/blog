import asyncio
import re
from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError
import config

async def main():
    # Inicialização do cliente
    client = TelegramClient('session_name', config.api_id, config.api_hash)

    print("Iniciando o cliente...")
    await client.connect()

    # Fluxo de login interativo
    if not await client.is_user_authorized():
        print(f"Fazendo login com o número: {config.phone}")
        await client.send_code_request(config.phone)
        code = input('Insira o código que você recebeu no Telegram: ')
        try:
            await client.sign_in(config.phone, code)
        except SessionPasswordNeededError:
            password = input('Verificação em duas etapas ativada. Insira sua senha: ')
            await client.sign_in(password=password)

    print("Login realizado com sucesso!")

    # Solicitar o canal alvo
    target_channel = input("Digite o @username do canal alvo: ")

    try:
        entity = await client.get_entity(target_channel)
    except Exception as e:
        print(f"Erro ao encontrar o canal: {e}")
        await client.disconnect()
        return

    # Dicionário para armazenar hashtags e usernames
    # chave: hashtag, valor: set de usernames (para evitar duplicatas)
    data = {}

    print(f"Iniciando a raspagem de mensagens em {target_channel}...")

    count = 0
    async for message in client.iter_messages(entity):
        if message.text:
            # Encontrar todas as hashtags
            hashtags = re.findall(r'#\w+', message.text)
            # Encontrar todos os usernames (@username)
            usernames = re.findall(r'@\w+', message.text)

            if hashtags and usernames:
                for tag in hashtags:
                    tag = tag.lower() # Normalizar para minúsculas
                    if tag not in data:
                        data[tag] = set()
                    for user in usernames:
                        data[tag].add(user)

        count += 1
        if count % 100 == 0:
            print(f"Processadas {count} mensagens...")

    print(f"Finalizado! Total de {count} mensagens processadas.")

    # Ordenar hashtags alfabeticamente
    sorted_hashtags = sorted(data.keys())

    # Gerar o arquivo .txt
    with open('resultado.txt', 'w', encoding='utf-8') as f:
        for tag in sorted_hashtags:
            f.write(f"{tag}\n")
            # Ordenar usernames alfabeticamente para cada hashtag
            sorted_users = sorted(list(data[tag]))
            for user in sorted_users:
                f.write(f"{user}\n")
            f.write("\n") # Linha em branco entre grupos

    print("O arquivo 'resultado.txt' foi gerado com sucesso!")
    await client.disconnect()

if __name__ == '__main__':
    asyncio.run(main())
