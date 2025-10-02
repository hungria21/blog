# Análise e Planejamento: Sistema Flexível de Legendas Sequenciais

## 📋 Formato Atualmente Reconhecido

Analisando o código atual, o bot reconhece **apenas um formato**:

### Formato Existente:
```
Padrão: <Prefixo opcional> <Número>
Regex: r'^(.*?)
---

## planejamento com Novos Formatos para Maior Flexibilidade

### **Categoria 1: Animes**
```
- EP01, EP 01, Ep01, Ep 01
- Episode 01, Episode01
- Episódio 01, Episódio01
- 第01話, 第1話 (formato japonês)
- [01], (01), {01}
- E01, E 01
- Cap 01, Capítulo 01
- OVA 01, OVA01
- Especial 01
- Movie 01, Filme 01
```

### **Categoria 2: Séries/TV Shows**
```
- S01E01, S1E1, S01 E01
- Temporada 1 Episódio 01
- T01E01, T1E1
- 1x01, 1x1
- Season 1 Episode 01
```

### **Categoria 3: Documentários**
```
- Parte 01, Part 01
- Capítulo 01, Chapter 01
- Seção 01, Section 01
- Segmento 01
- Vol 01, Volume 01
- Bloco 01
```

### **Categoria 4: Áudio/Música**
```
- Faixa 01, Track 01
- #01, N° 01, Nº 01
- Audio 01, Áudio 01
- Mix 01, Remix 01
- Tema 01
```

### **Categoria 5: Aulas/Cursos**
```
- Aula 01, Lesson 01, Class 01
- Módulo 01, Module 01
- Unidade 01, Unit 01
- Lição 01
- Tutorial 01
```

### **Categoria 6: Formatos Genéricos**
```
- 01, 001, 0001 (número puro)
- Arquivo 01, File 01
- Item 01
- Vídeo 01, Video 01
- #01
```

---

## 🔧 Planejamento da Lógica de Reconhecimento

### **Abordagem 1: Sistema de Padrões Múltiplos (Recomendado)**

**Conceito:** Criar uma lista de regex patterns que o bot testa sequencialmente até encontrar um match.

**Estrutura da lógica:**
```
1. Receber input do usuário: "/legenda [formato]"
2. Iterar sobre lista de padrões regex pré-definidos
3. Para cada padrão, tentar fazer match com o input
4. Quando encontrar match, extrair:
   - Prefixo (tudo antes do número)
   - Número inicial (com padding original)
   - Sufixo (tudo depois do número, se houver)
5. Armazenar no estado:
   - prefixo completo
   - sufixo completo
   - contador inicial
   - padding (zeros à esquerda)
6. Gerar próximas legendas concatenando: prefixo + número + sufixo
```

**Padrões Regex a implementar:**
```python
PATTERNS = [
    # S01E01, T01E01, etc
    r'^([ST])(\d+)[Ee](\d+)$'
    
    # 1x01, 1x1
    r'^(\d+)x(\d+)$'
    
    # EP01, Ep01, E01 (colado)
    r'^([EeÉé][Pp]?|Cap(?:ítulo)?|OVA)(\d+)$'
    
    # EP 01, Ep 01, E 01 (com espaço)
    r'^([EeÉé][Pp]?|Episode|Episódio|Cap(?:ítulo)?|OVA)\s+(\d+)$'
    
    # [01], (01), {01}
    r'^([\[\(\{])(\d+)([\]\)\}])$'
    
    # Parte 01, Part 01, etc
    r'^(Parte|Part|Cap(?:ítulo)?|Chapter|Volume?|Aula|Lesson)\s+(\d+)$'
    
    # Faixa 01, Track 01, #01
    r'^(Faixa|Track|#|N[º°]|Áudio|Audio)\s*(\d+)$'
    
    # Número puro no final (fallback, já existente)
    r'^(.*?)(\d+)$'
]
```

---

### **Abordagem 2: Sistema de Templates com Placeholders**

**Conceito:** Usuário define um template com marcador especial para o número.

**Exemplo de uso:**
```
/legenda EP{N} → EP1, EP2, EP3...
/legenda S01E{N} → S01E1, S01E2, S01E3...
/legenda [Temporada 1] Episódio {N} → [Temporada 1] Episódio 1, ...
```

**Lógica:**
```
1. Detectar marcador {N} ou {NUM} no input
2. Separar template em: parte_antes + marcador + parte_depois
3. Perguntar ao usuário o número inicial e padding
4. Gerar legendas substituindo o marcador
```

---

### **Abordagem 3: Sistema Híbrido (Mais Flexível)**

**Conceito:** Combinar detecção automática com opção de template manual.

**Fluxo:**
```
1. Tentar detecção automática com os padrões regex
2. Se falhar, sugerir ao usuário usar template com {N}
3. Permitir override manual: /legenda_custom <template> <inicio> <padding>
```

---

## 🎨 Casos Especiais a Considerar

### **1. Formatos com Múltiplos Números**
```
S01E01 → Como incrementar?
Opção A: Apenas o último número (E01 → E02)
Opção B: Perguntar ao usuário qual incrementar
Opção C: Sistema de "variáveis múltiplas"
```

### **2. Preservação de Formatação**
```
EP01 vs Ep01 vs ep01 → Manter case original
[01] vs (01) vs {01} → Manter delimitadores originais
```

### **3. Números com Separadores**
```
01-A, 01.1, 01_parte_1
Decisão: Aceitar ou rejeitar?
```

### **4. Sufixos Variáveis**
```
EP01 - Título Variável
Como lidar: Ignorar tudo após o número na detecção inicial
```

---

## 📝 Prompt de Implementação Sugerida

**"Crie um sistema flexível de reconhecimento de formatos de legenda sequencial que:**

1. **Mantenha compatibilidade total** com o formato atual (prefixo opcional + número)

2. **Adicione suporte para múltiplos padrões** através de uma lista de regex patterns que cubram:
   - Formatos de animes (EP01, Ep 01, Episode 01, OVA 01, Cap 01, [01])
   - Formatos de séries (S01E01, 1x01, T01E01)
   - Formatos de documentários (Parte 01, Volume 01, Capítulo 01)
   - Formatos de áudio (Faixa 01, Track 01, #01)
   - Formatos de aulas (Aula 01, Módulo 01, Lição 01)
   - Números puros e formatos genéricos

3. **Preserve a formatação original**, incluindo:
   - Case (maiúsculas/minúsculas)
   - Espaçamento
   - Delimitadores ([], (), {})
   - Padding de zeros

4. **Extraia e armazene**:
   - Prefixo completo (tudo antes do número)
   - Sufixo completo (tudo depois do número, se houver)
   - Número inicial com padding original
   - Pattern usado (para regeneração consistente)

5. **Implemente lógica de fallback**: Se nenhum padrão específico for reconhecido, use o sistema atual (número no final)

6. **Adicione validação**: Informe o usuário sobre o formato detectado e exemplo da sequência antes de ativar

7. **Mantenha a arquitetura assíncrona** e o sistema de fila existente sem alterações

8. **Teste com exemplos** de cada categoria para garantir reconhecimento correto"

---

## ✅ Benefícios da Abordagem Proposta

- ✨ **Flexibilidade máxima** sem aumentar complexidade para o usuário
- 🔄 **Retrocompatibilidade** garantida
- 🌍 **Suporte multilíngue** (português, inglês, japonês)
- 🎯 **Detecção inteligente** sem necessidade de comandos diferentes
- 🔧 **Extensível** para adicionar novos formatos facilmente
- 📊 **Mantém performance** usando regex eficientes