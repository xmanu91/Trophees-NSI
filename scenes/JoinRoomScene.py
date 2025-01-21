from ui.Scene import Scene
from ui.Text import Text
from ui.Button import Button
from ui.SceneManager import SceneManager
from ui.Image import Image
from ui.TextInput import TextInput
import pygame

class JoinRoomScene(Scene):
    def __init__(self, sceneManager : SceneManager, username : str):
        super().__init__()
        screenWidth, screenHeight = sceneManager.surface.get_width(), sceneManager.surface.get_height()
        background = Image('assets/background.jpg', pygame.Rect(0,0, screenWidth, screenHeight))
        seekRoomNameInput = TextInput(pygame.rect.Rect(screenWidth*0.05, screenHeight * 0.10 - 25, screenWidth * 0.6, 50), (0,0,0), (119,169,198), (255,255,255), (33,33,33, 50), placeholder="Entrez le nom de la room")
        createRoomButton = Button(pygame.rect.Rect(screenWidth * 0.68, screenHeight * 0.1 - 25, 120, 50), lambda: sceneManager.setAsCurrentScene(JoinRoomScene(sceneManager, usernameInput.getText())), None, None, None, "Join !", defaultColor=(255,255,255),  hoverColor=(119,169,198),textColor=(0,0,0), fontSize= 22)
        joinRoomButton = Button(pygame.rect.Rect(screenWidth * 0.82, screenHeight * 0.1 - 25, 120, 50), lambda: sceneManager.setAsCurrentScene(JoinRoomScene(sceneManager, usernameInput.getText())), None, None, None, "Create !", defaultColor=(255,255,255),  hoverColor=(119,169,198),textColor=(0,0,0), fontSize= 22)
        self.spriteGroup.add(background, seekRoomNameInput, createRoomButton, joinRoomButton)

