import pygame
from ui.Scene import Scene
from ui.SceneManager import SceneManager
from ui.Image import Image
from ui.Text import Text
from ui.Button import Button
from utility.RoomManager import RoomManager
import utility.eventManager as eventManager

class InRoomScene(Scene):
    def __init__(self, sceneManager: SceneManager, roomManager: RoomManager):
        super().__init__()
        self.screenWidth, self.screenHeight = sceneManager.surface.get_width(), sceneManager.surface.get_height()
        self.roomManager = roomManager
        self.background = Image('assets/background.jpg', pygame.Rect(0,0, self.screenWidth, self.screenHeight))
        self.roomNameText = Text(roomManager.getCurrentRoomName(), 30, (self.screenWidth*0.1, self.screenHeight*0.1), (0,0,0), isCentered=False)
        self.quitButton = Button(pygame.Rect(self.screenWidth*0.9 - 100, self.screenHeight*0.1, 100, 30), lambda: print('quit'), None, None, None, "QUITTER", 13, (0,0,0), defaultColor=(255,255,255),  hoverColor=(119,169,198))
        self.playButton = Button(pygame.Rect(self.screenWidth*0.9 - 220, self.screenHeight*0.1, 100, 30), lambda: print('play'), None, None, None, "JOUER", 13, (0,0,0), defaultColor=(255,255,255),  hoverColor=(119,169,198))
        self.spriteGroup.add(self.background, self.roomNameText, self.quitButton, self.playButton)
        self.connectedUsers = roomManager.getUsersInCurrentRoom()
        self.updateConnectedUsers()
        eventType = pygame.event.custom_type()
        pygame.time.set_timer(pygame.event.Event(eventType), 5000)
        eventManager.addEventHandler(eventType, self.updateConnectedUsers)
        
    def updateConnectedUsers(self, e=None): # e parameters is due to eventHandler contraints
        self.spriteGroup.empty()
        self.spriteGroup.add(self.background, self.roomNameText, self.quitButton, self.playButton)
        for i in range(len(self.connectedUsers)):
            self.spriteGroup.add(UserCard(pygame.Rect(self.screenWidth*0.1, self.screenHeight*0.2 + 50*i, self.screenWidth * 0.8, 40), self.connectedUsers[i]))
        self.connectedUsers = self.roomManager.getUsersInCurrentRoom()

class UserCard(pygame.sprite.Sprite):
    def __init__(self, rect: pygame.Rect, username: str):
        super().__init__()
        self.rect = rect
        self.text = Text(username, 20, (20, self.rect.height / 2 - 12), (255,255,255), isCentered=False)
        self.image = pygame.Surface(self.rect.size)
        self.image.fill((50,50,50))
        self.image.blit(self.text.image, self.text.rect)