# Relatório de Blocos de Script - Free Fire Craftland

Analisei os arquivos de projeto (`ProjectData_slot_1.bytes` e `ProjectData_slot_2.bytes`) e encontrei um total de **49 blocos únicos**.

## Evento
- **OnAwake**: Acionado quando o bloco ou script é inicializado.
- **OnClickHudButton**: Acionado quando um botão da interface (HUD) é clicado.
- **OnFixedUpdate**: Acionado em cada tick fixo da física/lógica do jogo.
- **OnMatchStart**: Acionado quando a partida começa.
- **OnObtainItem**: Acionado quando um jogador obtém um item.
- **OnPlayerAdd**: Acionado quando um novo jogador entra na partida.
- **OnPlayerDead**: Acionado quando um jogador morre.
- **OnUseItem**: Acionado quando um item é usado.
- **OnWield**: Acionado quando um jogador empunha uma arma ou item.

## Ação
- **AddItemToCharacter**: Adiciona um item ao inventário de um personagem.
- **CreateCustomHud**: Cria uma interface de usuário personalizada.
- **CreateInternalHud**: Cria uma interface de usuário padrão do sistema.
- **ModifyFormulaProperty**: Modifica propriedades baseadas em fórmulas (ex: dano, velocidade).
- **RemovePlayerClothIDByWardrobeType**: Remove vestimentas do jogador baseadas no tipo de guarda-roupa.
- **ReviveOnNextFrame**: Revive o jogador no próximo quadro de execução.
- **SetEntityProperty**: Define uma propriedade (PV, posição, etc.) de uma entidade.
- **SetReplicationDataSmoothly**: Sincroniza dados entre jogadores de forma suave.
- **TeleportPlayerPositionAndForward**: Teletransporta o jogador para uma posição e direção específicas.
- **WaitForSeconds**: Pausa a execução do script por um tempo determinado.

## Dados
- **AllPlayers**: Retorna uma lista com todos os jogadores na partida.
- **ColorGetter**: Obtém ou define valores de cores.
- **ConstBool**: Valor constante booleano (Verdadeiro/Falso).
- **ConstFloatOrInt**: Valor constante numérico (Inteiro ou Decimal).
- **ConstString**: Valor constante de texto.
- **ConstVector3**: Coordenada constante tridimensional (X, Y, Z).
- **EntityGetter**: Obtém uma referência a uma entidade específica.
- **EquipmentSlot**: Refere-se a um espaço de equipamento (ex: Mochila, Arma).
- **GetEntityProperty**: Recupera o valor de uma propriedade de uma entidade.
- **GetPlayerBagItemCount**: Conta a quantidade de um item específico na mochila do jogador.
- **GetPlayerEquipments**: Retorna a lista de equipamentos atuais de um jogador.
- **IconType**: Define o tipo de ícone usado em interfaces ou itens.
- **InternalHudType**: Define o tipo de interface padrão do sistema.
- **ItemGoodsIDType**: ID de identificação de um item específico do jogo.
- **NewVector3**: Cria um novo vetor de posição ou direção.
- **PropertyModifyType**: Define o método de modificação de propriedade (soma, substituição, etc).
- **RandomFloat**: Gera um número decimal aleatório.
- **ThisEntity**: Refere-se à entidade que está executando o script no momento.
- **WardrobeType**: Especifica a categoria de vestimenta do jogador.

## Jogo
- **EndCurrentPhase**: Finaliza a fase ou rodada atual do jogo.
- **PauseGame**: Pausa o processamento do estado do jogo.

## Lógica
- **Comparer**: Compara dois valores (igual, maior, menor, diferente).
- **ForEach**: Executa uma ação para cada item dentro de uma lista.
- **If**: Estrutura condicional (Se / Então).
- **LogicalOperation**: Executa operações lógicas como E (AND), OU (OR) ou NÃO (NOT).
- **While**: Executa um bloco de código repetidamente enquanto uma condição for verdadeira.

## Variável
- **DefLocalVar**: Define e inicializa uma nova variável local.
- **GetLocalVar**: Recupera o valor armazenado em uma variável local.

## Função
- **CallActionFunc**: Executa uma função de ação previamente definida.
- **DefFuncWithoutReturn**: Define uma função de script que executa tarefas sem retornar valor.

## Análise do Objeto "telegram"

Encontrei o objeto nomeado **"telegram"** no arquivo `ProjectData_slot_2.bytes`.
- **ID do Objeto**: 1771757735001
- **Grafo Vinculado**: GR_76b56b2e-d429-4828-9d67-1323c4ae93e0
- **Estrutura de Script**: OnMatchStart -> SetEntityProperty -> PauseGame -> If (Condition).
