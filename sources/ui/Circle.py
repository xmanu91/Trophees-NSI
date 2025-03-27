import pygame
import pygame.gfxdraw

class Circle(pygame.sprite.Sprite):
    def __init__(self, rect: pygame.Rect, color: pygame.Color):
        super().__init__()
        self.rect = rect
        self.image = pygame.Surface(self.rect.size, pygame.SRCALPHA).convert_alpha()
        pygame.gfxdraw.filled_circle(self.image, int(self.rect.w/2), int(self.rect.h/2), 18, color)

    def changeColor(self, color: pygame.Color):
        self.image = pygame.Surface(self.rect.size, pygame.SRCALPHA).convert_alpha()
        pygame.gfxdraw.filled_circle(self.image, int(self.rect.w/2), int(self.rect.h/2), 18, color)
