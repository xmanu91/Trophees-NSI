import pygame
import os

from ui.SceneManager import SceneManager
from ui.ProgressBar import ProgressBar
from ui.Button import Button 
from ui.Image import Image
from ui.Scene import Scene
from ui.Text import Text

from utility.gameInitialisation import sqlProvider
from utility.VotesManager import VotesManager
from utility.RoomManager import RoomManager
from utility.GameManager import GameManager
from utility import consolLog

from scenes.WinnerScene import WinnerScene
from time import sleep
import tempfile

class VoteScene(Scene):
    def __init__(self, sceneManager: SceneManager, roomManager: RoomManager, gameManager: GameManager):
        super().__init__()
        self.gameManager = gameManager
        self.tempdir = self.gameManager.getTempDir()
        self.sceneManager = sceneManager
        self.roomManager = roomManager
        self.votesManager = VotesManager(sqlProvider, roomManager.currentRoomID, roomManager.username, self.tempdir)
        sleep(2) # Waiting for data of all players
        self.votesManager.getDrawings()
        self.drawnList = []
        self.index = 0
        
        for drawn in os.listdir(self.tempdir.name):
            self.drawnList.append(drawn)

        self.screenWidth, self.screenHeight = sceneManager.surface.get_width(), sceneManager.surface.get_height()
        self.background = Image('assets/backgrounds/wallBackground_3.png', pygame.Rect(0, 0, self.screenWidth, self.screenHeight))
        
        self.drawRect = pygame.Rect(self.screenWidth /2 - self.screenWidth*0.35, 40, self.screenWidth*0.7, self.screenHeight*0.7)
        self.drawing = Image(os.path.join(self.tempdir.name, self.drawnList[self.index]), self.drawRect)

        self.note = 1

        self.vote1 = Button(pygame.rect.Rect((self.screenWidth/11*1) - 20, 440, 40, 40), lambda: self.setNote(1), None, None, None, "1", defaultColor=(255,255,255),  hoverColor=(119,169,198),textColor=(0,0,0), fontSize= 25)
        self.vote2 = Button(pygame.rect.Rect((self.screenWidth/11*2) - 20, 440, 40, 40), lambda: self.setNote(2), None, None, None, "2", defaultColor=(255,255,255),  hoverColor=(119,169,198),textColor=(0,0,0), fontSize= 25)
        self.vote3 = Button(pygame.rect.Rect((self.screenWidth/11*3) - 20, 440, 40, 40), lambda: self.setNote(3), None, None, None, "3", defaultColor=(255,255,255),  hoverColor=(119,169,198),textColor=(0,0,0), fontSize= 25)
        self.vote4 = Button(pygame.rect.Rect((self.screenWidth/11*4) - 20, 440, 40, 40), lambda: self.setNote(4), None, None, None, "4", defaultColor=(255,255,255),  hoverColor=(119,169,198),textColor=(0,0,0), fontSize= 25)
        self.vote5 = Button(pygame.rect.Rect((self.screenWidth/11*5) - 20, 440, 40, 40), lambda: self.setNote(5), None, None, None, "5", defaultColor=(255,255,255),  hoverColor=(119,169,198),textColor=(0,0,0), fontSize= 25)
        self.vote6 = Button(pygame.rect.Rect((self.screenWidth/11*6) - 20, 440, 40, 40), lambda: self.setNote(6), None, None, None, "6", defaultColor=(255,255,255),  hoverColor=(119,169,198),textColor=(0,0,0), fontSize= 25)
        self.vote7 = Button(pygame.rect.Rect((self.screenWidth/11*7) - 20, 440, 40, 40), lambda: self.setNote(7), None, None, None, "7", defaultColor=(255,255,255),  hoverColor=(119,169,198),textColor=(0,0,0), fontSize= 25)
        self.vote8 = Button(pygame.rect.Rect((self.screenWidth/11*8) - 20, 440, 40, 40), lambda: self.setNote(8), None, None, None, "8", defaultColor=(255,255,255),  hoverColor=(119,169,198),textColor=(0,0,0), fontSize= 25)
        self.vote9 = Button(pygame.rect.Rect((self.screenWidth/11*9) - 20, 440, 40, 40), lambda: self.setNote(9), None, None, None, "9", defaultColor=(255,255,255),  hoverColor=(119,169,198),textColor=(0,0,0), fontSize= 25)
        self.vote10 = Button(pygame.rect.Rect((self.screenWidth/11*10) -20, 440, 40, 40), lambda: self.setNote(10), None, None, None, "10", defaultColor=(255,255,255),  hoverColor=(119,169,198),textColor=(0,0,0), fontSize= 25)

        durationPerVote = 5
        self.progressBar = ProgressBar(pygame.Rect(0, 0, 900, 10), (0,255,0), durationPerVote, lambda: self.nextDrawing(self.note))
        self.progressBar.run_start()

        self.spriteGroup.add(self.background, self.drawing, self.vote1, self.vote2, self.vote3, self.vote4, self.vote5, 
        self.vote6, self.vote7, self.vote8, self.vote9, self.vote10, self.progressBar)

    def setNote(self, note: int):
        self.note = note

        for i in range(1, 11):
            button = getattr(self, f"vote{i}") # Permet d'accéder aux boutons de maniere dynamique
            if i == note:
                button.defaultColor = (0, 240, 28)
            else:
                button.defaultColor = (255, 255, 255)

    def nextDrawing(self, note: int):
        consolLog.info(self.votesManager.participants, self.index+1, note) # Debug (self.index+1 est l'index de l'image note, note ...)
        self.votesManager.vote(self.votesManager.participants[self.index], note, self.roomManager.currentRound)

        if self.index < len(self.votesManager.participants)-1:
            self.progressBar.run_start() # Re-start de la ProgressBar
            self.setNote(1) # Reset de la note

            for i in range(1, 11):
                button = getattr(self, f"vote{i}")
                button.defaultColor = (255, 255, 255)

            self.index += 1
            self.spriteGroup.remove(self.drawing)
            self.drawing = Image(os.path.join(self.tempdir.name, self.drawnList[self.index]), self.drawRect)
            self.spriteGroup.add(self.drawing)
            pygame.display.flip()
        else:
            consolLog.info(self.votesManager.getWinners())
            self.sceneManager.setAsCurrentScene(WinnerScene(self.sceneManager, self.votesManager, self.gameManager, self.roomManager))