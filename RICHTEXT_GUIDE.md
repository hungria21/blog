# Guia Mestre de Formatação: Rich Messages (Bot API 10.1)

Este guia contém todas as informações sobre as "Rich Messages" (Junho 2026) e o Catálogo de Dialetos Markdown suportados.

---

## 1. Rich Markdown (Novos Recursos)

O Telegram v10.1 expandiu o Markdown para suportar estruturas complexas.

### Cabeçalhos, Tabelas e Fórmulas
- **Headings:** `# Nível 1` até `###### Nível 6`
- **Tabelas:**
```markdown
| Recurso | Descrição |
|:---|:---:|
| Tabelas | Nativas e Alinhadas |
| LaTeX | $E = mc^2$ |
```
- **Matemática:** `$inline$` ou `$$bloco$$`. Suporta também blocos ` ```math `.
- **Checklists:** `- [ ] Pendente` e `- [x] Concluído`.

### Blocos Especiais
- **Mapas:** `<tg-map lat="41.9" long="12.5" zoom="14"/>`
- **Slideshow:**
```html
<tg-slideshow>
![](URL1)
![](URL2)
<figcaption>Legenda do Slide</figcaption>
</tg-slideshow>
```
- **Detalhes (Expandível):**
```html
<details>
  <summary>Clique aqui</summary>
  Conteúdo oculto.
</details>
```

---

## 2. Catálogo de Sintaxes e Dialetos

### Base e Padronização
- [Markdown Original](https://daringfireball.net/projects/markdown/)
- [CommonMark](https://commonmark.org/)
- [GFM (GitHub)](https://github.github.com/gfm/)

### Ecossistema e Parsers
- [Markdown-it](https://github.com/markdown-it/markdown-it)
- [Remark](https://remark.js.org/)
- [Pandoc](https://pandoc.org/)
- [Mistune (Python)](https://python-markdown.github.io/)

### Científico e Documentação
- [LaTeX](https://www.latex-project.org/)
- [MDX](https://mdxjs.com/)
- [Quarto](https://quarto.org/)
- [Docusaurus](https://docusaurus.io/)
- [MkDocs](https://www.mkdocs.org/)

### Outras Linguagens Poderosas
- [AsciiDoc](https://asciidoc.org/)
- [reStructuredText](https://docutils.sourceforge.io/rst.html)
- [Org Mode](https://orgmode.org/)
- [Typst](https://typst.app/)
- [Djot](https://djot.net/)

---

## 3. Guia de Referência Rápida (Boas-vindas)

Ao iniciar o bot, você terá acesso rápido a:
1. **Guia de referência Markdown:** Referência universal.
2. **Guia de formatação do Telegram:** Regras específicas da plataforma.
3. **GEM para auxílio:** Ferramentas de suporte à escrita.
4. **Estilo de IA:** Conversão inteligente para Markdown.

---

## 4. Limites Técnicos
- 32.768 caracteres por mensagem.
- 500 blocos de conteúdo.
- 16 níveis de aninhamento.
- 50 mídias por colagem/slideshow.
