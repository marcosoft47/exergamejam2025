import os
import random
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
        self.points = 0
        self.score = 0
        self.feedback = None
        self.superficie = pygame.display.set_mode(
            size = self.tamanho,
            display = 0
        )

        pygame.display.set_caption('exergamejam')
        self.origin = (0, 0, 0)
        self.fonte = pygame.font.SysFont('aakar', 35) # essa fonte NÃO funciona no windows

        self.imagemEsteira = pygame.image.load(os.path.join(path_assets, 'esteira-resize.png'))
        self.imagemMoldura = pygame.image.load(os.path.join(path_assets, 'fundo.png'))
        self.imagemKairos = pygame.image.load(os.path.join(path_assets, 'kairos_central.png'))

        self.menuBackgroundAsset = pygame.image.load(os.path.join(path_assets, 'background_temple.png'))
        self.startButtonAsset = pygame.image.load(os.path.join(path_assets, 'start.png'))
        self.rankingButtonAsset = pygame.image.load(os.path.join(path_assets, 'ranking.png'))

        self.somCerto = pygame.mixer.Sound(os.path.join(path_assets, 'snd_dumbvictory.wav'))
        self.somErrado = pygame.mixer.Sound(os.path.join(path_assets, 'snd_hurt1.wav'))

        songs = ['sangueferve.mp3', 'timmaia.mp3']
        self.song = random.choice(songs)

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
        self.corApertandoNO = (0,0,0)
        self.corApertandoSO = (0,0,0)
        self.corApertandoSL = (0,0,0)
        self.corApertandoNL = (0,0,0)

        self.next = sequencia.Sequencia(tamanho_tela[0]//2, -200, 2)

    def menu(self):
        in_menu = True
        relogio = pygame.time.Clock()

        button_width = 256
        button_height = 96
        button_spacing = 20

        start_button_x = (self.tamanho[0] - button_width) // 2
        start_button_y = (self.tamanho[1] - button_height) // 2 - (button_height // 2) - (button_spacing // 2)
        start_button_rect = pygame.Rect(start_button_x, start_button_y, button_width, button_height)

        ranking_button_x = (self.tamanho[0] - button_width) // 2
        ranking_button_y = start_button_y + button_height + button_spacing

        # Disabled for now
        ranking_button_disabled = self.rankingButtonAsset.copy()
        ranking_button_disabled.set_alpha(100)

        while in_menu and self.running:
            relogio.tick(60)

            for e in pygame.event.get():
                if e.type == pygame.MOUSEBUTTONDOWN:
                    if start_button_rect.collidepoint(e.pos):
                        in_menu = False

            self.superficie.fill(self.origin)
            self.superficie.blit(self.menuBackgroundAsset, (0, 0))

            self.superficie.blit(self.startButtonAsset, (start_button_x, start_button_y))
            self.superficie.blit(ranking_button_disabled, (ranking_button_x, ranking_button_y))

            pygame.display.update()

    def run(self):
        # Mainloop
        input = 0
        self.points = 0
        self.feedback = None

        relogio = pygame.time.Clock()

        pygame.mixer.music.load(os.path.join(path_assets, self.song))
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
            if self.flechaNO.update() != 0:
                input = self.flechaNO.number # 1
            elif self.flechaNL.update() != 0:
                input = self.flechaNL.number # 2
            elif self.flechaSO.update() != 0:
                input = self.flechaSO.number # 3
            elif self.flechaSL.update() != 0:
                input = self.flechaSL.number # 4


            self.next.update()
            # Verifica se foi apertado o botão certo
            if self.next.next == input:
                if self.next.rect.y < 10:
                    self.feedback = "Miss"
                    self.points = 0
                elif 10 <= self.next.rect.y < 40:
                    self.feedback = "Too Fast"
                    self.points = 1
                elif 40 <= self.next.rect.y <= 60 or self.next.rect.y > 80:
                    self.feedback = "Almost!"
                    self.points = 5
                elif 60 < self.next.rect.y <= 80:
                    self.feedback = "Perfect!"
                    self.points = 10
                    self.somCerto.play()

                self.score += self.points
                self.next.reset()
            elif input != 0:
                self.feedback = "Miss"
                self.points = 0
                self.somErrado.play()
                pass

            input = 0

            # ----- Render -----
            self.superficie.fill(self.origin)
            self.superficie.blit(self.imagemMoldura, (0,0))
            self.superficie.blit(self.fonte.render(f'Score: {self.score}', True, (255,255,255)), (25,25))
            if self.feedback: self.superficie.blit(self.fonte.render(f'{self.feedback}', True, (255,255,255)), (25, 60))
            self.superficie.blit(self.imagemEsteira, (tamanho_tela[0]//2-75,-50))

            self.flechaNO.render(self.superficie)
            self.flechaNL.render(self.superficie)
            self.flechaSO.render(self.superficie)
            self.flechaSL.render(self.superficie)

            self.next.render(self.superficie)

            pygame.display.update()



if __name__ == "__main__":
    g = Jogo()
    g.menu()
    if g.running:
        g.run()

    pygame.quit()
    exit()
