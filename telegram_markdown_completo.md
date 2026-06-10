# Guia de Formatação Markdown para Telegram (MarkdownV2 & Beta 2026)

Este guia utiliza a sintaxe oficial do **MarkdownV2** do Telegram, acrescida dos novos recursos detectados nas versões Beta de 2026 (Títulos, Tabelas e Fórmulas).

---

### 1. Formatações Oficiais (MarkdownV2)
*Importante: No MarkdownV2, caracteres especiais como `_`, `*`, `[`, `]`, `(`, `)`, `~`, `\`, `>`, `#`, `+`, `-`, `=`, `|`, `{`, `}`, `.`, `!` devem ser escapados com `\` se não forem usados para formatação.*

*   **Negrito**: `*texto*`
*   **Itálico**: `_texto_`
*   **Sublinhado**: `__texto__`
*   **Taxado (Strikethrough)**: `~texto~`
*   **Spoiler**: `||texto||`
*   **Link**: `[nome do link](https://exemplo.com)`
*   **Citação (Blockquote)**: `> Texto da citação`
*   **Monoespaçado (Inline)**: `` `texto` ``

---

### 2. Novos Recursos Experimentais (Beta 2026 / MarkdownV3)
Estes recursos foram adicionados recentemente e podem exigir que o destinatário esteja na versão mais atual do Telegram.

#### Títulos (Headings)
Use o símbolo `#` seguido de um espaço.
*   `# Título Nível 1`
*   `## Título Nível 2`
*   `### Título Nível 3`

#### Tabelas (Tables)
Suporte nativo a tabelas Markdown.
```markdown
| Coluna A | Coluna B |
|----------|----------|
| Dado 1   | Dado 2   |
```

#### Fórmulas Matemáticas (KaTeX/LaTeX)
*   **Inline**: `$E=mc^2$`
*   **Bloco**:
    `$$`
    `x = \frac{-b \pm \sqrt{b^2 - 4ac}}{2a}`
    `$$`

#### Listas
*   **Lista com Marcadores**: `- Item`
*   **Lista Numerada**: `1. Item`

---

### 3. Blocos de Código
````markdown
```python
# Exemplo de código
print("Olá Mundo")
```
````

---

### Tabela de Copiar e Colar Rápido:
| Estilo | Sintaxe |
| :--- | :--- |
| **Negrito** | `*texto*` |
| *Itálico* | `_texto_` |
| __Sublinhado__ | `__texto__` |
| ~~Taxado~~ | `~texto~` |
| Spoiler | `||texto||` |
| `Código` | `` `texto` `` |
| [Link](https://t.me) | `[texto](link)` |

---
*Nota: Se os novos recursos (Títulos/Tabelas) não aparecerem formatados, o seu aplicativo pode precisar de atualização para suportar as entidades de 2026.*
