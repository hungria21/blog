# Guia do Bot de Mensagens Ricas (MTProto Layer 227)

Este bot utiliza o protocolo MTProto (Telethon) com suporte à Camada 227 do Telegram para habilitar formatações avançadas "Rich Messages", superando as limitações dos bots convencionais.

## Funcionalidades Principais

### 1. Suporte Nativo (Layer 227)
O bot envia mensagens usando o novo campo nativo `rich_message`, permitindo:
- **Cabeçalhos:** `# Título 1`, `## Título 2`
- **Tabelas:** Uso de sintaxe Markdown para tabelas.
- **LaTeX Nativo:** Fórmulas matemáticas que renderizam diretamente no Telegram.
- **Checklists:** `[ ]` e `[x]`.

### 2. Formatação Avançada e Fallback
Se o destinatário ou o aplicativo não suportar Rich Messages nativas, o bot possui um motor de processamento próprio que garante:
- **Citações Expansíveis:** `>> Sua citação aqui` (Colapsada por padrão).
- **Diagramas (Kroki):** Blocos de código `mermaid`, `plantuml`, `graphviz`, etc., são convertidos em links de imagem renderizada.
- **LaTeX (Codecogs):** Como redundância para fórmulas matemáticas.
- **Markdown Padrão:** `**negrito**`, `*itálico*`, `~~tachado~~`, `||spoiler||`, etc.

### 3. Modos de Operação
- **Direto:** Envie o texto formatado para o bot e ele responderá com a versão rica.
- **Inline:** Use `@SeuBot texto` em qualquer conversa para enviar mensagens ricas.

## Configuração

1. Configure `api_id`, `api_hash` e `bot_token` no arquivo `config.py`.
2. Instale as dependências: `pip install -r requirements.txt`.
3. Execute: `python3 main.py`.

## Detalhes Técnicos
O bot implementa manualmente os construtores da Layer 227 para Telethon. O processamento de entidades manual garante o alinhamento correto de offsets UTF-16, essencial para mensagens contendo Emojis. O bot detecta automaticamente se a API rejeita o envio nativo e alterna para o modo de entidades tradicionais de alta compatibilidade.
