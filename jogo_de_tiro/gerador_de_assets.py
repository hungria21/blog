import pygame
import random
import os

# -- Configurações --
LARGURA_TELA = 800
ALTURA_TELA = 600
PASTA_ASSETS = 'assets'

# -- Cores --
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
AZUL = (50, 50, 255)
VERMELHO = (255, 50, 50)
AMARELO = (255, 255, 0)

def gerar_assets():
    """
    Gera todas as imagens necessárias para o jogo e as salva na pasta de assets.
    """
    pygame.init()

    # Garante que a pasta de assets exista
    if not os.path.exists(PASTA_ASSETS):
        os.makedirs(PASTA_ASSETS)

    # -- 1. Gerar Imagem do Jogador --
    imagem_jogador = pygame.Surface([50, 40], pygame.SRCALPHA)
    pygame.draw.polygon(imagem_jogador, AZUL, [(25, 0), (0, 40), (50, 40)])
    pygame.image.save(imagem_jogador, os.path.join(PASTA_ASSETS, 'jogador.png'))

    # -- 2. Gerar Imagem do Inimigo --
    imagem_inimigo = pygame.Surface([40, 30], pygame.SRCALPHA)
    pygame.draw.polygon(imagem_inimigo, VERMELHO, [(20, 30), (0, 0), (40, 0)])
    pygame.image.save(imagem_inimigo, os.path.join(PASTA_ASSETS, 'inimigo.png'))

    # -- 3. Gerar Imagem da Bala --
    imagem_bala = pygame.Surface([5, 15], pygame.SRCALPHA)
    imagem_bala.fill(AMARELO)
    pygame.image.save(imagem_bala, os.path.join(PASTA_ASSETS, 'bala.png'))

    # -- 4. Gerar Imagem de Fundo --
    imagem_fundo = pygame.Surface([LARGURA_TELA, ALTURA_TELA])
    imagem_fundo.fill(PRETO)
    for _ in range(200):
        x = random.randrange(LARGURA_TELA)
        y = random.randrange(ALTURA_TELA)
        raio = random.randrange(1, 3)
        pygame.draw.circle(imagem_fundo, BRANCO, (x, y), raio)
    pygame.image.save(imagem_fundo, os.path.join(PASTA_ASSETS, 'fundo.png'))

    pygame.quit()
    print("Assets gerados com sucesso!")

if __name__ == '__main__':
    gerar_assets()
