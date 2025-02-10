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

        self.playersOnPodium = ["Player1", "Player2", "Player3"] # Recuperer les noms des gagnants

    def podiumDraw(self):
        podium1 = Shape(pygame.Rect(250,300, 50, 50), (255,255,255))
        podium2 = Shape(pygame.Rect(200,0, 50, 50), (255,255,255))
        podium3 = Shape(pygame.Rect(0,250, 50, 50), (255,255,255))

        self.spriteGroup.add(podium1, podium2, podium3)
        