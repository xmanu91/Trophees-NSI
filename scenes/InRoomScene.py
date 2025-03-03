import pygame
import scenes
import time

import scenes.PaintingScene
import scenes.RoomSettingsScene
from ui.Scene import Scene
from ui.SceneManager import SceneManager
from ui.Image import Image
from ui.Text import Text
from ui.Button import Button

from utility.gameInitialisation import sqlProvider
from utility.ErrorHandler import raiseAnError
from utility.RoomManager import RoomManager
from utility.GameManager import GameManager
import utility.eventManager as eventManager
import utility.consolLog as consolLog

class InRoomScene(Scene):
    def __init__(self, sceneManager: SceneManager, roomManager: RoomManager, isUserRoomCreator: bool):
        super().__init__()
        self.screenWidth, self.screenHeight = sceneManager.surface.get_width(), sceneManager.surface.get_height()
        self.roomManager = roomManager
        self.sceneManager = sceneManager
        self.isUserRoomCreator = isUserRoomCreator
        self.connected_users = self.roomManager.getUsersInCurrentRoom()
        self.gameManager = GameManager(sqlProvider, roomManager.username, roomManager.currentRoomID)
        self.roomManager.setRoundsNumber(1)
        consolLog.info('In RoomId:', self.roomManager.currentRoomID)

        self.background = Image('assets/backgrounds/paperBackground_2.png', pygame.Rect(0,0, self.screenWidth, self.screenHeight))
        self.roomNameText = Text(roomManager.getCurrentRoomName(), 30, (self.screenWidth*0.05, self.screenHeight * 0.1 - 25), (0,0,0), isCentered=False)
        self.idDisplay = Text("ID: " + str(self.roomManager.currentRoomID), 15, (self.screenWidth*0.05, self.screenHeight*0.12), (0,0,0), isCentered=False)
        self.subHeadText = Text(f'Utilisateurs connectés ({str(len(self.roomManager.getUsersInCurrentRoom()))}):', 15, (self.screenWidth*0.05, self.screenHeight*0.16), (0,0,0), isCentered=False)
        
        if self.isUserRoomCreator:
            updateButtonRect = pygame.Rect(self.screenWidth*0.60, self.screenHeight*0.95-30, 100, 30)
        else:
            updateButtonRect = pygame.Rect(self.screenWidth*0.975 - 100, self.screenHeight*0.95-30, 100, 30)
            

        self.quitButton = Button(pygame.Rect(self.screenWidth*0.02, self.screenHeight*0.95-30, 100, 30), self.quitGame, None, None, None, "Quitter", 15, (0,0,0), defaultColor=(255,255,255),  hoverColor=(119,169,198))
        self.updateRoomsButton = Button(updateButtonRect, self.updateConnectedUsers, None, None, None, "Actualiser", 15, (0,0,0), defaultColor=(255,255,255), hoverColor=(119,169,198))        
        self.roomSettings = Button(pygame.Rect(self.screenWidth*0.73, self.screenHeight*0.95-30, 100, 30), self.openRoomSettings, None, None, None, "Paramètres", 15, (0,0,0), defaultColor=(255,255,255), hoverColor=(119,169,198))
        self.playButton = Button(pygame.Rect(self.screenWidth*0.975 - 100, self.screenHeight*0.95-30, 100, 30), self.startGame, None, None, None, "Jouer", 15, (0,0,0), defaultColor=(255,255,255),  hoverColor=(119,169,198))

        self.spriteGroup.add(
            self.background, self.roomNameText, self.subHeadText , self.quitButton, self.updateRoomsButton, 
            self.idDisplay)

        if self.isUserRoomCreator:
            self.spriteGroup.add(self.playButton)
        
        self.connectedUsers = self.roomManager.getUsersInCurrentRoom()
        self.updateConnectedUsers()

        self.updateStateEventType = pygame.event.custom_type()
        pygame.time.set_timer(pygame.event.Event(self.updateStateEventType), 1000)
        eventManager.addEventHandler(self.updateStateEventType, self.checkGameState)
        
    def updateConnectedUsers(self, e=None): # e parameters is due to eventHandler contraints
        consolLog.info('Actualisation...')
        self.spriteGroup.empty()

        self.subHeadText.setText(f'Utilisateurs connectés ({str(len(self.roomManager.getUsersInCurrentRoom()))}):')

        self.spriteGroup.add(
            self.background, self.roomNameText, self.subHeadText , self.quitButton, self.updateRoomsButton, 
            self.idDisplay)
        
        if self.isUserRoomCreator:
            self.spriteGroup.add(self.playButton, self.roomSettings)

        for i in range(len(self.connectedUsers)): # Mettre la couronne 
            if self.connectedUsers[i] == self.roomManager.getRoomCreator():
                self.spriteGroup.add(UserCard(pygame.Rect(self.screenWidth*0.06 + self.screenWidth * 0.295 * (i % 3), self.screenHeight*0.21 + 50*(i // 3), self.screenWidth * 0.285 , 40), self.connectedUsers[i], True))
            else:
                self.spriteGroup.add(UserCard(pygame.Rect(self.screenWidth*0.06 + self.screenWidth * 0.295 * (i % 3), self.screenHeight*0.21 + 50*(i // 3), self.screenWidth * 0.285 , 40), self.connectedUsers[i], False))

        self.connectedUsers = self.roomManager.getUsersInCurrentRoom()

    def startGame(self):
        self.dev = True
        self.playButton.disable()
        if len(self.connectedUsers) < 2 and self.dev == False:
            raiseAnError("Vous devez être plusieurs pour pouvoir jouer")
            self.updateConnectedUsers()
        else:
            if self.isUserRoomCreator:
                self.roomManager.setRoomState('playing')
            else:
                time.sleep(2)
            pygame.time.set_timer(pygame.event.Event(self.updateStateEventType), 0)
            paintingScene = scenes.PaintingScene.PaintingScene(self.sceneManager, self.roomManager, self.gameManager)
            self.sceneManager.setAsCurrentScene(paintingScene)
            
    def quitGame(self):
        consolLog.info("Room quitter")
        if self.isUserRoomCreator:
            self.roomManager.closeRoom(self.roomManager.currentRoomID)
        pygame.time.set_timer(pygame.event.Event(self.updateStateEventType), 0)
        self.roomManager.closeConnection()
        self.sceneManager.setAsCurrentScene(scenes.JoinRoomScene.JoinRoomScene(self.sceneManager, self.roomManager.username, self.roomManager)) 
        if len(self.connectedUsers) == 0 :
            self.roomManager.closeRoom(self.roomId)

    def checkGameState(self, e=None): # e is due to the event manager requirements
        if self.roomManager.getRoomState() == 'playing':
            self.startGame()

    def openRoomSettings(self):
        self.sceneManager.setAsCurrentScene(scenes.RoomSettingsScene.RoomSettingsScene(self.sceneManager, self.roomManager, self, self.gameManager), False)

class UserCard(pygame.sprite.Sprite):
    def __init__(self, rect: pygame.Rect, username: str, isCreator: bool):
        super().__init__()
        self.rect = rect

        self.text = Text(username, 20, (self.rect.w/2, self.rect.h/2), (255,255,255), isCentered=True)

        if isCreator:
            self.emoji = Text("👑", 20, (self.rect.w/2 + self.text.rect.w/2 + 16, self.rect.h/2 - 1), (255,255,255), isCentered=True, fontFamily="FirefoxEmoji.ttf")

        self.image = pygame.Surface(self.rect.size)
        self.image.fill((50, 50, 50))
        self.image.blit(self.text.image, self.text.rect)
        if isCreator:
            self.image.blit(self.emoji.image, self.emoji.rect)