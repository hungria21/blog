## Solução 1: Usar Marcadores de Posição

/legenda {n} - Título da Série
 ↑ Contador no início

/legenda EP{n} - Título
 ↑ Contador no meio  

/legenda Título da Série - Parte {n}
 ↑ Contador no final

/legenda EP{n:02d} - Título
 ↑ Com formatação específica


### Exemplos de uso 

| Comando | Resultado (Sequência) |
|---------|----------------------|
| /legenda {n} - Minha Série | 01 - Minha Série, 02 - Minha Série... |
| /legenda EP{n} | EP01, EP02, EP03... |
| /legenda Título - {n} | Título - 01, Título - 02... |
| /legenda {n:03d} - Série | 001 - Série, 002 - Série... |
| /legenda EP{n} - Parte | EP01 - Parte, EP02 - Parte... |