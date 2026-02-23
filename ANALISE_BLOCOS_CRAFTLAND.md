# Análise dos Blocos de Script - Free Fire Craftland

Esta documentação fornece uma análise detalhada do funcionamento dos scripts de bloco no Free Fire Craftland, baseada na documentação oficial e pesquisa técnica.

## 1. Conceito Geral
O **Script de Bloco** é um método de programação visual (estilo *block-based programming*) que permite aos criadores desenvolver lógicas de jogo personalizadas sem a necessidade de escrever código textual complexo. É a ferramenta principal para criar modos de jogo únicos, como o efeito de "cabeça grande", sistemas de economia, regras de combate customizadas, entre outros.

## 2. Interface do Editor
O editor de scripts de bloco é dividido em quatro áreas principais:

*   **Painel de Categorias (Esquerda):** Onde os blocos estão organizados por função (Eventos, Ações, Lógica, Variáveis, Funções).
*   **Tela/Canvas (Centro):** A área principal de trabalho onde os blocos são arrastados, soltos e conectados.
*   **Painel de Arquivos:** Mostra o arquivo que está sendo editado no momento (geralmente scripts `.fcg`).
*   **Painel de Operações/Propriedades (Baixo/Direita):** Aparece ao selecionar um bloco, permitindo deletar, copiar ou configurar parâmetros específicos.

## 3. Categorias e Tipos de Blocos
Os blocos possuem cores e formatos específicos que indicam sua função e como podem ser conectados:

### A. Eventos (Vermelho - Formato "Hat")
Os blocos de evento são os gatilhos (triggers) que iniciam a execução da lógica. Eles possuem o topo arredondado, indicando que são o ponto inicial e nada pode ser conectado acima deles.
*   **Exemplos:** "Ao iniciar a rodada", "Quando um jogador entra no jogo", "Quando um jogador sofre dano".

### B. Ações (Verde/Azul - Formato "Stack")
As ações são as instruções que executam comandos no jogo. Elas possuem encaixes superiores e inferiores para permitir o sequenciamento.
*   **Exemplos:** "Teleportar jogador", "Dar item", "Alterar velocidade de movimento", "Exibir mensagem HUD".

### C. Lógica e Fluxo (Amarelo/Laranja - Formato "C-Block")
Estes blocos controlam o fluxo de execução através de condições e loops. O formato em "C" permite "abraçar" outros blocos que serão executados se a condição for atendida.
*   **Se (If):** Executa os blocos internos se uma condição for verdadeira.
*   **Enquanto (While):** Repete os blocos internos enquanto a condição for verdadeira.
*   **Para cada (ForEach):** Itera sobre uma lista de elementos (ex: todos os jogadores).

### D. Variáveis e Dados
Utilizados para armazenar e manipular informações. Os tipos de dados disponíveis na categoria de variáveis são:
*   **Bool:** Valores booleanos (Verdadeiro/Falso).
*   **Inteiro:** Números inteiros (usados para contadores, IDs).
*   **Flutuante:** Números decimais.
*   **Cadeia:** Textos/Strings.
*   **Modelo de lista <qualquer tipo>:** Listas dinâmicas de elementos.
*   **Qualquer tipo:** Tipo genérico, frequentemente usado para referenciar Entidades/Jogadores.
*   **Vetor 3 / Vetor 2:** Coordenadas espaciais (X, Y, Z).

Existem três escopos principais:
1.  **Atributos Globais de Entidade:** Acessíveis por qualquer script através de "Obter Entidade Global" ou "Definir Entidade Global".
2.  **Variáveis de Script:** Locais ao script atual, mas podem ser referenciadas externamente.
3.  **Variáveis Locais:** Válidas apenas dentro de um bloco de código específico (ex: dentro de um loop).

## 4. Conectividade e Fluxo de Execução
*   **Ordem de Execução:** Por padrão, a execução ocorre de cima para baixo seguindo as conexões.
*   **Encaixe de Parâmetros:** Campos de entrada nos blocos (parâmetros) aceitam blocos de valor (expressões) que têm formatos arredondados ou hexagonais (booleanos).
*   **Separação de Contexto:** Scripts de Servidor e Scripts de Cliente operam em ambientes diferentes. O Servidor lida com a lógica de jogo e estado, enquanto o Cliente lida com UI e efeitos locais. Eles se comunicam via **Eventos**.

## 5. Arquivos Técnicos
*   `.fcg`: Extensão dos arquivos de script de bloco.
*   `.fcc`: Extensão das bibliotecas (Standard Libraries) que contêm as definições dos blocos disponíveis.

---
*Análise produzida com base no guia oficial do Free Fire Craftland (2025).*
