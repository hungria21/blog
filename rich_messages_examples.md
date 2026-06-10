# Guia de Formatação Rich Message (Layer 227)

Este bot suporta GitHub Flavored Markdown (GFM) e extensões do Telegram Layer 227 para formatações ricas enviadas nativamente.

## 1. GitHub Flavored Markdown (GFM)
Formatos básicos de texto.
```markdown
**Negrito**
*Itálico*
~~Riscado~~
||Spoiler||
`Código em linha`

```python
# Bloco de código
def hello():
    print("Mundo")
```
```

## 2. Fórmulas Matemáticas (LaTeX)
Use `$` para fórmulas em linha e `$$` para blocos.
```markdown
O teorema de Pitágoras é $a^2 + b^2 = c^2$.

Bloco matemático:
$$
\frac{-b \pm \sqrt{b^2 - 4ac}}{2a}
$$
```

## 3. Tabelas Nativa
Sintaxe Markdown padrão para tabelas.
```markdown
| Comando | Descrição |
| :--- | :--- |
| /start | Inicia o bot |
| Texto | Converte para Rich |
```

## 4. Cabeçalhos
```markdown
# Nível 1
## Nível 2
### Nível 3
```

## 5. Listas e Checklists
```markdown
- Item A
- Item B
  - Sub-item

1. Primeiro
2. Segundo

[ ] Tarefa a fazer
[x] Tarefa feita
```

## 6. Agrupamento de Mídia (Collage/SlideShow)
*Nota: Requer mídias anexadas na mesma requisição.*
```markdown
[collage:1,2]
[slideshow:1,2,3]
```

---
*Processado via MTProto `InputRichMessageMarkdown` (Layer 227).*
