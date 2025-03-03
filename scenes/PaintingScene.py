import pygame

from ui.SceneManager import SceneManager
from ui.ProgressBar import ProgressBar
from ui.Scene import Scene
from ui.Image import Image
from ui.Canva import Canva
from ui.Timer import Timer
from ui.Text import Text

from scenes.PaintingSceneComponent.ToolBar import ToolBar
from scenes.VoteScene import VoteScene


from utility.GameManager import GameManager
from utility.RoomManager import RoomManager
from utility import consolLog

import time
import os


class PaintingScene(Scene):
    def __init__(self, sceneManager: SceneManager, roomManager: RoomManager, gameManager: GameManager):
        super().__init__()
        consolLog.info('Initialisation de Painting Scene')
        screenWidth, screenHeight = sceneManager.surface.get_width(), sceneManager.surface.get_height()
        self.background = Image("assets/backgrounds/background_theme.png", pygame.Rect(0,0, screenWidth, screenHeight))
        self.roomManager = roomManager
        self.sceneManager = sceneManager
        self.gameManager = gameManager
        
        if self.roomManager.username == roomManager.getRoomCreator():
            self.gameManager.drawTheme()
            self.gameManager.deleteDrawings()
            self.theme = self.gameManager.drawingTheme
        else:
            self.theme = self.gameManager.getTheme()

        self.textTheme = Text(self.theme, 32, (450, 250-16), (255,255,255), True)

        themeTimerDuration = 5
        gameTimerDuration = self.roomManager.getRoundTime()
        self.textThemeTimer = Text(str(themeTimerDuration), 32, (450, 250+16), (255,255,255), True)
        self.gameProgressBar = ProgressBar(pygame.Rect(200, 0, screenWidth-200, 10), (0, 255, 0), gameTimerDuration, self.endDrawing)
        self.themeTimer = Timer(themeTimerDuration, self.textThemeTimer, self.setCanva)
        self.canva = Canva(pygame.Rect(200, 0, 700, 500), (255, 255, 255), (0, 0, 0), roomManager.username)
        self.toolBar = None
        self.spriteGroup.add(self.background, self.textThemeTimer, self.textTheme)

        self.themeTimer.startTimer()
        self.gameManager.resetTempDir()
        self.tempdir = self.gameManager.getTempDir()

        self.roomManager.currentRound += 1
        consolLog.info("Rounds number : ", self.roomManager.currentRound)
        consolLog.info("Total of rounds : ", self.roomManager.getRoundsNumber())

    def setCanva(self):
        self.spriteGroup.empty()
        self.toolBar = ToolBar(self.canva, self.spriteGroup, self.theme)
        self.spriteGroup.add(self.canva, self.gameProgressBar)
        self.gameProgressBar.run_start()

    def endDrawing(self):
        consolLog.info("Fin de la scene de dessin")

        self.spriteGroup.empty()
        self.canva.save(self.tempdir.name)
        self.gameManager.sendDrawing(os.path.join(self.tempdir.name, self.roomManager.username.strip() + "_drawing.png"))

        self.roomManager.setRoomState('voting')
        self.sceneManager.setAsCurrentScene(VoteScene(self.sceneManager, self.roomManager, self.gameManager))

    def update(self):
        if self.toolBar != None:
            self.toolBar.update()