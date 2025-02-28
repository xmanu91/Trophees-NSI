from ui.Scene import Scene
from ui.Text import Text 
from ui.SceneManager import SceneManager
from ui.Image import Image
import pygame
from utility.VotesManager import VotesManager
from utility.GameManager import GameManager
from ui.Shape import Shape

"""
    A modifier :
        - Recuperer les noms des gagnants
        - Duree de la scene
"""

class PodiumScene(Scene):
    def __init__(self, sceneManager: SceneManager, votesManager: VotesManager, gameManager: GameManager):
        super().__init__()
        self.sceneManager = sceneManager
        self.screenWidth, self.screenHeight = sceneManager.surface.get_width(), sceneManager.surface.get_height()
        self.votesManager = votesManager
        self.gameManager = gameManager

        self.background = Image('assets/backgrounds/wallBackground_3.png', pygame.Rect(0,0, self.screenWidth, self.screenHeight))
        self.spriteGroup.add(self.background)

        self.playersOnPodium = ["Azertyuiop", "Azer", "Azerty"] # self.votesManager.getWinners()

        podium1 = Shape(pygame.Rect(self.screenWidth /2 - 75, 250, 150, 250), (255, 220, 48))
        podiumRank1 = Text("1", 62, (self.screenWidth /2, 350 - 62/2), (255,255,255), True)
        podium2 = Shape(pygame.Rect(self.screenWidth /2 - 75 - 150, 300, 150, 200), (128, 128, 128))
        podiumRank2 = Text("2", 62, (self.screenWidth /2 - 150, 400 - 62/2), (255,255,255), True)

        if len(self.playersOnPodium) > 2:
            podium3 = Shape(pygame.Rect(self.screenWidth /2 - 75 + 150, 350, 150, 150), (127, 65, 24))
            podiumRank3 = Text("3", 62, (self.screenWidth /2 + 150, 450 - 62/2), (255,255,255), True)

        playerFontSize = [int((13 / len(player))*18) for player in self.playersOnPodium]
        playerOnPodium1 = Text(self.playersOnPodium[0], playerFontSize[0], (self.screenWidth /2, 250 - playerFontSize[0]/2), (255,255,255), True)
        playerOnPodium2 = Text(self.playersOnPodium[1], playerFontSize[1], (self.screenWidth /2 - 150, 300 - playerFontSize[1]/2), (255,255,255), True)
        
        if len(self.playersOnPodium) > 2:
            playerOnPodium3 = Text(self.playersOnPodium[2], playerFontSize[2], (self.screenWidth /2 + 150, 350 - playerFontSize[2]/2), (255,255,255), True)
            self.spriteGroup.add(playerOnPodium3, podiumRank3, podium3)

        self.quitButton = Button(pygame.Rect(self.screenWidth*0.975 - 100, self.screenHeight*0.95-30, 100, 30), self.quit, None, None, None, "Quitter", 13, (0,0,0), defaultColor=(255,255,255),  hoverColor=(119,169,198))
        
        self.spriteGroup.add(podium1, podium2, playerOnPodium1, playerOnPodium2, podiumRank1, podiumRank2, self.quitButton)

    def quit(self):
        self.tempdir = self.gameManager.getTempDir()
        self.tempdir.cleanup()
        self.connectedUsers = self.roomManager.getUsersInCurrentRoom()
        self.roomId = self.roomManager.currentRoomID
        self.roomManager.closeConnection()
        if len(self.connectedUsers)-1 <= 0 :
            self.roomManager.closeRoom(self.roomId)
        pygame.time.set_timer(self.pygameEventSwitchDrawing, 0)
        self.sceneManager.setAsCurrentScene(HomeScene.HomeScene(self.sceneManager, self.roomManager))
