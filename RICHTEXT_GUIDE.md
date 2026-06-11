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
  ```html
  <tg-collage>
    <img src="URL1"/>
    <img src="URL2"/>
  </tg-collage>
  ```

---

## 3. Limites das Rich Messages

- **Caracteres:** Até 32.768 caracteres UTF-8.
- **Blocos:** Máximo de 500 blocos (incluindo itens de lista, linhas de tabela, etc.).
- **Aninhamento:** Até 16 níveis de profundidade.
- **Mídia:** Até 50 anexos de mídia por mensagem.
- **Colunas:** Máximo de 20 colunas em uma tabela.

---

## 4. Exemplos de Uso no Bot

Para enviar uma Rich Message via API:
**Método:** `sendRichMessage`
**Parâmetros:**
- `chat_id`: ID do chat.
- `rich_message`: Objeto `InputRichMessage` contendo:
    - `markdown` ou `html`: O conteúdo formatado.
    - `is_rtl` (opcional): Booleano para exibição da direita para a esquerda.
    - `skip_entity_detection` (opcional): Booleano para pular a detecção automática de links/números.
