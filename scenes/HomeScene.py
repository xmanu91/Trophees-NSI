from ui.Scene import Scene
from ui.Text import Text
from ui.Button import Button 
from ui.SceneManager import SceneManager
from ui.Image import Image
from ui.TextInput import TextInput
from scenes.JoinRoomScene import JoinRoomScene
import pygame

class HomeScene(Scene):
    def __init__(self, sceneManager: SceneManager):
        super().__init__()
        screenWidth, screenHeight = sceneManager.surface.get_width(), sceneManager.surface.get_height()
        background = Image('assets/background.jpg', pygame.Rect(0,0, screenWidth, screenHeight))
        usernameInput = TextInput(pygame.rect.Rect(screenWidth / 2 - 200, screenHeight * 0.45 - 25, 400, 50), (0,0,0), (119,169,198), (255,255,255), (33,33,33, 50), placeholder="Entrez votre pseudonyme")
        playButton = Button(pygame.rect.Rect(screenWidth / 2 - 200, screenHeight * 0.63 - 37.5, 400,75), lambda: sceneManager.setAsCurrentScene(JoinRoomScene(sceneManager, usernameInput.getText())), None, None, None, "PLAY !", defaultColor=(255,255,255),  hoverColor=(119,169,198),textColor=(0,0,0), fontSize= 25)
        setttingsButton = Button(pygame.rect.Rect(screenWidth / 2 - 200, screenHeight * 0.8 - 37.5 , 400,75), lambda: print('Bonjour'), None, None, None, "SETTINGS ", defaultColor=(255,255,255),  hoverColor=(119,169,198),textColor=(0,0,0), fontSize= 25)
        self.spriteGroup.add(background, playButton, setttingsButton, usernameInput)