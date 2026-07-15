import os
import sys
import json
import asyncio
from telethon import TelegramClient, errors, types
from config import get_credentials

PROGRESS_FILE = "progress.json"

def load_progress():
    """
    Carrega o ID da última mensagem enviada com sucesso a partir do arquivo local.
    Retorna 0 caso o arquivo não exista ou esteja corrompido.
    """
    if os.path.exists(PROGRESS_FILE):
        try:
            with open(PROGRESS_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get("last_sent_id", 0)
        except Exception as e:
            print(f"[Aviso] Erro ao ler arquivo de progresso: {e}. Iniciando do zero.")
    return 0

def save_progress(last_id):
    """
    Salva o ID da última mensagem processada com sucesso no arquivo local.
    """
    try:
        with open(PROGRESS_FILE, 'w', encoding='utf-8') as f:
            json.dump({"last_sent_id": last_id}, f, indent=4)
    except Exception as e:
        print(f"[Erro] Falha ao salvar progresso: {e}")

async def main():
    print("=" * 60)
    print("            TELEGRAM CHANNEL CLONER USERBOT            ")
    print("=" * 60)

    # Obtém as credenciais (do ambiente, .env ou input do terminal)
    creds = get_credentials()
    api_id = creds["api_id"]
    api_hash = creds["api_hash"]
    source = creds["source"]
    destination = creds["destination"]

    # Carrega o progresso anterior
    last_sent_id = load_progress()
    if last_sent_id > 0:
        print(f"[*] Progresso detectado! Retomando a partir da mensagem ID: {last_sent_id}")
    else:
        print("[*] Nenhum progresso anterior encontrado. Iniciando clonagem do início do canal.")

    # Inicializa o cliente do Telethon
    # 'cloner_session' será o nome do arquivo de sessão do Telethon (.session)
    client = TelegramClient('cloner_session', api_id, api_hash)

    print("[*] Conectando ao Telegram...")
    await client.start()
    print("[+] Conectado com sucesso!")

    try:
        # Resolve as entidades do canal de origem e destino para validar acesso
        source_entity = await client.get_input_entity(source)
        dest_entity = await client.get_input_entity(destination)

        # Obtém detalhes amigáveis para exibição
        source_channel_info = await client.get_entity(source_entity)
        dest_channel_info = await client.get_entity(dest_entity)

        source_title = getattr(source_channel_info, 'title', str(source))
        dest_title = getattr(dest_channel_info, 'title', str(destination))

        print(f"[i] Canal Origem: {source_title} (ID: {source_channel_info.id})")
        print(f"[i] Canal Destino: {dest_title} (ID: {dest_channel_info.id})")
    except Exception as e:
        print(f"[Erro Crítico] Não foi possível acessar os canais configurados. Detalhes: {e}")
        await client.disconnect()
        sys.exit(1)

    print("[*] Buscando mensagens pendentes...")

    # Armazena a contagem de mensagens enviadas nesta sessão para controle de pausa de proteção
    messages_sent_count = 0

    try:
        # Iteramos em ordem cronológica (reverse=True) partindo do min_id=last_sent_id.
        # min_id garante que apenas mensagens com ID estritamente maior que last_sent_id sejam buscadas.
        async for message in client.iter_messages(source_entity, reverse=True, min_id=last_sent_id):
            # Ignora mensagens de serviço que não podem ser encaminhadas (ex: pin, chat_participant, etc.)
            if isinstance(message, types.MessageService):
                print(f"[Info] Pulando mensagem de serviço ID: {message.id}")
                last_sent_id = message.id
                save_progress(last_sent_id)
                continue

            # Se for uma mensagem de texto vazia sem mídia (caso raro, mas possível)
            if not message.message and not message.media:
                print(f"[Info] Pulando mensagem vazia/sem conteúdo ID: {message.id}")
                last_sent_id = message.id
                save_progress(last_sent_id)
                continue

            print(f"[~] Encaminhando mensagem ID: {message.id} ...")

            success = False
            retries = 3
            while retries > 0:
                try:
                    # Encaminha a mensagem respeitando integralmente a mídia e formatação original
                    await client.forward_messages(dest_entity, message)
                    success = True
                    break
                except errors.FloodWaitError as e:
                    print(f"[Aviso] Limite de requisições do Telegram atingido. Aguardando {e.seconds} segundos...")
                    await asyncio.sleep(e.seconds)
                    retries -= 1
                except Exception as e:
                    print(f"[Erro] Falha ao encaminhar mensagem {message.id}: {e}")
                    retries -= 1
                    if retries > 0:
                        print(f"Tentando novamente em 5 segundos... ({retries} tentativas restantes)")
                        await asyncio.sleep(5)

            if success:
                # Incrementa contadores e atualiza progresso local
                messages_sent_count += 1
                last_sent_id = message.id
                save_progress(last_sent_id)
                print(f"[+] Mensagem {message.id} encaminhada com sucesso! (Total na sessão: {messages_sent_count})")

                # Delay obrigatório de 2 segundos entre o envio de cada mensagem
                await asyncio.sleep(2)

                # Pausa automática de 1 minuto a cada 30 mensagens enviadas
                if messages_sent_count % 30 == 0:
                    print("-" * 60)
                    print(f"[i] Pausa automática de proteção contra bloqueios (1 minuto)...")
                    print("-" * 60)
                    for remaining in range(60, 0, -10):
                        print(f"Retomando em {remaining} segundos...")
                        await asyncio.sleep(10)
                    print("[*] Retomando clonagem...")
            else:
                # Se após as tentativas falhou, podemos optar por parar ou pular salvando o progresso para evitar loop infinito
                print(f"[Erro Crítico] Não foi possível encaminhar a mensagem {message.id} após várias tentativas. Pulando para não travar o processo.")
                last_sent_id = message.id
                save_progress(last_sent_id)

        print("=" * 60)
        print("[🎉] Clonagem concluída! Todas as mensagens disponíveis foram replicadas.")
        print("=" * 60)

    except KeyboardInterrupt:
        print("\n[!] Processo interrompido pelo usuário. O progresso foi salvo com sucesso!")
    except Exception as e:
        print(f"\n[!] Ocorreu um erro inesperado: {e}")
    finally:
        await client.disconnect()
        print("[*] Cliente desconectado. Até logo!")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n[!] Encerrando...")
