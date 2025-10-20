import pygame
import random
from settings import path_assets, resource_path
from os.path import join

class Sequencia():
    def __init__(self, x: int, y: int, bpm: int, offset: float = 0.0):
        self.next = -1
        self.sortear()
        self.images = [
            pygame.image.load(resource_path(join(path_assets, 'seta_copas_instrucao.png'))),
            pygame.image.load(resource_path(join(path_assets, 'seta_paus_instrucao.png'))),
            pygame.image.load(resource_path(join(path_assets, 'seta_ouros_instrucao.png'))),
            pygame.image.load(resource_path(join(path_assets, 'seta_espadas_instrucao.png')))
        ]
        self.rect = self.images[0].get_rect()
        self.rect.center = (x, y)

        # Calculate velocity based on BPM (pixels per second)
        # Arrow should take 4 beats (one measure in 4/4 time) to reach perfect zone
        # Distance from start (-200) to perfect zone (~70) = 270 pixels
        # Time for 4 beats = 240/BPM seconds
        # Velocity (px/sec) = 270 / (240/BPM) = BPM * 1.125
        self.speed = bpm * 1.125

        # Convert bars to seconds: bars * 4 beats/bar * 60/BPM
        self.bpm = bpm
        self.offset = offset
        offset_seconds = (60.0 / float(self.bpm)) * 4.0 * self.offset

        self.offset_remaining = max(0.0, float(offset_seconds))
        self.started = False

    def sortear(self):
        ''' Sortea direções aleatórias'''
        atual = self.next
        while self.next == atual:
            self.next = random.randint(1,4)

    def update(self, dt: float):
        if not self.started:
            self.offset_remaining -= dt
            if self.offset_remaining <= 0:
                self.started = True
            else:
                return

        self.rect.y += int(self.speed * dt)

    def reset(self):
        self.rect.y = -200
        self.sortear()

    def render(self, surface: pygame.surface.Surface):
        surface.blit(self.images[self.next-1], (self.rect.x, self.rect.y))
