# Análise de Arquivos Free Fire Craftland

Esta análise detalha a estrutura e o conteúdo dos arquivos do Free Fire Craftland encontrados no diretório `FreeFire/`. O projeto parece ser um mapa de "Guarda-Roupa" (Wardrobe/Outfitter), permitindo que os jogadores troquem de roupas através de uma interface customizada.

## Visão Geral dos Arquivos

| Arquivo | Descrição | Formato |
| :--- | :--- | :--- |
| `ProjectData_slot_1.bytes` | Dados principais do mapa e lógica de script. | Protobuf + GZIP |
| `UserLevelData_1.bytes` | Metadados de interface, textos de interação e mapeamento de funções. | Protobuf |
| `SceneReview_1.bytes` | Imagens de visualização (screenshots) do mapa. | Múltiplos arquivos PNG |
| `ProjectEditRecord_slot_1.meta.json` | Registro de edição do projeto (timestamps, flags). | JSON |

## Lógica de Script (Visual Scripting)

Os seguintes blocos de script foram identificados no arquivo `ProjectData_slot_1.bytes`:

### Eventos
- `OnAwake`: Disparado quando a entidade ou o mapa é carregado.
- `OnClickHudButton`: Disparado quando um jogador clica em um botão da interface (HUD) customizada.

### Ações
- `DefFuncWithoutReturn`: Define uma função personalizada sem valor de retorno.
- `CallActionFunc`: Chama uma função ou ação definida.
- `RemovePlayerClothIDByWardrobeType`: Remove uma peça de roupa do jogador baseada na categoria (ex: remover o "Top" atual).
- `SetReplicationDataSmoothly`: Sincroniza dados entre os jogadores de forma suave (interpolação).
- `CreateCustomHud`: Cria elementos de interface de usuário personalizados.

### Dados e Variáveis
- `GetLocalVar`: Obtém o valor de uma variável local.
- `GetEntityProperty`: Acessa propriedades de uma entidade (ex: jogador).
- `WardrobeType`: Tipo de dado que define categorias de vestuário.
- `ConstFloatOrInt`: Valores numéricos constantes.

## Interface de Usuário (HUD) e Interações

O arquivo `UserLevelData_1.bytes` contém textos que sugerem as seguintes interações disponíveis para os jogadores:

- **Categorias de Equipamento:**
  - `EQUIP ONESIE` (Macacão)
  - `EQUIP TOP` (Camisa/Superior)
  - `EQUIP BOTTOM` (Calça/Inferior)
  - `EQUIP SHOE` (Sapato)
  - `EQUIP HEAD` (Cabeça/Chapéu)
  - `EQUIP MASK` (Máscara)
  - `EQUIP FACEPAINT` (Pintura Facial)

Os textos de interface utilizam códigos de cores como `[ffff00]` (Amarelo) para destaque.

## Metadados do Projeto

- **Última Edição:** Registrada em timestamps que apontam para o início de 2026 (conforme `ProjectEditRecord_slot_1.meta.json`).
- **Visualização:** O arquivo `SceneReview_1.bytes` contém pelo menos 5 capturas de tela em formato PNG que mostram o layout do mapa, incluindo limites de área (bordas azuis) e pontos de spawn/objetivos (bandeiras).

## Conclusão

Os arquivos compõem um sistema funcional de customização de personagens dentro do Free Fire Craftland. A lógica está organizada de forma modular, utilizando funções para gerenciar a troca de diferentes partes do vestuário, integradas a uma interface de usuário personalizada.
