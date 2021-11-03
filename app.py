import pygame
from pygame.locals import *
from sys import exit
import os
from random import randrange, choice

pygame.init ()
pygame.mixer.init()

som_pts = pygame.mixer.Sound('coração certo.wav') #efeito sonoro
som_pts.set_volume (1)

# Localizar os arquivos do jogo
diretorio_principal = os.path.dirname(__file__) #pasta a onde ta os arquivos
diretorio_imagem = os.path.join(diretorio_principal, 'Sprites') #pasta da animação  
diretorio_som = os.path.join(diretorio_principal, 'Som') #pasta do som

# Cenario do jogo
imagemFundo = pygame.image.load('boa.gif')

#SOM
F = pygame.mixer.Sound(os.path.join(diretorio_principal,'morte certa.wav'))
colidiu = False

# Cor e tamanho da tela
branco = (255,255,255)
tela = pygame.display.set_mode((800,420)) # LARGURA E ALTURA

# Titulo do jogo
pygame.display.set_caption('Dark Souls Fácil')

# Todas as artes
sprite_sheet = pygame.image.load(os.path.join(diretorio_imagem, 'Completo.png')).convert_alpha()

obs_random = choice([0, 1]) # randomizar os obstaculos 

velovidade_fps = 10

class Dark(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.Completo = []
        for i in range(3):
            img = sprite_sheet.subsurface((i * 64, 0), (64, 64)) # corta o cavaleiro
            img = pygame.transform.scale(img, (64*2, 64*2)) # escala do cavaleiro 
            self.Completo.append(img)  
   
        self.index_lista = 0
        self.image = self.Completo[self.index_lista]
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.center = (100,333) # posição do cavaleiro
        self.pulo = False
        self.posy_inicial= 397 - 64 - 128//2 #posição do cavaeliro

    def pular(self): #pulo
        self.pulo = True
        
    def update(self): # Parametros do pulo
        if self.pulo == True:
            if self.rect.y <= 80: #limite da altura
                self.pulo = False
            self.rect.y -= 25 #velocidade do pulo
        else: #retorna a posição apos o pulo
            if self.rect.y < self.posy_inicial:
                self.rect.y += 17 #velocidade para voltar para a posição inicial
            else:
                self.rect.y = self.posy_inicial
        if self.index_lista > 2: # animção do cavaleiro 
            self.index_lista = 0
        self.index_lista += 0.25
        self.image = self.Completo[int(self.index_lista)]
 
class Chao(pygame.sprite.Sprite):
    def __init__(self, pos_x):
        pygame.sprite.Sprite.__init__(self)
        self.image = sprite_sheet.subsurface((7 * 64, 0), (64, 64)) #corta o chão
        self.image = pygame.transform.scale(self.image, (64*2, 64*2))     
        self.rect = self.image.get_rect() #possicionar na tela 
        self.rect.y = 290 #altura   
        self.rect.x = pos_x * 128    #largura


    def update(self): # fazer o chão se repetir 
        if self.rect.topright[0] < 0:
            self.rect.x = 800
        self.rect.x -= 10

class espada(pygame.sprite.Sprite): #obstaculo
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_obstaculo = []
        for i in range (3, 5):
            img_2 = sprite_sheet.subsurface((i * 64, 0), (64, 64))
            img_2 = pygame.transform.scale(img_2, (64*2, 64*2))
            self.image_obstaculo.append(img_2)
        
        self.index_lista = 0
        self.image = self.image_obstaculo[self.index_lista]
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.center = (800, 345)
        self.rect.x = 800
        self.obs = obs_random
        
    
    def update(self):
        if self.obs == 1:
            if self.rect.topright[0] < 0:
                self.rect.x =  800
            self.rect.x -= velovidade_fps #velocidade
        
        if self.index_lista > 1: # animção da espada
            self.index_lista = 0
        self.index_lista += 0.25
        self.image = self.image_obstaculo[int(self.index_lista)]


class corvo(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.imagens_corvo = []
        for i in range (5, 7):
            img_3= sprite_sheet.subsurface((i * 64, 0),(64, 64))
            img_3= pygame.transform.scale(img_3, (45*2, 45*2))
            self.imagens_corvo.append(img_3)

        self.index_lista = 0
        self.image = self.imagens_corvo[self.index_lista]
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image) # ver colisão 
        self.rect.center = (800, 310)
        self.rect.x = 800
        self.obs = obs_random
        

    def update(self):
        if self.obs == 0:
            if self.rect.topright[0] < 0:
                self.rect.x =  800
            self.rect.x -= velovidade_fps
            
            if self.index_lista > 1: # animção do cavaleiro 
                self.index_lista = 0
            self.index_lista += 0.25
            self.image = self.imagens_corvo[int(self.index_lista)]



todas_sprites = pygame.sprite.Group() #criar um grupo
souls = Dark()
todas_sprites.add(souls)

for i in range(800*2//128): #loop do chão
    piso = Chao(i)
    todas_sprites.add(piso)

fogueira = espada()
todas_sprites.add(fogueira) #criar grupo

passaro = corvo()
todas_sprites.add(passaro)

desafio = pygame.sprite.Group()
desafio.add(fogueira) #criar grupo
desafio.add(passaro)

pontos = 0
fonte = pygame.font.SysFont('time new roman', 40, True, False)

pygame.font.init()
font_padrao = pygame.font.get_default_font()
fonte_perdeu = pygame.font.SysFont(font_padrao, 45)

def exibe_mensagem(msg, tamanho, cor): #mensagem na tela 
    fonte = pygame.font.SysFont('time new roman', tamanho, True, False)
    mensagem = f'{msg}' 
    texto_formatado = fonte.render(mensagem, True, cor)
    return texto_formatado

def reiniciar(): # o que acontece quando aperta r
    global pontos, velovidade_fps, colidiu, obs_random 
    pontos = 0
    velovidade_fps = 10
    colidiu = False
    passaro.rect.x = 800
    fogueira.rect.x = 800
    obs_random = choice([0,1])


relogio = pygame.time.Clock()
while True: # loop para o jogo fica funcionando 
    relogio.tick(30) #FPS
    tela.fill(branco) #fundo da tela
    mensagem = f'Pontos: {pontos}' #pontos 
    texto_formatado = fonte.render(mensagem, True, (0,0,0))
    for event in pygame.event.get():
       if event.type == QUIT: #sair do jogo
           pygame.quit()
           exit()
       if event.type == KEYDOWN:   # tecla para a ação
            if event.key == K_SPACE: 
                if souls.rect.y != souls.posy_inicial:
                    pass
                else:
                    souls.pular()
            if event.key == K_r and colidiu == True:
                reiniciar()
    colisoes = pygame.sprite.spritecollide(souls, desafio, False, pygame.sprite.collide_mask)

    
    tela.blit(imagemFundo, (0, 0)) #fundo da imagem 

    if fogueira.rect.topright[0] <= 0 or passaro.rect.topright [0] <= 0: # quando reiniciar o jogo, possição dos objetos 
        obs_random = choice([0, 1])
        fogueira.rect.x = 800
        passaro.rect.x = 800
        fogueira.obs = obs_random
        passaro.obs = obs_random

    if colisoes and colidiu == False: #colisão do cavaleiro 
        F.play()
        colidiu = True

    if colidiu == True: #caso colidir 
        game_over = exibe_mensagem('GAME OVER', 70, (139,0,0))
        tela.blit(game_over, (225, 200)) 
        reset = exibe_mensagem('Pressione R para reiniciar', 30, (0,0,0))
        tela.blit(reset, (230, 260))

    else:
        pontos = pontos + 1 #aumenta os pontos 
        todas_sprites.update()
    
    if pontos % 100 == 0:
        som_pts.play()
        if velovidade_fps == 33:
            velovidade_fps += 0
        else:
            velovidade_fps += 3

    
  
    tela.blit(texto_formatado,(600,40)) #local do texto 
    todas_sprites.draw(tela) #desenhar
    pygame.display.flip()
