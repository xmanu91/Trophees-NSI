import pygame
import utility.tools as tools

class Shape(pygame.sprite.Sprite):
    def __init__(self, rect: pygame.Rect, color: pygame.Color):
        super().__init__()
        self.rect = rect
        self.color = color
        self.image = pygame.Surface((self.rect.width, self.rect.height))
        self.image = self.image.convert_alpha()
        self.image.fill(self.color)

    def changeColor(self, color: pygame.Color):
        self.color = tools.removeAlpha(color)
        self.image.fill(self.color)

    def changeRect(self, rect: pygame.Rect):
        self.rect = rect
        self.image = pygame.Surface((self.rect.width, self.rect.height))
        self.image.fill(self.color)

