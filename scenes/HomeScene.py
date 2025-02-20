from ui.Scene import Scene
from ui.Text import Text
from ui.Button import Button 
from ui.SceneManager import SceneManager
from ui.Image import Image
from ui.TextInput import TextInput
from scenes.JoinRoomScene import JoinRoomScene
from utility.RoomManager import RoomManager
from utility.ErrorHandler import raiseAnError
import pygame

class HomeScene(Scene):
    def __init__(self, sceneManager: SceneManager, roomManager: RoomManager):
        super().__init__()
        screenWidth, screenHeight = sceneManager.surface.get_width(), sceneManager.surface.get_height()
        self.sceneManager = sceneManager
        self.roomManager = roomManager
        background = Image('assets/background.jpg', pygame.Rect(0,0, screenWidth, screenHeight))
        
        self.usernameInput = TextInput(pygame.rect.Rect(screenWidth / 2 - 200, screenHeight * 0.45 - 25, 400, 50), (0,0,0), (119,169,198), (255,255,255), (33,33,33, 50), placeholder="Entrez votre pseudonyme")
        playButton = Button(pygame.rect.Rect(screenWidth / 2 - 200, screenHeight * 0.63 - 37.5, 400,75), self.joinRoom, None, None, None, "JOUER !", defaultColor=(255,255,255),  hoverColor=(119,169,198),textColor=(0,0,0), fontSize= 25)
        settingsButton = Button(pygame.rect.Rect(screenWidth / 2 - 200, screenHeight * 0.8 - 37.5 , 400,75), lambda: print("Settings Not Done yet"), None, None, None, "SETTINGS ", defaultColor=(255,255,255),  hoverColor=(119,169,198),textColor=(0,0,0), fontSize= 25)
        self.spriteGroup.add(background, playButton, settingsButton, self.usernameInput)

    def joinRoom(self):
        if self.usernameInput.getText() == self.usernameInput.placeHolder or self.usernameInput.getText() == "":
            raiseAnError("Veuillez entrer un pseudonyme")   
        else:
            self.sceneManager.setAsCurrentScene(JoinRoomScene(self.sceneManager, self.usernameInput.getText(), self.roomManager))
