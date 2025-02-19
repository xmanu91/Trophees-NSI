from ui.Scene import Scene
from utility.RoomManager import RoomManager
import pygame

class SceneManager:
    def __init__(self, surface):
        self.surface: pygame.Surface = surface
        self.currentScene: Scene = None

    def setAsCurrentScene(self, scene: type[Scene], deletePreviousScene: bool = True) -> None:
        if self.currentScene != None and deletePreviousScene:
            print('Changement de scene:', scene)
            self.currentScene.spriteGroup.empty()
            self.surface.fill((0,0,0))
        elif self.currentScene != None and deletePreviousScene == False:
            print('Changement de scene sans effacer la scene precedente', scene)
        self.currentScene = scene
        self.draw()

    def draw(self):
        self.currentScene.spriteGroup.draw(self.surface)

    def update(self):
        self.currentScene.spriteGroup.update()
        self.currentScene.update()

    def setHomeScene(self, scene: type[Scene], roomManager: RoomManager):
        self.homeScene = scene
        self.roomManager = roomManager

    def goToHomeScene(self):
        self.setAsCurrentScene(self.homeScene)
        self.currentScene.__init__(self, self.roomManager)
