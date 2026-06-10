# Exemplos de Formatação Rich Message (Telegram Layer 227)

Esta lista contém exemplos de formatações suportadas pelo novo sistema de 'Rich Messages' do Telegram (Layer 227).

## 1. Cabeçalhos (Headings)
Suporta até 6 níveis de cabeçalho.
```markdown
# Título H1
## Título H2
### Título H3
#### Título H4
##### Título H5
###### Título H6
```

## 2. Fórmulas Matemáticas (LaTeX)
Suporta fórmulas em linha e em blocos independentes.
```markdown
Fórmula em linha: $E = mc^2$

Bloco de fórmula:
$$
\int_{a}^{b} f(x) \,dx = F(b) - F(a)
$$
```

## 3. Tabelas
Tabelas nativas usando a sintaxe clássica do Markdown.
```markdown
| Produto | Preço | Status |
| :--- | :---: | ---: |
| Bot MTProto | R$ 0,00 | Ativo |
| Layer 227 | - | Beta |
```

## 4. Listas e Checklists
Listas ordenadas, não ordenadas e listas de tarefas.
```markdown
- Item 1
- Item 2
  - Sub-item A

1. Primeiro
2. Segundo

- [ ] Tarefa Pendente
- [x] Tarefa Concluída
```

## 5. Citações (Blockquotes)
Citações simples e expansíveis.
```markdown
> Esta é uma citação simples.

> [!QUOTE]
> Esta é uma citação que pode ser configurada como colapsada no MTProto.
```

## 6. Colagem e SlideShow (Mídia)
Agrupamento de mídias anexadas à mensagem.
```markdown
[collage:1,2,3] - Agrupa as mídias 1, 2 e 3 em uma colagem.
[slideshow:4,5] - Agrupa as mídias 4 e 5 em um slideshow.
```

---
*Nota: Estas formatações são processadas nativamente pelo servidor do Telegram quando enviadas via `inputRichMessageMarkdown` no Layer 227.*
