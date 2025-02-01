import pygame
from ui.Scene import Scene
from ui.SceneManager import SceneManager
from ui.Image import Image
from ui.Text import Text
from ui.Button import Button
from scenes.HomeScene import HomeScene
from utility.RoomManager import RoomManager
import utility.eventManager as eventManager

class InRoomScene(Scene):
    def __init__(self, sceneManager: SceneManager, roomManager: RoomManager, isUserRoomCreator: bool):
        super().__init__()
        self.screenWidth, self.screenHeight = sceneManager.surface.get_width(), sceneManager.surface.get_height()
        self.roomManager = roomManager
        self.sceneManager = sceneManager
        self.isUserRoomCreator = isUserRoomCreator

        self.background = Image('assets/background.jpg', pygame.Rect(0,0, self.screenWidth, self.screenHeight))
        self.roomNameText = Text(roomManager.getCurrentRoomName(), 30, (self.screenWidth*0.1, self.screenHeight*0.1), (0,0,0), isCentered=False)
        self.subHeadText = Text('Utilisateurs connectés:', 15, (self.screenWidth*0.1, self.screenHeight*0.20), (0,0,0), isCentered=False)
        self.quitButton = Button(pygame.Rect(self.screenWidth*0.9 - 100, self.screenHeight*0.1, 100, 30), self.quitGame, None, None, None, "QUITTER", 13, (0,0,0), defaultColor=(255,255,255),  hoverColor=(119,169,198))
        self.playButton = Button(pygame.Rect(self.screenWidth*0.9 - 220, self.screenHeight*0.1, 100, 30), self.startGame, None, None, None, "JOUER", 13, (0,0,0), defaultColor=(255,255,255),  hoverColor=(119,169,198))
        
        self.spriteGroup.add(self.background, self.roomNameText, self.quitButton)
        if self.isUserRoomCreator:
            self.spriteGroup.add(self.playButton)
        
        self.connectedUsers = roomManager.getUsersInCurrentRoom()
        self.updateConnectedUsers()
        eventType = pygame.event.custom_type()
        pygame.time.set_timer(pygame.event.Event(eventType), 5000)
        eventManager.addEventHandler(eventType, self.updateConnectedUsers)
        
    def updateConnectedUsers(self, e=None): # e parameters is due to eventHandler contraints
        self.spriteGroup.empty()
        self.spriteGroup.add(self.background, self.roomNameText, self.subHeadText , self.quitButton)
        if self.isUserRoomCreator:
            self.spriteGroup.add(self.playButton)
        for i in range(len(self.connectedUsers)):
            self.spriteGroup.add(UserCard(pygame.Rect(self.screenWidth*0.1, self.screenHeight*0.25 + 50*i, self.screenWidth * 0.8, 40), self.connectedUsers[i]))
        self.connectedUsers = self.roomManager.getUsersInCurrentRoom()

    def startGame(self):
        if self.isUserRoomCreator:
            self.roomManager.setRoomState('playing')
        self.sceneManager.setAsCurrentScene(Scene())
    
    def quitGame(self):
        if self.isUserRoomCreator:
            self.roomManager.closeRoom()
        self.roomManager.closeConnection()
        self.sceneManager.setAsCurrentScene(HomeScene(self.sceneManager))
    
    def checkGameState(self):
        if self.roomManager.getRoomState() == 'playing':
            self.startGame()

class UserCard(pygame.sprite.Sprite):
    def __init__(self, rect: pygame.Rect, username: str):
        super().__init__()
        self.rect = rect
        self.text = Text(username, 20, (20, self.rect.height / 2 - 12), (255,255,255), isCentered=False)
        self.image = pygame.Surface(self.rect.size)
        self.image.fill((50,50,50))
        self.image.blit(self.text.image, self.text.rect)