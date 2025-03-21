from ui.Scene import Scene
import pygame
from utility import consolLog

class SceneManager:
    def __init__(self, surface):
        self.surface: pygame.Surface = surface
        self.currentScene: Scene | None = None

    def setAsCurrentScene(self, scene: Scene, deletePreviousScene: bool = True) -> None:
        if self.currentScene != None and deletePreviousScene:
            consolLog.info('Changement de scene:', scene)
            self.currentScene.spriteGroup.empty()
            self.surface.fill((0,0,0))
        elif self.currentScene != None and deletePreviousScene == False:
            consolLog.info('Changement de scene sans effacer la scene precedente', scene)
        self.currentScene = scene
        self.draw()

    def draw(self) -> None:
        if self.currentScene:
            self.currentScene.spriteGroup.draw(self.surface)
    
    def update(self) -> None:
        if self.currentScene:
            self.currentScene.spriteGroup.update()
            self.currentScene.update()