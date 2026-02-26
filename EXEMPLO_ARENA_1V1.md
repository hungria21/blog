# Exemplo de Script: Arena 1v1 com Substituição de Jogador

Este exemplo utiliza os nomes exatos dos blocos conforme definidos no `instrucoes_blocos_craftland.json`.

## 1. Configuração de Variáveis
Vá na categoria **Variável** e crie as seguintes variáveis de script:
*   `Lutador1`: (Tipo: **Qualquer tipo**) - Primeiro duelista.
*   `Lutador2`: (Tipo: **Qualquer tipo**) - Segundo duelista.
*   `Mortes1`: (Tipo: **Inteiro**) - Contador de mortes do Lutador 1.
*   `Mortes2`: (Tipo: **Inteiro**) - Contador de mortes do Lutador 2.
*   `FilaEspera`: (Tipo: **Lista**) - Lista para armazenar jogadores aguardando.

## 2. Início da Partida (Setup)
**Evento:** `Quando o jogo começa`
1.  **Ação:** Obter lista de todos os jogadores (salvar em variável temporária `ListaGeral`).
2.  **Ação:** `Definir variável` `Lutador1` = Obter índice 0 da `ListaGeral`.
3.  **Ação:** `Definir variável` `Lutador2` = Obter índice 1 da `ListaGeral`.
4.  **Lógica:** `Ciclo de todos os elementos (For Each)` (para cada `Jogador` em `ListaGeral` a partir do índice 2):
    *   **Ação:** `Adicionar à lista` `FilaEspera` (valor: `Jogador`).
    *   **Ação:** `Teletransportar` `Jogador` para Posição de Espera.
5.  **Ação:** `Teletransportar` `Lutador1` para Arena Posição A.
6.  **Ação:** `Teletransportar` `Lutador2` para Arena Posição B.

## 3. Controle de Eliminação e Troca
**Evento:** `Quando o jogador é eliminado` (Parâmetro: `Vítima`)

### Verificação do Lutador 1
1.  **Lógica:** `Se (If)` (`Vítima` == `Obter variável` `Lutador1`):
    *   **Ação:** `Definir variável` `Mortes1` = (`Obter variável` `Mortes1` + 1).
    *   **Lógica:** `Se (If)` (`Obter variável` `Mortes1` >= 4):
        *   **Ação:** `Exibir dica de texto` ("Lutador 1 atingiu o limite de mortes e será trocado").
        *   **Ação:** `Adicionar à lista` `FilaEspera` (valor: `Lutador1`).
        *   **Ação:** `Teletransportar` `Lutador1` para Posição de Espera.
        *   **Ação:** `Definir variável` `Lutador1` = `Obter da lista` `FilaEspera` (índice 0).
        *   **Ação:** `Remover da lista` `FilaEspera` (índice 0).
        *   **Ação:** `Definir variável` `Mortes1` = 0.
        *   **Ação:** `Teletransportar` `Lutador1` para Arena Posição A.
    *   **Senão:**
        *   **Ação:** `Teletransportar` `Lutador1` para Arena Posição A (Respawn).

### Verificação do Lutador 2
2.  **Lógica:** `Se (If)` (`Vítima` == `Obter variável` `Lutador2`):
    *   **Ação:** `Definir variável` `Mortes2` = (`Obter variável` `Mortes2` + 1).
    *   **Lógica:** `Se (If)` (`Obter variável` `Mortes2` >= 4):
        *   **Ação:** `Exibir dica de texto` ("Lutador 2 atingiu o limite de mortes e será trocado").
        *   **Ação:** `Adicionar à lista` `FilaEspera` (valor: `Lutador2`).
        *   **Ação:** `Teletransportar` `Lutador2` para Posição de Espera.
        *   **Ação:** `Definir variável` `Lutador2` = `Obter da lista` `FilaEspera` (índice 0).
        *   **Ação:** `Remover da lista` `FilaEspera` (índice 0).
        *   **Ação:** `Definir variável` `Mortes2` = 0.
        *   **Ação:** `Teletransportar` `Lutador2` para Arena Posição B.
    *   **Senão:**
        *   **Ação:** `Teletransportar` `Lutador2` para Arena Posição B (Respawn).
