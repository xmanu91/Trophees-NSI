import pygame

class Scene():
    def __init__(self):
        self.spriteGroup: pygame.sprite.Group = pygame.sprite.Group()
    
    def draw(self, surface) -> None:
        self.spriteGroup.draw(surface)

    def update(self) -> None:
        self.spriteGroup.update()