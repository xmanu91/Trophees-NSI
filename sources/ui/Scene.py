import pygame

class Scene():
    def __init__(self):
        self.spriteGroup: pygame.sprite.Group = pygame.sprite.Group()
    
    def draw(self, surface):
        self.spriteGroup.draw(surface)

    def update(self):
        self.spriteGroup.update()