# 🤖 Telegram Userbot

Userbot completo para Telegram usando Telethon com sistema de plugins modular.

## ✨ Características

- 🔌 **Sistema de plugins modular**
- 📥 **Download de vídeos** (YouTube, TikTok, etc) via yt-dlp
- 🖼️ **Download de galerias** (Instagram, Twitter, Reddit, etc) via gallery-dl
- 📊 **Sistema de estatísticas** integrado
- 🛡️ **Proteção anti-flood** automática
- 🔄 **Auto-retry** em caso de erros
- 📝 **Logs detalhados**
- 🎨 **Captions formatadas** com metadados e hashtags

## 📋 Requisitos

- Python 3.8+
- Conta do Telegram
- API ID e API Hash (obtidos em https://my.telegram.org)

## 🚀 Instalação

### 1. Clone ou baixe o projeto

```bash
git clone <seu-repositorio>
cd telegram-userbot
```

### 2. Instale as dependências

```bash
pip install -r requirements.txt
```

### 3. Configure as credenciais

#### Obter API ID e API Hash:
1. Acesse https://my.telegram.org
2. Faça login com seu número do Telegram
3. Vá em "API Development Tools"
4. Crie um novo aplicativo
5. Copie o `api_id` e `api_hash`

#### Gerar String de Sessão:

```bash
python generate_session.py
```

Siga as instruções e copie a string gerada.

### 4. Configure o arquivo .env

Copie o arquivo de exemplo:

```bash
cp .env.example .env
```

Edite o `.env` e adicione suas credenciais:

```env
API_ID=seu_api_id
API_HASH=seu_api_hash
STRING_SESSION=sua_string_de_sessao
```

**Alternativamente:** Se você não configurar o `.env`, o bot solicitará o `API_ID` e `API_HASH` interativamente ao ser iniciado.

### 5. Execute o bot

```bash
python userbot.py
```

## 📁 Estrutura do Projeto

```
telegram-userbot/
│
├── userbot.py              # Bot principal
├── plugins/                # Pasta de plugins
│   ├── __init__.py
│   ├── ytdl_plugin.py     # Plugin yt-dlp
│   └── gallery_plugin.py  # Plugin gallery-dl
│
├── downloads/              # Arquivos baixados (auto-criado)
├── requirements.txt        # Dependências
├── generate_session.py     # Gerador de sessão
├── .env.example           # Exemplo de configuração
└── README.md              # Este arquivo
```

## 🎮 Comandos Disponíveis

### Comandos Básicos

- `.alive` - Verifica se o bot está online
- `.ping` - Mede a latência do bot
- `.stats` - Mostra estatísticas detalhadas
- `.help` - Lista todos os comandos

### Downloads de Vídeo (yt-dlp)

- `.ytdl <url>` - Download de vídeo (melhor qualidade)
- `.ytmp3 <url>` - Download apenas do áudio em MP3

**Suporta:**
- YouTube
- TikTok
- Instagram (vídeos)
- Facebook
- Twitter
- E mais de 1000 sites!

**Exemplo:**
```
.ytdl https://www.youtube.com/watch?v=dQw4w9WgXcQ
```

### Downloads de Galeria (gallery-dl)

- `.gdl <url>` - Download de galeria de imagens
- `.gdlinfo` - Lista plataformas suportadas

**Suporta:**
- Instagram (posts, carrosséis)
- Twitter/X (threads com imagens)
- Reddit (posts, galerias)
- Pinterest (pins, boards)
- Tumblr
- DeviantArt
- ArtStation
- E mais de 100 sites!

**Exemplo:**
```
.gdl https://www.instagram.com/p/ABC123/
```

## 📊 Recursos de Proteção

### Anti-Flood
- Delay automático entre mensagens (5 segundos padrão)
- Detecta e aguarda FloodWait do Telegram
- Respeita SlowMode de grupos

### Auto-Retry
- 3 tentativas automáticas em caso de erro
- Tratamento inteligente de timeouts
- Logs detalhados de erros

### Limites do Telegram
- Arquivos até 2GB
- Verificação automática de tamanho
- Avisos quando exceder limites

## 🎨 Formatação de Conteúdo

### Captions Automáticas

Todos os downloads incluem captions formatadas com:

- ✅ Título/Nome do conteúdo
- 👤 Autor/Uploader
- 📅 Data de publicação
- 👁️ Visualizações (quando disponível)
- ❤️ Curtidas/Engajamento
- 💬 Descrição formatada
- 🏷️ Hashtags relevantes
- 🔗 Link original

### Exemplo de Caption:

```
📷 Instagram

👤 Autor: @usuario
📅 08/11/2025 14:30

💬 Descrição do post aqui...

🏷️ #foto #viagem #natureza

🔗 https://instagram.com/p/ABC123
```

## ⚙️ Configurações Avançadas

### Personalizar Prefixo de Comando

Edite em `userbot.py`:

```python
CMD_PREFIX = "."  # Altere para qualquer caractere
```

### Ajustar Anti-Flood

```python
FLOOD_WAIT_TIME = 5  # Segundos entre mensagens
MAX_RETRIES = 3      # Tentativas em caso de erro
```

### Pasta de Downloads

```python
DOWNLOAD_PATH = "./downloads"  # Caminho personalizado
```

## 🔌 Criando Novos Plugins

### Estrutura Básica

Crie um arquivo em `plugins/meu_plugin.py`:

```python
"""
Descrição do plugin
"""

def setup(bot, Config, stats, safe_send, safe_edit):
    """Função de setup obrigatória"""

    from telethon import events

    @bot.on(events.NewMessage(outgoing=True, pattern=r'^\.meucmd$'))
    async def meu_comando(event):
        stats.commands_executed += 1
        await safe_edit(event, "Olá do meu plugin!")
```

### Funções Disponíveis

- `safe_send(event, message, **kwargs)` - Enviar mensagem com anti-flood
- `safe_edit(message, text, **kwargs)` - Editar mensagem com proteção
- `Config` - Configurações globais
- `stats` - Objeto de estatísticas

## 🛡️ Segurança

### ⚠️ IMPORTANTE:

1. **NUNCA compartilhe sua STRING_SESSION**
   - Com ela, qualquer pessoa pode acessar sua conta

2. **Use em conta secundária**
   - Recomendado para testes
   - Evite usar em conta principal

3. **Cuidado com comandos públicos**
   - Comandos executados em grupos são visíveis
   - Use em conversas privadas quando necessário

4. **Backup da sessão**
   - Guarde sua string de sessão em local seguro
   - Se perder, precisará gerar nova

### 🚫 Riscos de Banimento

Para evitar ban do Telegram:

- ✅ Respeite os limites de API
- ✅ Use delays entre operações
- ✅ Não faça spam
- ✅ Não envie muitos arquivos rapidamente
- ✅ Respeite direitos autorais

## 🐛 Troubleshooting

### Bot não conecta

```bash
# Verifique suas credenciais
python generate_session.py

# Teste a conexão
python -c "from telethon import TelegramClient; print('OK')"
```

### Erro "yt-dlp not found"

```bash
pip install --upgrade yt-dlp
```

### Erro "gallery-dl not found"

```bash
pip install --upgrade gallery-dl
```

### Erro de permissões em downloads

```bash
chmod -R 755 downloads/
```

### FloodWait muito longo

- Aguarde o tempo indicado
- Reduza a frequência de comandos
- Aumente o `FLOOD_WAIT_TIME`

## 📝 Logs

Os logs são salvos em:
- `userbot.log` - Log completo
- Console - Log em tempo real

Níveis de log:
- INFO: Operações normais
- WARNING: Avisos (flood, etc)
- ERROR: Erros capturados

## 🔄 Atualizações

Para atualizar o bot:

```bash
git pull origin main
pip install -r requirements.txt --upgrade
```

## 📜 Licença

Este projeto é apenas para fins educacionais. Use por sua conta e risco.

## ⚠️ Disclaimer

- Este bot é um userbot, não é um bot oficial do Telegram
- Userbots operam na conta do usuário, não como bot separado
- O uso inadequado pode resultar em banimento da conta
- Respeite os Termos de Serviço do Telegram
- Respeite direitos autorais ao baixar conteúdo

## 🤝 Contribuindo

Contribuições são bem-vindas! Para adicionar novos plugins:

1. Crie o plugin em `plugins/`
2. Siga a estrutura padrão
3. Teste completamente
4. Documente os comandos

## 📞 Suporte

- Documentação Telethon: https://docs.telethon.dev
- yt-dlp: https://github.com/yt-dlp/yt-dlp
- gallery-dl: https://github.com/mikf/gallery-dl

---

**Desenvolvido com ❤️ usando Telethon**