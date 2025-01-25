from ui.SceneManager import SceneManager
from ui.Scene import Scene
from ui.Image import Image
from ui.Canva import Canva
from ui.Text import Text
import pygame

from scenes.PaintingSceneComponent.ToolBar import ToolBar
from scenes.PaintingSceneComponent.Timer import Timer

class PaintingScene(Scene):
    def __init__(self, sceneManager: SceneManager):
        super().__init__()
        screenWidth, screenHeight = sceneManager.surface.get_width(), sceneManager.surface.get_height()
        self.background = Image("assets/background_theme.png", pygame.Rect(0,0, screenWidth, screenHeight))
        self.theme = "Le système solaire"

        self.textTheme = Text(self.theme, 32, (450, 250-16), (255,255,255), True)

        timerDuration = 1
        self.textTimer = Text(str(timerDuration), 32, (450, 250+16), (255,255,255), True)
        self.timer = Timer(timerDuration, self.textTimer, self.setCanva)

        self.spriteGroup.add(self.background, self.textTimer, self.textTheme)

        self.timer.startTimer()
        
    def setCanva(self):
        self.spriteGroup.empty()
        self.canva = Canva(200, 0, 700, 500, (255, 255, 255), (0, 0, 0))
        self.toolBar = ToolBar(self.canva, self.spriteGroup, self.theme)
        self.spriteGroup.add(self.canva)

    def update(self):
        self.toolBar.update()
        self.timer.update()