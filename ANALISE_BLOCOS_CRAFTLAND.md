# Análise de Blocos de Script - Free Fire Craftland

Este documento fornece uma análise detalhada dos blocos de script visual disponíveis no Free Fire Craftland, baseada nas imagens fornecidas. O sistema utiliza uma linguagem de programação visual baseada em blocos, semelhante ao Blockly ou Scratch, permitindo a criação de lógicas personalizadas para mapas.

## Categorias de Blocos

### 1. Eventos (Evento)
Blocos que disparam ações quando algo acontece no jogo.

#### Eventos Globais
*   **Início do jogo**: Disparado quando a partida começa.
*   **Início da rodada**: Disparado no início de cada rodada (fornece o index da rodada).
*   **Fim da rodada**: Disparado quando uma rodada termina.
*   **Início da fase**: Disparado no início de uma fase específica.
*   **Fim da fase**: Disparado no fim de uma fase específica.
*   **Na saída do jogador no meio da partida**: Disparado quando um jogador desconecta ou sai.
*   **Na eliminação do jogador**: Disparado quando um jogador é eliminado.
*   **Ao ajudar jogador**: Disparado quando um jogador presta assistência (ajuda a levantar).
*   **No dano causado pelo jogador**: Disparado quando um jogador causa dano (fornece atacante, alvo, tipo de dano, valor e parte do corpo).

#### Eventos Privados
*   **Evento privado**: Blocos de eventos que podem ser definidos para entidades específicas.

---

### 2. Ações (Ação)
Blocos que executam operações específicas no mundo ou nas entidades.

#### IA e Comportamento
*   **Habilitar Árvore de Comportamento Padrão**: Ativa ou desativa a IA padrão de uma entidade.
*   **Alvo de Perseguição**: Define qual entidade a IA deve perseguir.
*   **Patrulhar Até**: Envia uma entidade para patrulhar até um ponto (X, Y, Z).
*   **Patrulhar Ao Longo**: Define uma rota de patrulha através de múltiplos pontos.
*   **Criar Monstro**: Spawna uma criatura em uma posição específica com parâmetros de tipo e direção.

#### Cena e Ambiente
*   **Definir Skybox**: Altera o visual do céu (Ex: Dia, Noite).
*   **Encontrar Caminho**: Calcula uma rota entre dois pontos para navegação de IAs.

#### Combate
*   **Causar Dano**: Aplica dano a um alvo específico, permitindo definir o atacante e o tipo de arma/dano.

#### Interface (UI)
*   **Criar UI Incorporada**: Cria elementos de interface que fazem parte do mundo.
*   **Criar HUD personalizada**: Gera uma interface de usuário sobreposta para o jogador.
*   **Obter Widget da UI Personalizada**: Referencia um elemento específico da interface.
*   **Notificar Exibição de Dicas**: Mostra uma mensagem de texto (dica) na tela com cor e duração definidas.

#### Nível do Objeto
*   **Criar Objeto de Nível**: Instancia objetos pré-definidos (Ex: Villa de deck duplo).
*   **Entrar no Veículo**: Força um jogador a entrar em um veículo em um assento específico (Motorista/Passageiro).
*   **Criar Carga Aérea**: Spawna um airdrop no mapa.
*   **Começar a Pular de Paraquedas**: Inicia a sequência de queda livre e paraquedas para um jogador.

#### Biblioteca Padrão
*   **Tem Componente**: Verifica se uma entidade possui um componente específico.
*   **Obter Filho por Nome**: Busca um objeto filho dentro de uma hierarquia pelo nome.
*   **Adicionar Comentário**: Bloco organizacional para documentar o script (não executa ação).

---

### 3. Dados (Dados)
Blocos relacionados à manipulação de informações e tipos de dados.

#### Matemática
*   **Arredondar / Arredondar para Baixo**: Funções matemáticas para tratar números decimais.
*   **Funções Trigonométricas**: Sin, Cos, Tan, Asin, Acos, ATan2 para cálculos de ângulos e vetores.

#### Vetores (Vector)
*   Manipulação de coordenadas X, Y, Z (Vetor3) e X, Y (Vetor2).

#### Enums
*   **Tipo de Equipamento**: Seleção de armas e itens (Arma Primária A, etc).
*   **Tipo de Dinheiro**: Seleção de moedas do jogo.
*   **Tipo de Buff**: Seleção de efeitos de bônus.

---

### 4. Jogo (Jogo)
Blocos de alto nível que controlam as regras e o estado da partida.

#### Jogador
*   **Adicionar HP**: Cura ou remove vida de um jogador.
*   **Teleportar**: Move um jogador instantaneamente para novas coordenadas e rotação.
*   **Definir Status de Movimento**: Habilita ou desabilita a capacidade de andar de todos os jogadores.
*   **Definir Habilidades**: Atribui habilidades específicas a um jogador.

#### Equipe
*   **Definir Equipe Atacável**: Define se uma equipe pode ser atacada por outra.
*   **Entrar na equipe / Entrar em nova equipe**: Gerencia a afiliação de jogadores a times.

#### Economia
*   Controle de dinheiro e recursos financeiros dentro da partida.

---

### 5. Lógica (Lógica)
Blocos de controle de fluxo de execução.

*   **Se (If)**: Execução condicional.
*   **caso/ou**: Alternativas condicionais (Else if / Else).
*   **Ciclo condicional (While)**: Repetição enquanto uma condição for verdadeira.
*   **Ciclo do alcance (For range)**: Repetição por um número definido de vezes ou intervalo.
*   **Ciclo de todos os elementos (For each)**: Itera sobre uma lista de objetos ou jogadores.
*   **Quebrar ciclo / Continue**: Controle interno de loops.

---

### 6. Variáveis e Funções
*   **Variável temporária**: Criação de variáveis locais com tipos específicos (Bool, Inteiro, Flutuante, Cadeia/String, Vetor, Lista).
*   **Voltar (Return)**: Finaliza uma função e opcionalmente retorna um valor.

---

## Observações Técnicas
*   **Tipagem**: O sistema parece ser fortemente tipado, exigindo que os tipos de dados (Inteiro, Vetor, Entidade) coincidam nas conexões dos blocos.
*   **Referenciação**: Muitos blocos utilizam o parâmetro "Alvo" (Target), que pode ser o "Jogador que disparou o evento", uma entidade específica ou uma variável.
*   **Coordenadas**: O sistema utiliza um sistema de coordenadas 3D (X, Y, Z) para quase todas as ações espaciais.
