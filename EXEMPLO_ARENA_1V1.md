# Exemplo de Script de Bloco: Arena 1v1 com Fila de Espera

Este guia descreve como montar a lógica de blocos para uma arena de 50x50 onde dois jogadores lutam e, se um deles morrer 4 vezes, ele é substituído por um jogador da fila.

## 1. Variáveis Necessárias (Escopo de Script)
Crie as seguintes variáveis na categoria **Variáveis**, utilizando os tipos exatos do editor:
*   `Lutador1`: (Tipo: **Qualquer tipo**) - Referência ao primeiro duelista (entidade jogador).
*   `Lutador2`: (Tipo: **Qualquer tipo**) - Referência ao segundo duelista (entidade jogador).
*   `Mortes1`: (Tipo: **Inteiro**) - Contador de mortes do Lutador 1.
*   `Mortes2`: (Tipo: **Inteiro**) - Contador de mortes do Lutador 2.
*   `FilaEspera`: (Tipo: **Modelo de lista <Qualquer tipo>**) - Lista de jogadores aguardando a vez.

## 2. Lógica de Inicialização
**Evento:** `Ao Iniciar Partida` (ou um gatilho de início).
1.  **Obter todos os jogadores** e salvar em uma lista temporária.
2.  **Definir Lutador1** como o primeiro jogador da lista.
3.  **Definir Lutador2** como o segundo jogador da lista.
4.  **Para cada** jogador restante na lista:
    *   Adicionar o jogador na `FilaEspera`.
    *   Teleportar para a "Área de Espera" (fora da arena).
5.  **Teleportar** `Lutador1` para a Posição A da Arena.
6.  **Teleportar** `Lutador2` para a Posição B da Arena.

## 3. Lógica de Substituição (O Coração do Script)
**Evento:** `Ao Morrer` (Trigger: Jogador que morreu).

Use um bloco **Se (If)** para verificar quem morreu:

### Caso seja o Lutador 1:
*   **Se** (Jogador que morreu == `Lutador1`):
    *   **Alterar Variável** `Mortes1` (Aumentar em 1).
    *   **Se** (`Mortes1` >= 4):
        *   **Ação:** Teleportar `Lutador1` para a "Área de Espera".
        *   **Ação:** Adicionar `Lutador1` ao final da `FilaEspera`.
        *   **Ação:** **Definir Lutador1** como o primeiro elemento da `FilaEspera` (índice 0).
        *   **Ação:** Remover primeiro elemento da `FilaEspera`.
        *   **Ação:** Definir `Mortes1` como 0.
        *   **Ação:** Teleportar o NOVO `Lutador1` para a Posição A da Arena.
    *   **Senão** (Ainda não morreu 4 vezes):
        *   **Ação:** Teleportar `Lutador1` de volta para a Posição A (Respawn na arena).

### Caso seja o Lutador 2:
*   **Se** (Jogador que morreu == `Lutador2`):
    *   **Alterar Variável** `Mortes2` (Aumentar em 1).
    *   **Se** (`Mortes2` >= 4):
        *   **Ação:** Teleportar `Lutador2` para a "Área de Espera".
        *   **Ação:** Adicionar `Lutador2` ao final da `FilaEspera`.
        *   **Ação:** **Definir Lutador2** como o primeiro elemento da `FilaEspera` (índice 0).
        *   **Ação:** Remover primeiro elemento da `FilaEspera`.
        *   **Ação:** Definir `Mortes2` como 0.
        *   **Ação:** Teleportar o NOVO `Lutador2` para a Posição B da Arena.
    *   **Senão** (Ainda não morreu 4 vezes):
        *   **Ação:** Teleportar `Lutador2` de volta para a Posição B (Respawn na arena).

## 4. Dicas Adicionais
*   **Área de Arena:** Certifique-se de que as coordenadas da Posição A e B estejam dentro do espaço 50x50 planejado.
*   **Reset de Itens:** Ao teleportar o novo jogador para a arena, pode ser útil usar a ação "Curar Totalmente" e "Resetar Mochila" (opcional).
*   **Mensagens:** Use o bloco "Exibir Notificação" para avisar a todos: *"O jogador [Nome] entrou na arena!"*.
