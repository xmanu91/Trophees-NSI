from utility.VotesManager import VotesManager
import utility.eventManager as eventManager
from utility.GameManager import GameManager
from ui.SceneManager import SceneManager
import utility.RoomManager as RoomManager
from scenes import HomeScene, PaintingScene
from ui.Scene import Scene
from ui.Image import Image
from ui.Text import Text
from ui.Button import Button
import pygame
import time
import os

"""
    A modifier :
        - Duree de la scene
"""

class WinnerScene(Scene):
    def __init__(self, sceneManager: SceneManager, votesManager: VotesManager, gameManager: GameManager, roomManager: RoomManager,sceneDuration: int = 5):
        super().__init__()
        self.sceneManager = sceneManager
        self.roomManager = roomManager
        self.screenWidth, self.screenHeight = sceneManager.surface.get_width(), sceneManager.surface.get_height()
        self.background = Image("assets/backgrounds/wallBackground_3.png", pygame.Rect(0,0, self.screenWidth, self.screenHeight))
        self.spriteGroup.add(self.background)
        self.gameManager = gameManager
        
        self.votesManager = votesManager
        self.tempdir = self.gameManager.getTempDir()
        self.sceneDuration = sceneDuration
        time.sleep(2) # Waiting for data of all users
        self.winners =  self.votesManager.getWinners()
        print(f"self.winners: {self.winners}")

        if self.roomManager.currentRound == self.roomManager.getRoundsNumber():
            self.QuitButton = Button(pygame.Rect(self.screenWidth*0.975 - 100, self.screenHeight*0.95-30, 100, 30), self.quit, None, None, None, "QUITTER", 13, (0,0,0), defaultColor=(255,255,255),  hoverColor=(119,169,198))
            self.spriteGroup.add(self.QuitButton)
        elif self.roomManager.currentRound < self.roomManager.getRoundsNumber() and self.roomManager.username == self.roomManager.getRoomCreator():
            self.nextRoundButton = Button(pygame.Rect(self.screenWidth*0.975 - 100, self.screenHeight*0.95-30, 100, 30), self.nextRound, None, None, None, "NEXT ROUND", 13, (0,0,0), defaultColor=(255,255,255),  hoverColor=(119,169,198))
            self.spriteGroup.add(self.nextRoundButton)
        else:
            self.updateStateEventType = pygame.event.custom_type()
            print('updateStateType:', self.updateStateEventType)
            pygame.time.set_timer(pygame.event.Event(self.updateStateEventType), 1000)
            eventManager.addEventHandler(self.updateStateEventType, self.checkGameState)

        self.text = ""
        if len(self.winners) == 1:
            self.text = "Le gagnant est : "
        else:
            self.text = "Les gagnants sont : "
        for winner in self.winners:
            self.text += winner + ", "
        self.text = self.text[:-2]

        self.textLabel = Text(self.text, 32, (450, 450), (255,255,255), True)
        self.spriteGroup.add(self.textLabel)    

        self.drawRect = pygame.Rect(self.screenWidth /2 - self.screenWidth*0.35, 40, self.screenWidth*0.7, self.screenHeight*0.7)

        for winner in self.winners:
            self.votesManager.getDrawing(winner)

        self.winnersDrawings = []
        for winner in self.winners:
            self.winnersDrawings.append(Image(os.path.join(self.tempdir.name, winner.strip() + ".png"), self.drawRect))

        self.displayedDrawing = self.winnersDrawings[-1]
        self.spriteGroup.add(self.displayedDrawing)

        self.pygameEventSwitchDrawing = pygame.event.custom_type()
        if len(self.winnersDrawings) > 1:
            pygame.time.set_timer(self.pygameEventSwitchDrawing, int(self.sceneDuration/2)*1000)
            eventManager.addEventHandler(self.pygameEventSwitchDrawing, self.switchDrawing)

    def switchDrawing(self, event):  # Event
        print("Switching drawing") 
        self.spriteGroup.remove(self.displayedDrawing)
        self.displayedDrawing = self.winnersDrawings[(self.winnersDrawings.index(self.displayedDrawing) + 1) % len(self.winnersDrawings)]
        self.spriteGroup.add(self.displayedDrawing)

    def checkGameState(self, e=None): # e is due to the event manager requirements
        print('check game state')
        if self.roomManager.getRoomState() == 'playing':
            print("new round started")
            self.nextRound()
        else:
            print("game not started")

    def nextRound(self):
        if self.roomManager.username == self.roomManager.getRoomCreator():
            self.roomManager.setRoomState('playing')
        else:
            pygame.time.set_timer(pygame.event.Event(self.updateStateEventType), 0)
        self.sceneManager.setAsCurrentScene(PaintingScene.PaintingScene(self.sceneManager, self.roomManager, self.gameManager))
        
    def quit(self):
        self.tempdir = self.gameManager.getTempDir()
        self.tempdir.cleanup()
        self.connectedUsers = self.roomManager.getUsersInCurrentRoom()
        self.roomId = self.roomManager.currentRoomID
        self.roomManager.closeConnection()
        print(f"self.connectedUsers: {len(self.connectedUsers)-1}")
        if len(self.connectedUsers)-1 <= 0 :
            self.roomManager.closeRoom(self.roomId)
        pygame.time.set_timer(self.pygameEventSwitchDrawing, 0)
        self.sceneManager.setAsCurrentScene(HomeScene.HomeScene(self.sceneManager, self.roomManager))
