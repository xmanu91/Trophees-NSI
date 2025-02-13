import pygame

from ui.SceneManager import SceneManager
from ui.Scene import Scene
from ui.Image import Image
from ui.Canva import Canva
from ui.Timer import Timer
from ui.Text import Text
from ui.ProgressBar import ProgressBar

from scenes.PaintingSceneComponent.ToolBar import ToolBar
from scenes.VoteScene import VoteScene

from utility.GameManager import GameManager
from utility.gameInitialisation import sqlProvider
from utility.RoomManager import RoomManager

class PaintingScene(Scene):
    def __init__(self, sceneManager: SceneManager, roomManager: RoomManager):
        super().__init__()
        print('Initialisation de Painting Scene')
        screenWidth, screenHeight = sceneManager.surface.get_width(), sceneManager.surface.get_height()
        self.background = Image("assets/background_theme.png", pygame.Rect(0,0, screenWidth, screenHeight))
        self.roomManager = roomManager
        self.sceneManager = sceneManager
        self.gameManager = GameManager(sqlProvider, roomManager.username, roomManager.currentRoomID)
        self.gameManager.drawTheme()
        self.theme = self.gameManager.drawingTheme

        self.textTheme = Text(self.theme, 32, (450, 250-16), (255,255,255), True)

        themeTimerDuration = 5
        gameTimerDuration = 20
        self.textThemeTimer = Text(str(themeTimerDuration), 32, (450, 250+16), (255,255,255), True)
        self.gameProgressBar = ProgressBar(pygame.Rect(200, 0, screenWidth-200, 10), (0, 255, 0), gameTimerDuration, self.endDrawing)
        self.themeTimer = Timer(themeTimerDuration, self.textThemeTimer, self.setCanva)
        self.canva = Canva(pygame.Rect(200, 0, 700, 500), (255, 255, 255), (0, 0, 0), roomManager.username)
        self.toolBar = None
        self.spriteGroup.add(self.background, self.textThemeTimer, self.textTheme)

        self.themeTimer.startTimer()
        
    def setCanva(self):
        self.spriteGroup.empty()
        self.toolBar = ToolBar(self.canva, self.spriteGroup, self.theme)
        self.spriteGroup.add(self.canva, self.gameProgressBar)
        self.gameProgressBar.run_start()

    def endDrawing(self):
        self.canva.save()
        self.gameManager.sendDrawing("assets/temp/" + self.roomManager.username.strip() + "_drawing.png")
        self.roomManager.setRoomState('voting')
        self.sceneManager.setAsCurrentScene(VoteScene(self.sceneManager, self.roomManager))

    def update(self):
        if self.toolBar != None:
            self.toolBar.update()