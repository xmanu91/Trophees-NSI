import pygame
from utility.tools import getPath

class Image(pygame.sprite.Sprite):
    def __init__(self, image: str, imageCoordinates: pygame.Rect):
        super().__init__()
        self.image = pygame.image.load(getPath(image))
        self.image = pygame.transform.scale(self.image, imageCoordinates.size).convert_alpha()
        self.rect = imageCoordinates