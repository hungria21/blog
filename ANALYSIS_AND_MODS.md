# Análise do Jogo: Super Mario World Infinite Lives

## Informações do Arquivo
- **Nome:** Super_Mario_World_InfiniteLives.smc
- **Tamanho:** 524.800 bytes (512 KB + 512 bytes de header)
- **Versão:** Super Mario World (USA)
- **Header:** SMC (512 bytes)
- **Checksum Interno:** Originalmente `0xA0DA`, atualizado para `0xA80D` após modificações.

## Análise Inicial
O arquivo fornecido já continha uma modificação para **Vidas Infinitas**. A instrução original `DEC $0DBE` (localizada no endereço de memória `$00D2D8`, correspondente ao offset `0x52D8` no arquivo com header) foi substituída por instruções `NOP` (`EA EA EA`), impedindo a perda de vidas.

---

## Modificações Realizadas

Foram aplicadas as seguintes 5 modificações adicionais para melhorar a experiência de jogo:

### 1. Tempo Infinito
- **Descrição:** Impede que o cronômetro da fase diminua.
- **Offset PC:** `0x103F`
- **Alteração:** `DE 31 0F` (DEC $0F31,X) -> `EA EA EA` (NOP)

### 2. Pulo Infinito (Air Jump)
- **Descrição:** Permite que o Mario pule novamente enquanto estiver no ar.
- **Offset PC:** `0x4EEF`
- **Alteração:** `D0 2B` (BNE) -> `EA EA` (NOP)

### 3. Estrela Infinita
- **Descrição:** O efeito da Estrela de Invencibilidade não expira.
- **Offset PC:** `0x64E0`
- **Alteração:** `CE 90 14` (DEC $1490) -> `EA EA EA` (NOP)

### 4. Voo Infinito (Capa)
- **Descrição:** Impede que o timer de voo da capa suba, permitindo voar indefinidamente sem perder altitude.
- **Offset PC:** `0x5AFB`
- **Alteração:** `EE 9F 14` (INC $149F) -> `EA EA EA` (NOP)

### 5. Invencibilidade (Proteção contra Dano)
- **Descrição:** O Mario não entra no estado de "ferido" (Hurt) ao tocar em inimigos ou obstáculos, mantendo seu powerup atual.
- **Offset PC:** `0xC763`
- **Alteração:** `85 71` (STA $71) -> `EA EA` (NOP)
