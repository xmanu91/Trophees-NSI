from ui.Scene import Scene
from ui.Text import Text
from ui.Button import Button 
from ui.SceneManager import SceneManager
from ui.Image import Image
from ui.TextInput import TextInput
from scenes.JoinRoomScene import JoinRoomScene
from utility.RoomManager import RoomManager
import pygame
from utility.VotesManager import VotesManager
from ui.Shape import Shape

"""
    A modifier :
        - Recuperer les noms des gagnants
        - Duree de la scene
"""

class PodiumScene(Scene):
    def __init__(self, sceneManager: SceneManager, votesManager: VotesManager, sceneDuration: int = 5):
        super().__init__()
        self.sceneManager = sceneManager
        self.screenWidth, self.screenHeight = sceneManager.surface.get_width(), sceneManager.surface.get_height()
        self.votesManager = votesManager
        self.sceneDuration = sceneDuration

        self.background = Image('assets/background.jpg', pygame.Rect(0,0, self.screenWidth, self.screenHeight))
        self.spriteGroup.add(self.background)

        self.playersOnPodium = ["Azertyuiop", "Azer", "Azerty"] # Recuperer les noms des gagnants

        self.podiumDraw()

    def podiumDraw(self):
        podium1 = Shape(pygame.Rect(self.screenWidth /2 - 75, 250, 150, 250), (255, 220, 48))
        podium2 = Shape(pygame.Rect(self.screenWidth /2 - 75 - 150, 300, 150, 200), (128, 128, 128))
        podium3 = Shape(pygame.Rect(self.screenWidth /2 - 75 + 150, 350, 150, 150), (127, 65, 24))

        playerFontSize = [int((16 / len(player))*18) for player in self.playersOnPodium]
        playerOnPodium1 = Text(self.playersOnPodium[0], playerFontSize[0], (self.screenWidth /2, 250 - playerFontSize[0]/2), (255,255,255), True)
        playerOnPodium2 = Text(self.playersOnPodium[1], playerFontSize[1], (self.screenWidth /2 - 150, 300 - playerFontSize[1]/2), (255,255,255), True)
        playerOnPodium3 = Text(self.playersOnPodium[2], playerFontSize[2], (self.screenWidth /2 + 150, 350 - playerFontSize[2]/2), (255,255,255), True)

        self.spriteGroup.add(podium1, podium2, podium3, playerOnPodium1, playerOnPodium2, playerOnPodium3)     

    def update(self):
        pass