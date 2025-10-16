import pygame
import random
from settings import path_assets
from os.path import join

class Sequencia():
    def __init__(self, x: int, y: int, speed: int):
        self.sortear()
        self.images = [
            pygame.image.load(join(path_assets, 'seta_copas_instrucao.png')),
            pygame.image.load(join(path_assets, 'seta_paus_instrucao.png')),
            pygame.image.load(join(path_assets, 'seta_ouros_instrucao.png')),
            pygame.image.load(join(path_assets, 'seta_espadas_instrucao.png'))
        ]
        self.rect = self.images[0].get_rect()
        self.rect.center = (x, y)
        self.velocidade = speed

    def sortear(self):
        ''' Sortea direções aleatórias'''
        self.next = random.randint(1,4)
    
    def update(self):
        self.rect.y += self.velocidade
        if self.rect.y >= 100:
            self.reset()
    
    def reset(self):
        self.rect.y = -200
        self.sortear()

    def render(self, surface: pygame.surface.Surface):
        surface.blit(self.images[self.next-1], (self.rect.x, self.rect.y))