import pygame
import os

class Image(pygame.sprite.Sprite):
    def __init__(self, image: str, imageCoordinates: pygame.Rect):
        super().__init__()
        self.image = pygame.image.load(os.path.join(image))
        self.image = pygame.transform.scale(self.image, imageCoordinates.size).convert_alpha()
        self.rect = imageCoordinates

    def get_image(self):
        return self.image

    def get_rect(self):
        return self.rect