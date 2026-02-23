# Lógica de Arena X1 - Passo a Passo (Free Fire Craftland)

Este guia descreve como montar a lógica solicitada para uma arena 50x50 com sistema de substituição após 4 mortes.

## 1. Variáveis Necessárias
No menu **Variáveis**, crie as seguintes:
- `FilaEspera` (Tipo: Modelo de lista <Entidade>) - Armazena quem está fora da arena.
- `Duelista1` (Tipo: Entidade) - O primeiro jogador no X1.
- `Duelista2` (Tipo: Entidade) - O segundo jogador no X1.
- `Mortes1` (Tipo: Inteiro) - Contador de mortes do Duelista 1.
- `Mortes2` (Tipo: Inteiro) - Contador de mortes do Duelista 2.

## 2. Evento: Entrada de Jogadores
Este bloco gerencia quem entra na fila ou ocupa as vagas vazias no X1.

**Blocos:**
1. **Evento**: `Quando o jogador entra no jogo`
2. **Lógica**: `Se` (Verificação vazia: `Duelista1`)
   - **Ação**: `Definir variável` (`Duelista1` = `Jogador`)
   - **Ação**: `Teletransportar` (`Jogador`, Destino: Spawn A)
3. `Se / caso/ou` (Verificação vazia: `Duelista2`)
   - **Ação**: `Definir variável` (`Duelista2` = `Jogador`)
   - **Ação**: `Teletransportar` (`Jogador`, Destino: Spawn B)
4. `Caso/ou` (Senão)
   - **Dados - Lista**: `Adicionar à lista` (`FilaEspera`, `Jogador`)
   - **Ação**: `Teletransportar` (`Jogador`, Destino: Sala de Espera)

## 3. Evento: Controle de Eliminação e Substituição
Este é o núcleo da lógica de substituição.

**Blocos:**
1. **Evento**: `Quando o jogador é eliminado`
2. **Lógica**: `Se` (`Vítima` == `Duelista1`)
   - **Matemática**: `Definir variável` (`Mortes1` = `Mortes1` + 1)
   - **Lógica**: `Se` (`Mortes1` >= 4)
     - **Ação**: `Teletransportar` (`Vítima`, Destino: Sala de Espera)
     - **Dados - Lista**: `Adicionar à lista` (`FilaEspera`, `Duelista1`)
     - **Ação**: `Definir variável` (`Mortes1` = 0)
     - **Lógica**: `Se` (`Tamanho da lista(FilaEspera)` > 0)
       - **Ação**: `Definir variável` (`Duelista1` = `Obter da lista(FilaEspera, 0)`)
       - **Dados - Lista**: `Remover da lista` (índice 0)
       - **Ação**: `Teletransportar` (`Duelista1`, Destino: Spawn A)
       - **Ação**: `Exibir dica de texto` ("Um novo lutador entrou na arena!")

3. **Lógica**: `Se` (`Vítima` == `Duelista2`)
   - *Repita a lógica acima trocando `Duelista1` por `Duelista2`, `Mortes1` por `Mortes2` e `Spawn A` por `Spawn B`.*

## 4. Dicas Adicionais
- Use o bloco **Dados - Básico - Comparador** para verificar as mortes e as entidades.
- Use **Ação - Interface** para avisar aos jogadores quem é o próximo na fila.
- Certifique-se de que a área 50x50 esteja delimitada por barreiras para que os jogadores não saiam do X1 prematuramente.
