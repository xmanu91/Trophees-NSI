from ui.Scene import Scene
from ui.Text import Text
from ui.Button import Button
from ui.SceneManager import SceneManager
from utility.RoomManager import RoomManager
from ui.Image import Image
from ui.TextInput import TextInput
from typing import Callable
import utility.eventManager as eventManager
import pygame

class JoinRoomScene(Scene):
    def __init__(self, sceneManager : SceneManager, username : str, roomManager: RoomManager):
        super().__init__()
        self.screenWidth, self.screenHeight = sceneManager.surface.get_width(), sceneManager.surface.get_height()
        self.roomManager = roomManager
        self.sceneManager = sceneManager
        self.rooms = self.roomManager.getAllRooms()
        self.background = Image('assets/background.jpg', pygame.Rect(0,0, self.screenWidth, self.screenHeight))
        self.seekRoomNameInput = TextInput(pygame.rect.Rect(self.screenWidth*0.05, self.screenHeight * 0.10 - 25, self.screenWidth * 0.6, 50), (0,0,0), (119,169,198), (255,255,255), (33,33,33, 50), placeholder="Entrez le nom de la room")
        self.createRoomButton = Button(pygame.rect.Rect(self.screenWidth * 0.68, self.screenHeight * 0.1 - 25, 120, 50), lambda: sceneManager.setAsCurrentScene(JoinRoomScene(sceneManager, usernameInput.getText())), None, None, None, "Join", defaultColor=(255,255,255),  hoverColor=(119,169,198),textColor=(0,0,0), fontSize= 25)
        self.joinRoomButton = Button(pygame.rect.Rect(self.screenWidth * 0.82, self.screenHeight * 0.1 - 25, 120, 50), lambda: sceneManager.setAsCurrentScene(JoinRoomScene(sceneManager, usernameInput.getText())), None, None, None, "Create", defaultColor=(255,255,255),  hoverColor=(119,169,198),textColor=(0,0,0), fontSize= 25)

        self.spriteGroup.add(self.background, self.seekRoomNameInput, self.createRoomButton, self.joinRoomButton)

        self.updateRooms()
        eventType = pygame.event.custom_type()
        pygame.time.set_timer(pygame.event.Event(eventType), 5000)
        eventManager.addEventHandler(eventType, self.updateRooms)
       
    def updateRooms(self, e=None): # e parameters is due to eventHandler contraints
        self.spriteGroup.empty()
        self.spriteGroup.add(self.background, self.seekRoomNameInput, self.createRoomButton, self.joinRoomButton)
        for i in range(len(self.rooms)):
            self.spriteGroup.add(RoomCard(pygame.Rect(self.screenWidth*0.05, self.screenHeight*0.2 + 70*i , self.screenWidth * 0.9, 60), self.rooms[i][1], self.rooms[i][0], lambda: self.sceneManager.setAsCurrentScene(Scene()), self.roomManager))
        self.rooms = self.roomManager.getAllRooms()

class RoomCard(pygame.sprite.Sprite):
    def __init__(self, size : pygame.Rect, roomName : str, roomID : str, action: Callable, roomManager: RoomManager):
        super().__init__()
        self.rect = size
        self.roomName = roomName
        self.roomID = roomID
        self.image = pygame.Surface(self.rect.size)
        self.color = (129, 143, 129)
        self.image.fill(self.color)
        #instance des cards :
        self.numberPlayer = 0
        self.numberPlayerText = Text((str(self.numberPlayer) + " players connected"), 17, (self.rect.width /1.5, self.rect.y + 19) , (0,0,0), False)
        self.button = Button(pygame.rect.Rect(self.rect.width - 75, self.rect.y + self.rect.height/2 - 20 , 100, 40), action, None, None, None, "Join", defaultColor=(164, 212, 162),  hoverColor=(119, 161, 117),textColor=(0,0,0), fontSize= 25)
        self.text = Text(roomName , 30, (self.rect.x + 10, self.rect.y + 15), (0,0,0), False )

        self.image.blit(self.text.image , (self.text.rect.x - self.rect.x, self.text.rect.y - self.rect.y))
        self.image.blit(self.numberPlayerText.image , (self.numberPlayerText.rect.x - self.rect.x, self.numberPlayerText.rect.y - self.rect.y))


    def update(self):
        self.button.update()
        self.image.blit(self.button.image, (self.button.rect.x - self.rect.x, self.button.rect.y - self.rect.y))