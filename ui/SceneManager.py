from Scene import Scene

class SceneManager:
    def __init__(self, surface):
        self.surface = surface
        self.currentScene = None

    def setAsCurrentScene(self, scene: type[Scene]) -> None:
        if self.currentScene != None:
            self.currentScene.empty()
        scene.draw(self.surface)