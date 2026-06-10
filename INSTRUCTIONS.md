# Guia do Bot de Mensagens Ricas (MTProto)

Este bot foi desenvolvido para contornar as limitações da API oficial de bots do Telegram, utilizando o protocolo MTProto (Telethon) para enviar mensagens com formatações avançadas, incluindo citações expansíveis, diagramas e fórmulas matemáticas.

## Funcionalidades Suportadas

### 1. Formatação Padrão (Markdown)
- `**negrito**` -> **negrito**
- `*itálico*` ou `_itálico_` -> *itálico*
- `__sublinhado__` -> __sublinhado__
- `~~tachado~~` -> ~~tachado~~
- `||spoiler||` -> spoiler
- `` `código` `` -> monocompactado
- `[texto](url)` -> Link clicável

### 2. Citações (Quotes)
- `> Citação simples`
- `>> Citação expansível (colapsada por padrão)`

### 3. Diagramas (Kroki Integration)
Você pode criar diagramas usando blocos de código com a linguagem específica. O bot converterá automaticamente para um link de imagem renderizada.
Linguagens suportadas: `mermaid`, `plantuml`, `graphviz`, `dot`, `ditaa`, `c4plantuml`, `erd`, `nomnoml`, `vega`, `vegalite`, `wavedrom`, `bpmn`, `bytefield`, `actdiag`, `nwdiag`, `packetdiag`, `rackdiag`, `seqdiag`, `svgbob`, `umlet`, `pikchr`, `structurizr`, `diagramsnet`, `excalidraw`, `tikz`, `symbolator`.

Exemplo:
\```mermaid
graph TD;
    A-->B;
    A-->C;
    B-->D;
    C-->D;
\```

### 4. Fórmulas Matemáticas (LaTeX)
Use `$$` para envolver fórmulas LaTeX. O bot converterá para um link de imagem.
Exemplo: `$$e^{i\pi} + 1 = 0$$`

### 5. Cabeçalhos e Listas (Simulados)
Como o Telegram ainda está liberando suporte nativo para Headings e Tabelas (Layer 227+), o bot simula essas funções:
- `# Título 1` -> **◈ TÍTULO 1**
- `## Título 2` -> **◇ Título 2**
- `[ ] Tarefa pendente` -> ⬜ Tarefa pendente
- `[x] Tarefa concluída` -> ✅ Tarefa concluída
- `---` -> Linha divisória

## Como Usar

### Modo Direto
Envie qualquer mensagem formatada diretamente para o bot.

### Modo Inline
Em qualquer chat, digite `@NomeDoSeuBot sua mensagem`.
O bot mostrará um resultado "Enviar Mensagem Rica". Clique nele para enviar a mensagem formatada para o chat atual.

## Configuração

1. Obtenha seu `api_id` e `api_hash` em [my.telegram.org](https://my.telegram.org).
2. Obtenha o `bot_token` no `@BotFather`.
3. Preencha os dados no arquivo `config.py`.
4. Instale as dependências: `pip install -r requirements.txt`.
5. Execute: `python3 main.py`.

## Notas Técnicas
- O bot utiliza a biblioteca **Telethon**.
- O processamento de entidades é feito manualmente para garantir que offsets UTF-16 (necessários para emojis) e aninhamentos funcionem corretamente.
- Se o Telegram atualizar o suporte oficial para tabelas e cabeçalhos na API de bots, este bot poderá ser atualizado para usar as entidades nativas.
