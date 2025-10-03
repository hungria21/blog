## Solução 1: Usar Marcadores de Posição

/legenda {n} - Título da Série
 ↑ Contador no início

/legenda EP{n} - Título
 ↑ Contador no meio  

/legenda Título da Série - Parte {n}
 ↑ Contador no final

/legenda EP{n:02d} - Título
 ↑ Com formatação específica


### Exemplos de uso: 

| Comando | Resultado (Sequência) |
|---------|----------------------|
| /legenda {n} - Minha Série | 01 - Minha Série, 02 - Minha Série... |
| /legenda EP{n} | EP01, EP02, EP03... |
| /legenda Título - {n} | Título - 01, Título - 02... |
| /legenda {n:03d} - Série | 001 - Série, 002 - Série... |
| /legenda EP{n} - Parte | EP01 - Parte, EP02 - Parte... |


### Prompt para correção:

No código fornecido, a função `parse_caption_format()` está separando incorretamente o prefixo com espaços.

Quando o usuário envia '/legenda S01E01', o bot deve capturar:
- prefix: 'S01E'
- number: '01'
- suffix: ''

Mas atualmente o código está capturando apenas 'S' como prefix e adicionando um espaço, resultando em 'S 01E01'.

O primeiro padrão regex da lista `PATTERNS` precisa ser corrigido para capturar corretamente 'S01E' como prefixo completo em formatos como S01E01, S02E15, T01E03, etc.

Além disso, a lógica que adiciona espaço extra ao prefixo (a linha `prefix += " "`) deve ser removida ou corrigida, pois está causando separação indesejada nos formatos que já estão corretos.

Resumindo, corrija o erro do prefixo e deixe mais flexível caso o usuário queira usar com ou sem espaço e pra isso basta ele enviar como desejar. 

Exemplo: 
- /legenda S01E01
- /legenda S 01E01