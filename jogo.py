import os
import pygame
from pygame.locals import QUIT, KEYDOWN, K_ESCAPE

import flecha
import sequencia
from settings import path_assets, tamanho_tela

class Jogo():
    def __init__(self):
        pygame.init()
        self.running = True
        self.tamanho = tamanho_tela
        self.pontuacao = 0
        self.sweetspot = 0
        self.superficie = pygame.display.set_mode(
            size = self.tamanho,
            display = 0
        )
        pygame.display.set_caption('exergamejam')
        self.fundo = (0,0,0)
        self.fonte = pygame.font.SysFont('aakar', 35) # essa fonte NÃO funciona no windows

        self.imagemEsteira = pygame.image.load(os.path.join(path_assets, 'esteira-resize.png'))
        self.imagemMoldura = pygame.image.load(os.path.join(path_assets, 'fundo.png'))
        self.imagemKairos = pygame.image.load(os.path.join(path_assets, 'kairos_central.png'))

        self.somCerto = pygame.mixer.Sound(os.path.join(path_assets, 'snd_dumbvictory.wav'))
        self.somErrado = pygame.mixer.Sound(os.path.join(path_assets, 'snd_hurt1.wav'))
        self.nomeMusica = 'sangueferve.mp3'
        # self.nomeMusica = 'timmaia.mp3'

        #  N
        # O L
        #  S
        
        __N = 220
        __S = 450
        __L = 490
        __O = 180
        self.flechaNO = flecha.Flecha(
            x = __O, 
            y = __N, 
            image = pygame.image.load(os.path.join(path_assets, 'seta_copas.png')),
            number = 1
        )
        self.flechaSO = flecha.Flecha(
            x = __O,
            y = __S, 
            image = pygame.image.load(os.path.join(path_assets, 'seta_paus.png')),
            number = 2
        )
        self.flechaSL = flecha.Flecha(
            x = __L,
            y = __S, 
            image = pygame.image.load(os.path.join(path_assets, 'seta_ouros.png')), 
            number = 3
        )
        self.flechaNL = flecha.Flecha(
            x = __L,
            y = __N, 
            image = pygame.image.load(os.path.join(path_assets, 'seta_espadas.png')), 
            number = 4
        )
        
        self.next = sequencia.Sequencia(tamanho_tela[0]//2, -200, 2)

        # self.somCorreto = pygame.mixer.Sound(os.path.join(path_assets, ''))
    
    def run(self):
        # Mainloop
        input = 0
        relogio = pygame.time.Clock()
        
        pygame.mixer.music.load(os.path.join(path_assets, self.nomeMusica))
        pygame.mixer.music.play()
        while self.running:
            relogio.tick(60)
            # ----- Eventos -----
            for e in pygame.event.get():
                if e.type == QUIT:
                    self.running = False
                if e.type == KEYDOWN:
                    if e.key == K_ESCAPE:
                        self.running = False
            
            # ----- Update -----
            if self.flechaNO.update(self.superficie) != 0:
                input = self.flechaNO.number # 1
            elif self.flechaNL.update(self.superficie) != 0:
                input = self.flechaNL.number # 2
            elif self.flechaSO.update(self.superficie) != 0:
                input = self.flechaSO.number # 3
            elif self.flechaSL.update(self.superficie) != 0:
                input = self.flechaSL.number # 4

            self.next.update()

            # Verifica se foi apertado o botão certo
            if self.next.next == input:
                # Deu boa :D
                if 10 <= self.next.rect.y < 40:
                    self.pontuacao += 1
                elif 40 <= self.next.rect.y <= 60 or self.next.rect.y > 80:
                    self.pontuacao += 5
                elif 60 < self.next.rect.y <= 80:
                    self.pontuacao += 10
                    self.somCerto.play()
                print(self.next.rect.y)
                self.next.reset()
            elif input != 0:
                # Deu ruim D:
                self.somErrado.play()
                pass
            input = 0


            # ----- Render -----
            self.superficie.fill((self.fundo))
            self.superficie.blit(self.imagemMoldura, (0,0))
            self.superficie.blit(self.fonte.render(f'Pontuação: {self.pontuacao}', True,(255,255,255)), (25,25))
            self.superficie.blit(self.imagemEsteira, (tamanho_tela[0]//2-75,-50))
            # self.superficie.blit(self.imagemKairos, (tamanho_tela[0]//2-135,400))

            self.flechaNO.render(self.superficie)
            self.flechaNL.render(self.superficie)
            self.flechaSO.render(self.superficie)
            self.flechaSL.render(self.superficie)

            self.next.render(self.superficie)

            pygame.display.update()



if __name__ == "__main__":
    g = Jogo()
    g.run()

    pygame.quit()
    exit()