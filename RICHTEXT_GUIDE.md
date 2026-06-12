# Guia de Formatação: Rich Messages (Bot API 10.1)

Este guia descreve as novas funcionalidades de "Rich Messages" introduzidas na versão 10.1 da API de Bots do Telegram (Junho de 2026). As Rich Messages permitem enviar textos altamente estruturados, incluindo tabelas, fórmulas matemáticas (LaTeX), colagens de mídia e blocos expansíveis.

---

## 1. Rich Markdown

Para utilizar este modo, o conteúdo deve ser enviado no campo `markdown` do objeto `InputRichMessage`.

### Formatação de Texto
- `**negrito**` ou `__negrito__`
- `*itálico*` ou `_itálico_`
- `~~tachado~~`
- `==marcado==` (Destaque/Highlight)
- `||spoiler||`
- `` `código inline` ``
- `<u>sublinhado</u>` (via tag HTML aninhada)
- `^sobrescrito^` (via tag `<sup>`) e `~subscrito~` (via tag `<sub>`)

### Cabeçalhos (Headings)
```markdown
# Título Nível 1
## Título Nível 2
### Título Nível 3
#### Título Nível 4
##### Título Nível 5
###### Título Nível 6
```

### Listas
- **Não ordenada:** `-` , `*` ou `+`
- **Ordenada:** `1.` , `2.` , etc.
- **Lista de Tarefas (Checklist):**
  - `- [ ] Item pendente`
  - `- [x] Item concluído`

### Tabelas
```markdown
| Coluna 1 | Coluna 2 |
|:---------|:--------:|
| Alinhado Esquerda | Centralizado |
```

### Matemática (LaTeX)
- **Inline:** `$x^2 + y^2$`
- **Bloco:**
  ```markdown
  $$E = mc^2$$
  ```
  Ou use o bloco:
  ```math
  \sum_{i=1}^{n} i = \frac{n(n+1)}{2}
  ```

### Blocos de Citação e Expansíveis
- **Citação:** `> Bloco de citação`
- **Citação Expansível:** Use a sintaxe de spoiler ou tags HTML `<details>` dentro do Markdown.

### Mídia (URLs Diretas)
- Foto: `![](https://link.com/foto.jpg)`
- Vídeo: `![](https://link.com/video.mp4)`
- Com legenda: `![](https://link.com/foto.jpg "Legenda aqui")`

### Colagens e SlideShows (Markdown)
No Rich Markdown, as colagens e slideshows são inseridos utilizando tags HTML diretamente no corpo do texto:

```markdown
<tg-slideshow>
![](https://link.com/foto1.jpg "Legenda 1")
![](https://link.com/foto2.jpg "Legenda 2")
<figcaption>Legenda do Slideshow</figcaption>
</tg-slideshow>
```

---

## 2. Rich HTML

Para utilizar este modo, o conteúdo deve ser enviado no campo `html` do objeto `InputRichMessage`.

### Tags Suportadas
- `<b>`, `<strong>`: Negrito
- `<i>`, `<em>`: Itálico
- `<u>`, `<ins>`: Sublinhado
- `<s>`, `<strike>`, `<del>`: Tachado
- `<mark>`: Texto marcado/destacado
- `<sub>`, `<sup>`: Subscrito e Sobrescrito
- `<tg-spoiler>`: Spoiler
- `<code>`: Código inline
- `<pre>`: Bloco de código (use `<code class="language-python">` para sintaxe)
- `<h1>` até `<h6>`: Cabeçalhos
- `<hr/>`: Divisor horizontal
- `<footer>`: Rodapé da mensagem

### Elementos Avançados
- **Matemática:** `<tg-math>x^2</tg-math>` (inline) ou `<tg-math-block>E=mc^2</tg-math-block>` (bloco).
- **Tabelas:** `<table>`, `<tr>`, `<td>`, `<th>`. Suporta atributos `colspan`, `rowspan`, `bordered`, `striped`.
- **Blocos Expansíveis:**
  ```html
  <details>
    <summary>Título do Bloco</summary>
    Conteúdo oculto que pode conter outros blocos.
  </details>
  ```
- **Mapas:** `<tg-map lat="41.9" long="12.5" zoom="14"/>`
- **Colagens e Slideshows:**
  No Rich HTML, use as tags `<tg-collage>` ou `<tg-slideshow>`. Você pode incluir legendas usando `<figcaption>`.
  ```html
  <tg-slideshow>
    <figure>
      <img src="https://link.com/foto1.jpg"/>
      <figcaption>Legenda da Foto 1</figcaption>
    </figure>
    <img src="https://link.com/foto2.jpg"/>
    <figcaption>Legenda Geral do Slideshow</figcaption>
  </tg-slideshow>
  ```

---

## 3. Limites das Rich Messages

- **Caracteres:** Até 32.768 caracteres UTF-8.
- **Blocos:** Máximo de 500 blocos (incluindo itens de lista, linhas de tabela, etc.).
- **Aninhamento:** Até 16 níveis de profundidade.
- **Mídia:** Até 50 anexos de mídia por mensagem.
- **Colunas:** Máximo de 20 colunas em uma tabela.

---
---

## 4. Uso Programático (rich_models.py)

Para facilitar a criação de mensagens complexas sem lidar com strings manuais, utilize as classes fornecidas no projeto:

```python
from rich_models import RichMessageBuilder, Heading, Bold, Table, TableCell, RichText

builder = RichMessageBuilder()
builder.add(Heading(RichText("Relatório de Vendas"), level=1))

# Criando uma tabela
header = [TableCell(RichText("Produto"), is_header=True), TableCell(RichText("Qtd"), is_header=True)]
row1 = [TableCell(RichText("Bot")), TableCell(RichText("10"))]
builder.add(Table([header, row1]))

# Gerando o payload
markdown_text = builder.build_markdown()
bot.send_rich_message(chat_id, markdown=markdown_text)
```

---

## 5. Modo Inline

O bot suporta o modo inline para transformar links e textos em Rich Messages instantaneamente através de templates pré-configurados.

### Como usar:
1. Em qualquer chat, digite `@NomeDoSeuBot <comando ou links>`.
2. Escolha uma das opções:
   - **Criar SlideShow:** Se você colar 2 ou mais links de imagens.
   - **Criar Colagem:** Se você colar 2 ou mais links de imagens.
   - **Criar Tabela:** Digite qualquer texto para gerar uma linha de dados.
   - **Converter para LaTeX:** Digite uma fórmula científica.
   - **Criar Bloco Expansível:** Digite o conteúdo que deseja ocultar.

---

## 6. API Reference (Bot API 10.1)

Para enviar uma Rich Message via API:
**Método:** `sendRichMessage`
**Parâmetros:**
- `chat_id`: ID do chat.
- `rich_message`: Objeto `InputRichMessage` contendo:
    - `markdown` ou `html`: O conteúdo formatado.
    - `is_rtl` (opcional): Booleano para exibição da direita para a esquerda.
    - `skip_entity_detection` (opcional): Booleano para pular a detecção automática de links/números.
