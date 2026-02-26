# Análise Detalhada dos Blocos de Script - Free Fire Craftland

Esta documentação fornece uma visão técnica e estruturada do sistema de scripting visual do Free Fire Craftland, baseada no guia oficial de instruções (`instrucoes_blocos_craftland.json`).

## 1. Categorias de Blocos
O sistema é organizado em categorias lógicas, cada uma com propósitos específicos:

### A. Evento (Red - "Hat" Blocks)
Estes blocos iniciam a execução. São classificados em:
*   **Global:** Eventos que afetam o jogo como um todo (ex: "Quando o jogo começa", "Quando o jogador entra no jogo").
*   **Privado:** Eventos específicos de um jogador ou entidade (ex: "Quando o jogador é eliminado", "Quando o jogador causa dano").
*   **Área:** Gatilhos baseados em posicionamento espacial (ex: "Quando o jogador entra na área").

### B. Ação (Comandos)
Blocos que executam tarefas ativas, divididos em:
*   **IA:** Controle de bots ("Controle de IA").
*   **Lógica:** Comandos de tempo e fluxo externo ("Esperar", "Executar script").
*   **Combate:** Manipulação de saúde e dano ("Dar dano", "Curar", "Definir HP Máximo").
*   **Interface (UI):** Comunicação visual com o jogador ("Exibir dica de texto", "Enviar mensagem de chat").
*   **Inventário:** Gerenciamento de itens e armas.

### C. Dados (Valores e Operações)
Utilizados para fornecer informações aos blocos de ação ou lógica:
*   **Básico:** Constantes como Número, Cadeia, Vetor3, Bool e referências a Entidades. Inclui também o "Comparador" (==, !=, >, etc.) e "Operador Lógico" (e, ou).
*   **Matemática:** Operações aritméticas e funções como Raiz Quadrada e Número Aleatório.
*   **Lista:** Operações de coleção (Adicionar à lista, Obter da lista, Tamanho da lista).
*   **Textos (Cadeia):** Manipulação de strings.
*   **Vetor:** Cálculos espaciais (Distância, Normalizar).

### D. Lógica (Controle de Fluxo - "C-Blocks")
Controlam como e quando as ações são executadas:
*   **Se (If) / Se / caso/ou (If/Else):** Tomada de decisão.
*   **Ciclo condicional (While):** Repetição baseada em condição.
*   **Ciclo do alcance (For Range):** Repetição baseada em contador.
*   **Ciclo de todos os elementos (For Each):** Iteração sobre listas (o antigo "para cada" ou "percorrer").
*   **Quebrar ciclo (Break) / Continue para o próximo:** Controle interno de loops.

### E. Variável
*   **Variável temporária:** Escopo local à execução atual.
*   **Definir/Obter variável:** Gerenciamento de estado.
*   **Tipos Suportados:** Bool, Inteiro, Flutuante, Cadeia, Vetor2, Vetor3, Lista, Qualquer tipo.

### F. Função
Permite modularização ("Definir função", "Chamar função", "Voltar com valor").

## 2. Tipos de Arquivos
*   `.fcg`: Script de bloco.
*   `.fcc`: Bibliotecas padrão (Standard Libraries).

## 3. Fluxo Técnico
1.  **Gatilho:** Um `Evento` é disparado por uma ação no jogo ou tempo.
2.  **Verificação:** Blocos de `Lógica` (Se) filtram se a ação deve ocorrer.
3.  **Execução:** Blocos de `Ação` alteram o estado do mundo, jogador ou interface.
4.  **Processamento:** Blocos de `Dados` e `Variáveis` fornecem os parâmetros necessários para as ações.
