import pygame
#button class
class Flecha():
	def __init__(self, x: int, y: int, image: pygame.surface.Surface, number: int, scale=0.5):
		width = image.get_width()
		height = image.get_height()
		self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
		self.number = number
		self.rect = self.image.get_rect()
		self.rect.topleft = (x, y)
		self.clicked = False
		self.corDestaque = (0,0,0)

	def update(self) -> int:
		pos = pygame.mouse.get_pos()

		# Verifica se o mouse está em cima da flecha
		if self.rect.collidepoint(pos):
			self.corDestaque = (239, 215, 111)
			if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
				self.clicked = True
				return self.number
		else:
			self.corDestaque = (0,0,0)

		if pygame.mouse.get_pressed()[0] == 0:
			self.clicked = False
		return 0
	
	def render(self, surface: pygame.surface.Surface):
		pygame.draw.rect(surface, self.corDestaque, (self.rect.x, self.rect.y,128,128))
		surface.blit(self.image, (self.rect.x, self.rect.y))
