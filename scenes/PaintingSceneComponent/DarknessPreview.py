import pygame
from utility.tools import fill_gradient

class DarknessPreview(pygame.sprite.Sprite):
    def __init__(self, rect: pygame.Rect):
        super().__init__()
        self.rect = rect
        self.image = pygame.Surface(self.rect.size)
        fill_gradient(self.image, (255,255,255), (0,0,0), vertical=False)

    def changeColor(self, color):
        self.image.fill((255,0,0))
        fill_gradient(self.image, color, (0,0,0), vertical=False)


        