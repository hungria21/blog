# Bot de Mensagens Ricas (MTProto)

Este bot permite o uso de novas formatações do Telegram (Rich Messages) que ainda não estão disponíveis na API padrão de bots, como citações expandíveis e integração com diagramas/fórmulas.

## Requisitos

- Python 3.8+
- Telethon
- Requests

## Instalação

1. Clone o repositório.
2. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
3. Configure suas credenciais no arquivo `config.py`:
   - Obtenha seu `API_ID` e `API_HASH` em [my.telegram.org](https://my.telegram.org).
   - Obtenha seu `BOT_TOKEN` através do [@BotFather](https://t.me/BotFather).

## Execução

```bash
python3 main.py
```

## Formatações Suportadas

O bot utiliza um parser personalizado para converter sintaxe Markdown em entidades MTProto.

### Formatação de Texto
- `**negrito**` -> **negrito**
- `__sublinhado__` -> <u>sublinhado</u>
- `*itálico*` ou `_itálico_` -> *itálico*
- `~~riscado~~` -> ~~riscado~~
- `||spoiler||` -> spoiler
- `[texto](url)` -> Link clicável

### Citações (Quotes)
- `> Citação padrão` -> Bloco de citação normal.
- `>> Citação expandível` -> Bloco de citação que aparece recolhido por padrão.

### Fórmulas Matemáticas (LaTeX)
Use `$$` para envolver fórmulas LaTeX. Elas serão convertidas em links clicáveis que exibem a imagem da fórmula.
Exemplo: `$$e=mc^2$$`

### Diagramas (Kroki)
Use blocos de código com o nome da linguagem para renderizar diagramas via Kroki.
Exemplo:
\```mermaid
graph TD;
    A-->B;
    A-->C;
    B-->D;
    C-->D;
\```
Suporta: `mermaid`, `plantuml`, `graphviz`, `dot`, `ditaa`, `c4plantuml`, `erd`, `nomnoml`, `vega`, `vegalite`, `wavedrom`, `bpmn`, `bytefield`, `actdiag`, `nwdiag`, `packetdiag`, `rackdiag`, `seqdiag`, `svgbob`, `umlet`, `pikchr`, `structurizr`, `diagramsnet`, `excalidraw`, `tikz`, `symbolator`.

## Modo Inline

Você pode usar o bot em qualquer chat sem precisar adicioná-lo ao grupo. Basta digitar o username do seu bot seguido do texto:
`@nome_do_bot seu texto aqui com **formatação**`
