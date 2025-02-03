from ui.Scene import Scene
import pygame

class SceneManager:
    def __init__(self, surface):
        self.surface: pygame.Surface = surface
        self.currentScene: Scene = None

    def setAsCurrentScene(self, scene: type[Scene]) -> None:
        if self.currentScene != None:
            self.currentScene.spriteGroup.empty()
            self.surface.fill((0,0,0))
        self.currentScene = scene
        self.draw()

    def draw(self):
        self.currentScene.spriteGroup.draw(self.surface)

    def update(self):
        self.currentScene.spriteGroup.update()
        self.currentScene.update()
