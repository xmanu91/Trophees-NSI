from ui.Scene import Scene
from ui.Button import Button 
from ui.SceneManager import SceneManager
from ui.Image import Image
from ui.TextInput import TextInput
from utility.RoomManager import RoomManager
from utility.ErrorHandler import raiseAnError
from ui.Text import Text
from utility.GameManager import GameManager
import json
import tempfile
import os

import pygame

class RoomSettingsScene(Scene):
    def __init__(self, sceneManager: SceneManager, roomManager: RoomManager, previousScene: Scene, gameManager: GameManager):
        super().__init__()
        screenWidth, screenHeight = sceneManager.surface.get_width(), sceneManager.surface.get_height()
        self.sceneManager = sceneManager
        self.roomManager = roomManager
        self.previousScene = previousScene
        self.gameManager = gameManager
        background = Image('assets/background.jpg', pygame.Rect(0,0, screenWidth, screenHeight))

        self.Text = Text("Paramètres", 30, (screenWidth*0.15, screenHeight*0.15), (0,0,0), isCentered=True)
        self.textNbRound = Text("Nombre de tours : ", 22, (screenWidth*0.1, screenHeight*0.25), (0,0,0), isCentered=False)
        self.textDurationRound = Text("Duree de la partie (en sec): ", 22, (screenWidth*0.1, screenHeight*0.35), (0,0,0), isCentered=False)

        self.textInputNbRound = TextInput(pygame.Rect(screenWidth*0.38, screenHeight*0.25, 100, 30), (0,0,0), (119,169,198), (255,255,255), (33,33,33, 50), placeholder="1", fontSize=22)
        self.textInputDurationRound = TextInput(pygame.Rect(screenWidth*0.38, screenHeight*0.35, 100, 30), (0,0,0), (119,169,198), (255,255,255), (33,33,33, 50), placeholder="60", fontSize=22)

        self.buttonBack = Button(pygame.Rect(screenWidth*0.05, screenHeight*0.95-50, 100, 50), self.back, None, None, None, "Annuler", defaultColor=(255,255,255),  hoverColor=(119,169,198),textColor=(0,0,0), fontSize=22)
        self.buttonSave = Button(pygame.Rect(screenWidth*0.95-100, screenHeight*0.95-50, 100, 50), self.save, None, None, None, "Appliquer", defaultColor=(255,255,255),  hoverColor=(119,169,198),textColor=(0,0,0), fontSize=22)

        self.spriteGroup.add(background, self.Text, self.textNbRound, self.textDurationRound, self.textInputNbRound, self.textInputDurationRound, self.buttonBack, self.buttonSave)

    def back(self):
        self.sceneManager.setAsCurrentScene(self.previousScene)
        self.previousScene.update()
        
    def save(self):
        try:
            self.roomManager.setRoundsNumber(int(self.textInputNbRound.getText()))
            self.roomManager.setRoundTime(int(self.textInputDurationRound.getText()))
            self.back()
        except ValueError:
            raiseAnError("Veuillez entrer des nombres pour les champs de saisie")
        