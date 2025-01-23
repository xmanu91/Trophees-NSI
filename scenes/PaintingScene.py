from ui.Scene import Scene
from ui.Text import Text
from ui.Button import Button 
from ui.SceneManager import SceneManager
from ui.Image import Image
from ui.TextInput import TextInput
from ui.ProgressBar import ProgressBar
from ui.Canva import Canva
import pygame
import threading
import time

class PaintingScene(Scene):
    def __init__(self, sceneManager: SceneManager):
        super().__init__()
        screenWidth, screenHeight = sceneManager.surface.get_width(), sceneManager.surface.get_height()
        self.background = Image("assets/background_theme.png", pygame.Rect(0,0, screenWidth, screenHeight))
        self.startTimer()
        self.timerDuration = 5
        self.textTheme = Text("Les planètes imaginaires", 32, (450, 250-16), (255,255,255), True)
        self.textTimer = Text(str(self.timerDuration), 32, (450, 250+16), (255,255,255), True)

        self.spriteGroup.add(self.background, self.textTimer, self.textTheme)

    def setCanva(self):
        canva = Canva(100, 0, 900-50, 500, (255, 255, 255), (0, 0, 0))
        self.spriteGroup.add(canva)

    def startTimer(self):
        threading.Thread(target=self.timer, daemon=True).start()

    def timer(self):
        print("Start timer")
        timer = 0
        while timer < self.timerDuration:
            time.sleep(1)
            timer += 1
            self.textTimer.setText(str(self.timerDuration - timer))
        print("End timer")
        self.setCanva()