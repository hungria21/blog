import pygame
import random
import os

# Inicializa o Pygame
pygame.init()

# -- Configurações da Tela --
largura_tela = 800
altura_tela = 600
tela = pygame.display.set_mode((largura_tela, altura_tela))
pygame.display.set_caption("Jogo de Tiro Espacial")

# -- Cores --
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)

# -- Carregar Assets --
# Constrói o caminho para a pasta de assets
pasta_assets = os.path.join(os.path.dirname(__file__), 'assets')
fundo_img = pygame.image.load(os.path.join(pasta_assets, 'fundo.png')).convert()
jogador_img = pygame.image.load(os.path.join(pasta_assets, 'jogador.png')).convert_alpha()
inimigo_img = pygame.image.load(os.path.join(pasta_assets, 'inimigo.png')).convert_alpha()
bala_img = pygame.image.load(os.path.join(pasta_assets, 'bala.png')).convert_alpha()

# -- Jogador --
class Jogador(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(jogador_img, (50, 40))
        self.rect = self.image.get_rect()
        self.rect.centerx = largura_tela // 2
        self.rect.bottom = altura_tela - 10
        self.velocidade_x = 0

    def update(self):
        self.velocidade_x = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.velocidade_x = -8
        if keystate[pygame.K_RIGHT]:
            self.velocidade_x = 8
        self.rect.x += self.velocidade_x
        if self.rect.right > largura_tela:
            self.rect.right = largura_tela
        if self.rect.left < 0:
            self.rect.left = 0

    def atirar(self):
        bala = Bala(self.rect.centerx, self.rect.top)
        todos_sprites.add(bala)
        balas.add(bala)

# -- Inimigo --
class Inimigo(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(inimigo_img, (40, 30))
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(largura_tela - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.velocidade_y = random.randrange(1, 4)

    def update(self):
        self.rect.y += self.velocidade_y
        if self.rect.top > altura_tela + 10:
            self.rect.x = random.randrange(largura_tela - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.velocidade_y = random.randrange(1, 4)

# -- Bala --
class Bala(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.transform.scale(bala_img, (5, 15))
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.velocidade_y = -10

    def update(self):
        self.rect.y += self.velocidade_y
        if self.rect.bottom < 0:
            self.kill()

# -- Grupos de Sprites --
todos_sprites = pygame.sprite.Group()
inimigos = pygame.sprite.Group()
balas = pygame.sprite.Group()

jogador = Jogador()
todos_sprites.add(jogador)

for i in range(8):
    inimigo = Inimigo()
    todos_sprites.add(inimigo)
    inimigos.add(inimigo)

# -- Loop do Jogo --
rodando = True
clock = pygame.time.Clock()

while rodando:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            rodando = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                jogador.atirar()

    # Atualiza
    todos_sprites.update()

    # Verifica colisões de balas com inimigos
    colisoes = pygame.sprite.groupcollide(inimigos, balas, True, True)
    for colisao in colisoes:
        inimigo = Inimigo()
        todos_sprites.add(inimigo)
        inimigos.add(inimigo)

    # Verifica colisões do jogador com inimigos
    colisoes = pygame.sprite.spritecollide(jogador, inimigos, False)
    if colisoes:
        rodando = False

    # Desenha
    tela.blit(fundo_img, (0, 0))
    todos_sprites.draw(tela)

    # Atualiza a tela
    pygame.display.flip()

pygame.quit()
