import pygame
from ui.Scene import Scene
from ui.SceneManager import SceneManager
from ui.Image import Image
from ui.Text import Text
from ui.Button import Button
from utility.RoomManager import RoomManager
from time import sleep

class InRoomScene(Scene):
    def __init__(self, sceneManager: SceneManager, roomManager: RoomManager):
        super().__init__()
        self.screenWidth, self.screenHeight = sceneManager.surface.get_width(), sceneManager.surface.get_height()
        self.roomManager = roomManager
        background = Image('assets/background.jpg', pygame.Rect(0,0, self.screenWidth, self.screenHeight))
        roomName = Text(roomManager.getCurrentRoomName(), 30, (self.screenWidth*0.1, self.screenHeight*0.1), (0,0,0), isCentered=False)
        quitButton = Button(pygame.Rect(self.screenWidth*0.9 - 100, self.screenHeight*0.1, 100, 30), lambda: print('quit'), None, None, None, "QUITTER", 13, (0,0,0), defaultColor=(255,255,255),  hoverColor=(119,169,198))
        self.connectedUsers = roomManager.getUsersInCurrentRoom()
        self.spriteGroup.add(background, roomName, quitButton)
        self.updateConnectedUsers()
        
    def updateConnectedUsers(self):
        for i in range(len(self.connectedUsers)):
            self.spriteGroup.add(UserCard(pygame.Rect(self.screenWidth*0.1, self.screenHeight*0.2 + 50*i, self.screenWidth * 0.8, 40), self.connectedUsers[i]))
        sleep(5)
        self.connectedUsers = self.roomManager.getUsersInCurrentRoom()
        self.updateConnectedUsers()


class UserCard(pygame.sprite.Sprite):
    def __init__(self, rect: pygame.Rect, username: str):
        super().__init__()
        self.rect = rect
        text = Text(username, 20, (20, self.rect.height / 2 - 12), (255,255,255), isCentered=False)
        self.image = pygame.Surface(self.rect.size)
        self.image.fill((50,50,50))
        self.image.blit(text.image, text.rect)
