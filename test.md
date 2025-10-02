# Análise e Planejamento: Sistema Flexível de Legendas Sequen

## planejamento de Novos Formatos para Maior Flexibilidade

### **Categoria 1: Animes**
```
- EP01, EP 01, Ep01, Ep 01
- Episode 01, Episode01
- Episódio 01, Episódio01
- 第01話, 第1話 (formato japonês)
- [01], (01), {01}
- E01, E 01
- Cap 01, Capítulo 01
- OVA 01, OVA01
- Especial 01
- Movie 01, Filme 01
```

### **Categoria 2: Séries/TV Shows**
```
- S01E01, S1E1, S01 E01
- Temporada 1 Episódio 01
- T01E01, T1E1
- 1x01, 1x1
- Season 1 Episode 01
```

### **Categoria 3: Documentários**
```
- Parte 01, Part 01
- Capítulo 01, Chapter 01
- Seção 01, Section 01
- Segmento 01
- Vol 01, Volume 01
- Bloco 01
```

### **Categoria 4: Áudio/Música**
```
- Faixa 01, Track 01
- #01, N° 01, Nº 01
- Audio 01, Áudio 01
- Mix 01, Remix 01
- Tema 01
```

### **Categoria 5: Aulas/Cursos**
```
- Aula 01, Lesson 01, Class 01
- Módulo 01, Module 01
- Unidade 01, Unit 01
- Lição 01
- Tutorial 01
```

### **Categoria 6: Formatos Genéricos**
```
- 01, 001, 0001 (número puro)
- Arquivo 01, File 01
- Item 01
- Vídeo 01, Video 01
- #01
```

---

## 🔧 Planejamento da Lógica de Reconhecimento

### **Abordagem 1: Sistema de Padrões Múltiplos (Recomendado)**

**Conceito:** Criar uma lista de regex patterns que o bot testa sequencialmente até encontrar um match.

**Estrutura da lógica:**
```
1. Receber input do usuário: "/legenda [formato]"
2. Iterar sobre lista de padrões regex pré-definidos
3. Para cada padrão, tentar fazer match com o input
4. Quando encontrar match, extrair:
   - Prefixo (tudo antes do número)
   - Número inicial (com padding original)
   - Sufixo (tudo depois do número, se houver)
5. Armazenar no estado:
   - prefixo completo
   - sufixo completo
   - contador inicial
   - padding (zeros à esquerda)
6. Gerar próximas legendas concatenando: prefixo + número + sufixo
```

**Padrões Regex a implementar:**
```python
PATTERNS = [
    # S01E01, T01E01, etc
    r'^([ST])(\d+)[Ee](\d+)$'
    
    # 1x01, 1x1
    r'^(\d+)x(\d+)$'
    
    # EP01, Ep01, E01 (colado)
    r'^([EeÉé][Pp]?|Cap(?:ítulo)?|OVA)(\d+)$'
    
    # EP 01, Ep 01, E 01 (com espaço)
    r'^([EeÉé][Pp]?|Episode|Episódio|Cap(?:ítulo)?|OVA)\s+(\d+)$'
    
    # [01], (01), {01}
    r'^([\[\(\{])(\d+)([\]\)\}])$'
    
    # Parte 01, Part 01, etc
    r'^(Parte|Part|Cap(?:ítulo)?|Chapter|Volume?|Aula|Lesson)\s+(\d+)$'
    
    # Faixa 01, Track 01, #01
    r'^(Faixa|Track|#|N[º°]|Áudio|Audio)\s*(\d+)$'
    
    # Número puro no final (fallback, já existente)
    r'^(.*?)(\d+)$'
]
```

---

### **Abordagem 2: Sistema de Templates com Placeholders**

**Conceito:** Usuário define um template com marcador especial para o número.

**Exemplo de uso:**
```
/legenda EP{N} → EP1, EP2, EP3...
/legenda S01E{N} → S01E1, S01E2, S01E3...
/legenda [Temporada 1] Episódio {N} → [Temporada 1] Episódio 1, ...
```

**Lógica:**
```
1. Detectar marcador {N} ou {NUM} no input
2. Separar template em: parte_antes + marcador + parte_depois
3. Perguntar ao usuário o número inicial e padding
4. Gerar legendas substituindo o marcador
```

---

### **Abordagem 3: Sistema Híbrido (Mais Flexível)**

**Conceito:** Combinar detecção automática com opção de template manual.

**Fluxo:**
```
1. Tentar detecção automática com os padrões regex
2. Se falhar, sugerir ao usuário usar template com {N}
3. Permitir override manual: /legenda_custom <template> <inicio> <padding>
```

---

## 🎨 Casos Especiais a Considerar

### **1. Formatos com Múltiplos Números**
```
S01E01 → Como incrementar?
Opção A: Apenas o último número (E01 → E02)
Opção B: Perguntar ao usuário qual incrementar
Opção C: Sistema de "variáveis múltiplas"
```

### **2. Preservação de Formatação**
```
EP01 vs Ep01 vs ep01 → Manter case original
[01] vs (01) vs {01} → Manter delimitadores originais
```

### **3. Números com Separadores**
```
01-A, 01.1, 01_parte_1
Decisão: Aceitar ou rejeitar?
```

### **4. Sufixos Variáveis**
```
EP01 - Título Variável
Como lidar: Ignorar tudo após o número na detecção inicial
```

---

## 📝 Prompt de Implementação Sugerida

**"Crie um sistema flexível de reconhecimento de formatos de legenda sequencial que:**

1. **Mantenha compatibilidade total** com o formato atual (prefixo opcional + número)

2. **Adicione suporte para múltiplos padrões** através de uma lista de regex patterns que cubram:
   - Formatos de animes (EP01, Ep 01, Episode 01, OVA 01, Cap 01, [01])
   - Formatos de séries (S01E01, 1x01, T01E01)
   - Formatos de documentários (Parte 01, Volume 01, Capítulo 01)
   - Formatos de áudio (Faixa 01, Track 01, #01)
   - Formatos de aulas (Aula 01, Módulo 01, Lição 01)
   - Números puros e formatos genéricos

3. **Preserve a formatação original**, incluindo:
   - Case (maiúsculas/minúsculas)
   - Espaçamento
   - Delimitadores ([], (), {})
   - Padding de zeros

4. **Extraia e armazene**:
   - Prefixo completo (tudo antes do número)
   - Sufixo completo (tudo depois do número, se houver)
   - Número inicial com padding original
   - Pattern usado (para regeneração consistente)

5. **Implemente lógica de fallback**: Se nenhum padrão específico for reconhecido, use o sistema atual (número no final)

6. **Adicione validação**: Informe o usuário sobre o formato detectado e exemplo da sequência antes de ativar

7. **Mantenha a arquitetura assíncrona** e o sistema de fila existente sem alterações

8. **Teste com exemplos** de cada categoria para garantir reconhecimento correto"

---

## código a ser corrigido 

```
# -*- coding: utf-8 -*-

import asyncio
import logging
import re
from telethon import TelegramClient, events
from telethon.errors.rpcerrorlist import FloodWaitError
from telethon.tl.types import Message

# Importa as credenciais do arquivo de configuração.
# É fundamental que o arquivo config.py esteja na mesma pasta.
try:
    from config import API_ID, API_HASH, BOT_TOKEN
except ImportError:
    print("ERRO: O arquivo 'config.py' não foi encontrado.")
    print("Por favor, crie o arquivo com suas credenciais do Telegram (API_ID, API_HASH, BOT_TOKEN).")
    exit(1)

# --- Configuração do Logging ---
# Configura o logging para exibir informações de depuração no console.
# Mantendo os logs em inglês para facilitar a depuração técnica.
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# --- Configuração do Cliente Telethon ---
# Cria uma instância do cliente Telegram.
# O arquivo '.session' armazena o estado da sessão para evitar logins repetidos.
client = TelegramClient('bot_session', API_ID, API_HASH).start(bot_token=BOT_TOKEN)

# --- Gestão de Estado ---
# Mantém o estado do bot em memória.
class BotState:
    def __init__(self):
        self.text_to_remove = ""
        self.renaming_mode_active = False
        self.renaming_prefix = ""
        self.renaming_counter = 0
        self.renaming_padding = 0

    def reset(self):
        """Reseta todas as configurações de edição para o estado inicial."""
        self.text_to_remove = ""
        self.renaming_mode_active = False
        self.renaming_prefix = ""
        self.renaming_counter = 0
        self.renaming_padding = 0
        logging.info("All editing modes have been reset.")

bot_state = BotState()

# --- Sistema de Fila Assíncrona ---
# Fila para gerenciar tarefas de edição de mensagens e evitar limites de taxa da API.
# Usar asyncio.Queue é a abordagem idiomática para bibliotecas assíncronas como a Telethon.
edit_queue = asyncio.Queue()

# O restante da lógica (worker, handlers) será adicionado nas próximas etapas.
logging.info("Bot core logic initialized.")


async def edit_worker():
    """
    Processa tarefas da fila de edição de forma assíncrona.
    Este worker é a única fonte da verdade para gerar legendas sequenciais,
    prevenindo condições de corrida e tratando os limites de taxa da API do Telegram.
    """
    while True:
        # Aguarda uma nova tarefa na fila.
        task_type, message = await edit_queue.get()
        new_caption = None

        try:
            # --- Lógica de Geração de Legenda ---
            # A lógica foi movida para dentro do worker para garantir execução atômica.
            if task_type == 'rename' and bot_state.renaming_mode_active:
                new_caption = f"{bot_state.renaming_prefix}{str(bot_state.renaming_counter).zfill(bot_state.renaming_padding)}"
                bot_state.renaming_counter += 1
                logging.info(f"Worker generated caption '{new_caption}' for message {message.id}.")

            elif task_type == 'remove' and bot_state.text_to_remove and message.text and bot_state.text_to_remove in message.text:
                new_caption = message.text.replace(bot_state.text_to_remove, '').strip()
                logging.info(f"Worker generated caption for message {message.id} by removing text.")

            if new_caption is None:
                # O modo pode ter sido resetado após a tarefa ser enfileirada.
                logging.warning(f"Skipping task for message {message.id} as no action is applicable.")
                continue

            # --- Chamada de API com Lógica de Retry ---
            while True:
                try:
                    # Para editar a legenda de uma mídia, é crucial passar o 'file' original.
                    # Caso contrário, a Telethon pode remover a mídia da mensagem.
                    await client.edit_message(
                        entity=message.chat_id,
                        message=message.id,
                        text=new_caption,
                        file=message.media if message.media else None
                    )
                    logging.info(f"Successfully edited message {message.id} in chat {message.chat_id}.")
                    break  # Sucesso, sai do loop de retry.
                except FloodWaitError as e:
                    # A API do Telegram pediu para esperar.
                    logging.warning(f"Rate limited. Waiting for {e.seconds} seconds...")
                    await asyncio.sleep(e.seconds)
                except Exception as e:
                    logging.error(f"Failed to edit caption for message {message.id}: {e}")
                    break  # Erro não recuperável, desiste da tarefa.

        finally:
            # Garante que a tarefa seja marcada como concluída, mesmo se ocorrer um erro.
            edit_queue.task_done()


@client.on(events.NewMessage(pattern='/start'))
async def start_handler(event):
    """Handler para o comando /start."""
    await event.reply("Este bot renomeia postagens de forma sequencial, envie o comando /help para ver os comandos disponíveis.")


@client.on(events.NewMessage(pattern='/help'))
async def help_handler(event):
    """Handler para o comando /help."""
    help_text = (
        "Comandos\n"
        "/set_text - Remove um texto\n"
        "/legenda - Define renomeação sequencial\n"
        "/reset - Reseta o modo do bot."
    )
    await event.reply(help_text)


@client.on(events.NewMessage(pattern='/reset'))
async def reset_handler(event):
    """Handler para o comando /reset."""
    bot_state.reset()
    await event.reply("Todos os modos de edição foram resetados. O bot está inativo agora.")


@client.on(events.NewMessage(pattern='/set_text'))
async def set_text_handler(event):
    """
    Define o texto a ser removido das legendas.
    Exemplo: /set_text 'Dual Audio'
    """
    bot_state.reset()
    # Pega o texto após o comando /set_text
    parts = event.text.split(maxsplit=1)
    if len(parts) > 1:
        text_to_remove = parts[1].strip()
        bot_state.text_to_remove = text_to_remove
        await event.reply(f"Modo de remoção de texto ativado. Vou remover '{text_to_remove}' das legendas.")
    else:
        await event.reply(
            "Por favor, forneça o texto a ser removido após o comando.\n"
            "Exemplo: /set_text 'Dual Audio'"
        )


@client.on(events.NewMessage(pattern='/legenda'))
async def legenda_handler(event):
    """
    Define o modo de renomeação sequencial.
    Formato: /legenda <Prefixo> <Número> (ex: /legenda Ep 01)
    """
    bot_state.reset()
    parts = event.text.split(maxsplit=1)
    if len(parts) < 2:
        await event.reply("Por favor, forneça o formato inicial. Exemplo: /legenda Ep 01")
        return

    args = parts[1].strip()
    # Regex para encontrar o prefixo (opcional) e o número no final.
    match = re.match(r'^(.*?)(\s*)(\d+)$', args)

    if not match:
        await event.reply("Formato inválido. Por favor, use um formato como '/legenda Ep 01' ou '/legenda 10'.")
        return

    prefix = match.group(1).strip()
    number_str = match.group(3)

    bot_state.renaming_prefix = f"{prefix} " if prefix else ""
    bot_state.renaming_counter = int(number_str)
    bot_state.renaming_padding = len(number_str)
    bot_state.renaming_mode_active = True

    start_example = f"{bot_state.renaming_prefix}{str(bot_state.renaming_counter).zfill(bot_state.renaming_padding)}"
    await event.reply(f"Modo de renomeação sequencial ativado. Começando com: '{start_example}'.")


@client.on(events.NewMessage(func=lambda e: e.is_channel and not e.is_group))
async def channel_post_handler(event: Message):
    """
    Handler para novos posts em canais. Enfileira a mensagem para edição.
    A lógica de decisão está aqui, mas a execução está no worker.
    """
    message = event.message
    
    # Verifica se o modo de renomeação está ativo.
    if bot_state.renaming_mode_active:
        await edit_queue.put(('rename', message))
        logging.info(f"Queued message {message.id} for sequential rename.")
    
    # Verifica se o modo de remoção de texto está ativo e se a legenda é aplicável.
    elif bot_state.text_to_remove and message.text and bot_state.text_to_remove in message.text:
        await edit_queue.put(('remove', message))
        logging.info(f"Queued message {message.id} for text removal.")


async def main():
    """Função principal para iniciar o bot e o worker."""
    # Inicia o worker de edição em segundo plano.
    # asyncio.create_task é a forma moderna de agendar tarefas.
    asyncio.create_task(edit_worker())
    
    logging.info("Bot is starting...")
    # O 'await client.start()' já foi chamado na inicialização do client.
    # Agora, apenas mantemos o bot rodando.
    print("O bot foi iniciado e está aguardando mensagens.")
    await client.run_until_disconnected()


if __name__ == '__main__':
    # Executa a função principal usando o loop de eventos asyncio.
    try:
        client.loop.run_until_complete(main())
    except KeyboardInterrupt:
        print("Bot encerrado.")
    except Exception as e:
        logging.critical(f"A critical error occurred: {e}")
```

## ✅ Benefícios da Abordagem Proposta

- ✨ **Flexibilidade máxima** sem aumentar complexidade para o usuário
- 🔄 **Retrocompatibilidade** garantida
- 🌍 **Suporte multilíngue** (português, inglês, japonês)
- 🎯 **Detecção inteligente** sem necessidade de comandos diferentes
- 🔧 **Extensível** para adicionar novos formatos facilmente
- 📊 **Mantém performance** usando regex eficientes