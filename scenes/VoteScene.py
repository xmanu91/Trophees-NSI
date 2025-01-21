from ui.Scene import Scene
from ui.Text import Text
from ui.Button import Button 
from ui.SceneManager import SceneManager
from ui.Image import Image
from ui.TextInput import TextInput
import pygame
import os

"""
Pensez à changer les liens des images pour la version finale
"""

class VoteScene(Scene):
    def __init__(self, sceneManager: SceneManager):
        super().__init__()

        self.drawnList = []
        self.index = 0
        for drawn in os.listdir("assets/temp/"):
            self.drawnList.append(drawn)

        self.screenWidth, self.screenHeight = sceneManager.surface.get_width(), sceneManager.surface.get_height()
        self.background = Image('assets/votebackground.png', pygame.Rect(0, 0, self.screenWidth, self.screenHeight))
        
        self.drawing = Image("assets/temp/image1.png", pygame.Rect(40, 40, self.screenWidth - 80, self.screenHeight - 80))

        self.vote1 = Button(pygame.rect.Rect(40, 468, 75, 25), lambda: self.nextScene("Vote 1"), None, None, None, "Vote 1", defaultColor=(255,255,0),  hoverColor=(119,169,198),textColor=(0,0,0), fontSize= 25)
        self.vote2 = Button(pygame.rect.Rect(125, 468, 75, 25), lambda: self.nextScene("Vote 2"), None, None, None, "Vote 2", defaultColor=(255,255,0),  hoverColor=(119,169,198),textColor=(0,0,0), fontSize= 25)
        self.vote3 = Button(pygame.rect.Rect(210, 468, 75, 25), lambda: self.nextScene("Vote 3"), None, None, None, "Vote 3", defaultColor=(255,255,0),  hoverColor=(119,169,198),textColor=(0,0,0), fontSize= 25)
        self.vote4 = Button(pygame.rect.Rect(295, 468, 75, 25), lambda: self.nextScene("Vote 4"), None, None, None, "Vote 4", defaultColor=(255,255,0),  hoverColor=(119,169,198),textColor=(0,0,0), fontSize= 25)
        self.vote5 = Button(pygame.rect.Rect(380, 468, 75, 25), lambda: self.nextScene("Vote 5"), None, None, None, "Vote 5", defaultColor=(255,255,0),  hoverColor=(119,169,198),textColor=(0,0,0), fontSize= 25)
        self.vote6 = Button(pygame.rect.Rect(465, 468, 75, 25), lambda: self.nextScene("Vote 6"), None, None, None, "Vote 6", defaultColor=(255,255,0),  hoverColor=(119,169,198),textColor=(0,0,0), fontSize= 25)
        self.vote7 = Button(pygame.rect.Rect(550, 468, 75, 25), lambda: self.nextScene("Vote 7"), None, None, None, "Vote 7", defaultColor=(255,255,0),  hoverColor=(119,169,198),textColor=(0,0,0), fontSize= 25)
        self.vote8 = Button(pygame.rect.Rect(635, 468, 75, 25), lambda: self.nextScene("Vote 8"), None, None, None, "Vote 8", defaultColor=(255,255,0),  hoverColor=(119,169,198),textColor=(0,0,0), fontSize= 25)
        self.vote9 = Button(pygame.rect.Rect(720, 468, 75, 25), lambda: self.nextScene("Vote 9"), None, None, None, "Vote 9", defaultColor=(255,255,0),  hoverColor=(119,169,198),textColor=(0,0,0), fontSize= 25)
        self.vote10 = Button(pygame.rect.Rect(805, 468, 75, 25), lambda: self.nextScene("Vote 10"), None, None, None, "Vote 10", defaultColor=(255,255,0),  hoverColor=(119,169,198),textColor=(0,0,0), fontSize= 25)

        self.spriteGroup.add(self.background, self.drawing, self.vote1, self.vote2, self.vote3, self.vote4, self.vote5, self.vote6, self.vote7, self.vote8, self.vote9, self.vote10)

    def nextScene(self, note):
        print(self.index+1, note) # Debug (self.index+1 est l'index de l'image note, note ...)
        print("Sending vote to server") # Mettre ici l'envoi de vote

        if self.index < len(self.drawnList) - 1:
            self.index += 1
            self.spriteGroup.remove(self.drawing)
            self.drawing = Image("assets/temp/" + self.drawnList[self.index], pygame.Rect(40, 40, self.screenWidth - 80, self.screenHeight - 80))
            self.spriteGroup.add(self.drawing)
            pygame.display.flip()
        else:
            print("VoteScene finished") # Passez à la scene suivante (HomeScene)