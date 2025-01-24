import pygame

class Shape(pygame.sprite.Sprite):
    def __init__(self, rect: pygame.Rect, color: pygame.Color):
        super().__init__()
        self.rect = rect
        self.color = color
        self.image = pygame.Surface((self.rect.width, self.rect.height))
        self.image.fill(self.color)

    def changeColor(self, color: pygame.Color):
        self.color = color
        self.image.fill(self.color)

    def changeRect(self, rect: pygame.Rect):
        """ Allow to change the position and the size of the shape """
        self.rect = rect
        self.image = pygame.Surface((self.rect.width, self.rect.height))
        self.image.fill(self.color)

    def get_rect(self):
        return self.rect

    def get_image(self):
        return self.image

