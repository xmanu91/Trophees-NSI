import pygame
from ui.SceneManager import SceneManager

class ButtonManager:
    def __init__(self, sceneManager: SceneManager):
        self.sceneManager = sceneManager
        print('ButtonManager created')
        print(f"Scene manager: {self.sceneManager}")
        print(f"Current scene: {self.sceneManager.currentScene}")

    def getSpriteGroup(self) -> pygame.sprite.Group:
        return self.sceneManager.getSpriteGroup()

    def update(self):
        self.sceneManager.update()
        
    