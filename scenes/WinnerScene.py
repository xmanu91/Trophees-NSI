from utility.VotesManager import VotesManager
from ui.SceneManager import SceneManager
from ui.Scene import Scene
from ui.Image import Image
from ui.Text import Text
import threading
import pygame
import time

"""
    A modifier :
        - Recuperer les gagnants
        - Duree de la scene
"""

class WinnerScene(Scene):
    def __init__(self, sceneManager: SceneManager, votesManager: VotesManager, sceneDuration: int = 5):
        super().__init__()
        self.sceneManager = sceneManager
        self.screenWidth, self.screenHeight = sceneManager.surface.get_width(), sceneManager.surface.get_height()
        self.background = Image("assets/background.jpg", pygame.Rect(0,0, self.screenWidth, self.screenHeight))
        self.spriteGroup.add(self.background)
        self.votesManager = votesManager
        self.sceneDuration = sceneDuration
        self.winners = ["Image1", "Image2"] # self.votesManager.getWinners() #self.votesManager.getWinners() mettre ici la fonction qui recupere le noms des gagnants
        
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

        self.winnersDrawings = []
        for winner in self.winners:
            self.winnersDrawings.append(Image(f"assets/temp/{winner}.png", self.drawRect))

        self.displayedDrawing = self.winnersDrawings[-1]
        self.spriteGroup.add(self.displayedDrawing)

        threading.Thread(target=self.switchDrawing).start()

    def switchDrawing(self):
        while True:   
            self.spriteGroup.remove(self.displayedDrawing)
            self.displayedDrawing = self.winnersDrawings[(self.winnersDrawings.index(self.displayedDrawing) + 1) % len(self.winnersDrawings)]
            self.spriteGroup.add(self.displayedDrawing)
            time.sleep(self.sceneDuration/2)

    def update(self):
        pass

        

