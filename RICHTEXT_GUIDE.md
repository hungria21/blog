# Guia Mestre de Formatação: Rich Messages (Bot API 10.1)

Este documento é a referência completa para o uso do bot e das novas funcionalidades de formatação estruturada do Telegram.

---

## 1. Como Usar o Bot

### Modo Direto
Envie qualquer texto formatado em Markdown para o bot em uma conversa privada. Ele responderá processando esse texto através do novo motor de **Rich Messages**.

### Modo Inline
Em qualquer chat, digite `@SeuBot <links ou texto>`:
- **🎞️ SlideShow:** Aparece automaticamente ao colar 2 ou mais links de imagens.
- **📊 Tabela:** Gera uma tabela rápida a partir do texto digitado.
- **📝 Texto Simples:** Fallback de segurança para mensagens rápidas.

---

## 2. Sintaxes Suportadas (Rich Markdown)

### Estruturas Nativas
- **Cabeçalhos:** `# H1` até `###### H6`
- **Tabelas:**
  ```markdown
  | Coluna A | Coluna B |
  |:--- |:---:|
  | Dado 1 | Centralizado |
  ```
- **Matemática (LaTeX):** `$x+y$` ou `$$E=mc^2$$`
- **Checklists:** `- [ ] Fazer café` e `- [x] Beber café`

### Blocos Complexos (HTML aninhado)
- **Mapas:** `<tg-map lat="41.9" long="12.5" zoom="14"/>`
- **SlideShow:**
  ```html
  <tg-slideshow>
    ![](URL1)
    ![](URL2)
  </tg-slideshow>
  ```
- **Detalhes:** `<details><summary>Spoiler</summary>Conteúdo</details>`

---

## 3. Catálogo de Dialetos (50+)

O bot é compatível com a maioria das extensões Markdown modernas:

| Categoria | Exemplos de Dialetos |
|:--- |:--- |
| **Base** | Original, CommonMark, GFM (GitHub) |
| **Científico** | LaTeX, R Markdown, Quarto, Jupyter |
| **Documentação** | MkDocs, Docusaurus, Hugo, Jekyll |
| **Parsers** | Markdown-it, Remark, Pandoc, Mistune |
| **Anotações** | Obsidian, Logseq, Joplin, Zettlr |
| **Chat** | Discord, Slack, Reddit, Telegram V2 |

---

## 4. Referências Rápidas
- [Guia de referência Markdown](https://commonmark.org/help/)
- [Guia de formatação do Telegram](https://core.telegram.org/bots/api#formatting-options)
- [Projeto LaTeX](https://www.latex-project.org/)
- [GitHub Flavored Markdown](https://github.github.com/gfm/)
