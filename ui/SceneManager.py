from ui.Scene import Scene
import pygame
from utility import consolLog

class SceneManager:
    def __init__(self, surface):
        self.surface: pygame.Surface = surface
        self.currentScene: Scene = None

    def setAsCurrentScene(self, scene: type[Scene], deletePreviousScene: bool = True) -> None:
        if self.currentScene != None and deletePreviousScene:
            consolLog.info('Changement de scene:', scene)
            self.currentScene.spriteGroup.empty()
            self.surface.fill((0,0,0))
        elif self.currentScene != None and deletePreviousScene == False:
            consolLog.info('Changement de scene sans effacer la scene precedente', scene)
        self.currentScene = scene
        self.draw()

    def draw(self):
        self.currentScene.spriteGroup.draw(self.surface)

    def getSpriteGroup(self) -> pygame.sprite.Group:
        return self.currentScene.spriteGroup
    
    def update(self):
        self.currentScene.spriteGroup.update()
        self.currentScene.update()