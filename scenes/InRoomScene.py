import pygame
import scenes.HomeScene
from ui.Scene import Scene
from ui.SceneManager import SceneManager
from ui.Image import Image
from ui.Text import Text
from ui.Button import Button

from scenes.PaintingScene import PaintingScene

from utility.RoomManager import RoomManager
import utility.eventManager as eventManager

class InRoomScene(Scene):
    def __init__(self, sceneManager: SceneManager, roomManager: RoomManager, isUserRoomCreator: bool):
        super().__init__()
        self.screenWidth, self.screenHeight = sceneManager.surface.get_width(), sceneManager.surface.get_height()
        self.roomManager = roomManager
        self.sceneManager = sceneManager
        self.isUserRoomCreator = isUserRoomCreator
        print('In RoomId:', self.roomManager.currentRoomID)

        self.background = Image('assets/background.jpg', pygame.Rect(0,0, self.screenWidth, self.screenHeight))
        self.roomNameText = Text(roomManager.getCurrentRoomName(), 30, (self.screenWidth*0.1, self.screenHeight*0.1), (0,0,0), isCentered=False)
        self.subHeadText = Text('Utilisateurs connectés:', 15, (self.screenWidth*0.1, self.screenHeight*0.20), (0,0,0), isCentered=False)
        self.playButton = Button(pygame.Rect(self.screenWidth*0.9 - 220, self.screenHeight*0.1, 100, 30), self.startGame, None, None, None, "JOUER", 13, (0,0,0), defaultColor=(255,255,255),  hoverColor=(119,169,198))
        self.quitButton = Button(pygame.Rect(self.screenWidth*0.9 - 100, self.screenHeight*0.1, 100, 30), self.quitGame, None, None, None, "QUITTER", 13, (0,0,0), defaultColor=(255,255,255),  hoverColor=(119,169,198))
        
        self.spriteGroup.add(self.background, self.roomNameText, self.quitButton)
        if self.isUserRoomCreator:
            self.spriteGroup.add(self.playButton)
        
        self.connectedUsers = roomManager.getUsersInCurrentRoom()
        self.updateConnectedUsers()
        self.updateUsersEventType = pygame.event.custom_type()
        self.updateStateEventType = pygame.event.custom_type()
        print('updateUserType:', self.updateUsersEventType, 'updateStateType:', self.updateStateEventType)
        pygame.time.set_timer(pygame.event.Event(self.updateUsersEventType), 5000)
        pygame.time.set_timer(pygame.event.Event(self.updateStateEventType), 1000)
        eventManager.addEventHandler(self.updateUsersEventType, self.updateConnectedUsers)
        eventManager.addEventHandler(self.updateStateEventType, self.checkGameState)
        
    def updateConnectedUsers(self, e=None): # e parameters is due to eventHandler contraints
        print('executed')
        self.spriteGroup.empty()
        self.spriteGroup.add(self.background, self.roomNameText, self.subHeadText , self.quitButton)
        if self.isUserRoomCreator:
            self.spriteGroup.add(self.playButton)
        for i in range(len(self.connectedUsers)):
            self.spriteGroup.add(UserCard(pygame.Rect(self.screenWidth*0.1, self.screenHeight*0.25 + 50*i, self.screenWidth * 0.8, 40), self.connectedUsers[i]))
        self.connectedUsers = self.roomManager.getUsersInCurrentRoom()

    def startGame(self):
        print('start game')
        if self.isUserRoomCreator:
            self.roomManager.setRoomState('playing')
        pygame.time.set_timer(pygame.event.Event(self.updateUsersEventType), 0)
        pygame.time.set_timer(pygame.event.Event(self.updateStateEventType), 0)
        self.sceneManager.setAsCurrentScene(PaintingScene(self.sceneManager, self.roomManager))
    
    def quitGame(self):
        print('quit game')
        if self.isUserRoomCreator:
            self.roomManager.closeRoom(self.roomManager.currentRoomID)
        pygame.time.set_timer(pygame.event.Event(self.updateUsersEventType), 0)
        pygame.time.set_timer(pygame.event.Event(self.updateStateEventType), 0)
        self.roomManager.closeConnection()
        self.sceneManager.setAsCurrentScene(scenes.JoinRoomScene.JoinRoomScene(self.sceneManager, self.roomManager.username, self.roomManager)) 
        if len(self.connectedUsers) == 0 :
            self.roomManager.closeRoom(self.roomId)
    
    def checkGameState(self, e=None): # e is due to the event manager requirements
        print('check game check')
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

