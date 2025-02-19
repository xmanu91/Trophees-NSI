import pygame
from ui.Scene import Scene
from ui.Text import Text
from ui.Button import Button
from ui.SceneManager import SceneManager
from ui.Image import Image
from ui.TextInput import TextInput

from scenes.InRoomScene import InRoomScene

from utility.RoomManager import RoomManager
import utility.eventManager

class JoinRoomScene(Scene):
    def __init__(self, sceneManager : SceneManager, username : str, roomManager: RoomManager):
        super().__init__()
        print('join room scene init')
        self.screenWidth, self.screenHeight = sceneManager.surface.get_width(), sceneManager.surface.get_height()
        self.roomManager = roomManager
        self.roomManager.setUsername(username)
        self.sceneManager = sceneManager
        self.rooms = self.roomManager.getAllRooms()
        self.background = Image('assets/background.jpg', pygame.Rect(0,0, self.screenWidth, self.screenHeight))
        self.seekRoomNameInput = TextInput(pygame.rect.Rect(self.screenWidth*0.05, self.screenHeight * 0.10 - 25, self.screenWidth * 0.6, 50), (0,0,0), (119,169,198), (255,255,255), (33,33,33, 50), placeholder="Entrez le nom de la room")
        self.joinRoomButton = Button(pygame.rect.Rect(self.screenWidth * 0.68, self.screenHeight * 0.1 - 25, 120, 50), self.joinRoom, None, None, None, "Rejoindre", defaultColor=(255,255,255),  hoverColor=(119,169,198),textColor=(0,0,0), fontSize= 25)
        self.createRoomButton = Button(pygame.rect.Rect(self.screenWidth * 0.82, self.screenHeight * 0.1 - 25, 120, 50), self.createRoom, None, None, None, "Créer", defaultColor=(255,255,255),  hoverColor=(119,169,198),textColor=(0,0,0), fontSize= 25)
        self.updateRoomsButton = Button(pygame.rect.Rect(self.screenWidth * 0.82, self.screenHeight * 0.25 - 15, 120, 30), self.updateRooms, None, None, None, "Actualiser", defaultColor=(0,0,0,0), hoverColor=(119,169,198), textColor=(255,255,255), fontSize= 18)

        self.spriteGroup.add(self.background, self.seekRoomNameInput, self.createRoomButton, self.joinRoomButton, self.updateRoomsButton)
        self.updateRooms()
       
    def updateRooms(self, e=None): # e parameters is due to eventHandler contraints
        print('updateRoom')
        self.spriteGroup.empty()
        self.spriteGroup.add(self.background, self.seekRoomNameInput, self.createRoomButton, self.joinRoomButton, self.updateRoomsButton)
        for i in range(len(self.rooms)):
            self.spriteGroup.add(RoomCard(pygame.Rect(self.screenWidth*0.05, self.screenHeight*0.3 + 70*i , self.screenWidth * 0.9, 60), 
                                          self.rooms[i][2], 
                                          self.rooms[i][0], 
                                          self.roomManager,
                                          self.sceneManager))
        self.rooms = self.roomManager.getAllRooms()
    
    def joinRoom(self):
        self.roomManager.createConnection(self.seekRoomNameInput.getText())
        self.sceneManager.setAsCurrentScene(InRoomScene(self.sceneManager, self.roomManager, False))
    
    def createRoom(self):
        self.roomManager.createRoom(self.seekRoomNameInput.getText())
        self.sceneManager.setAsCurrentScene(InRoomScene(self.sceneManager, self.roomManager, True))

class RoomCard(pygame.sprite.Sprite):
    def __init__(self, size : pygame.Rect, roomName : str, roomID : int, roomManager: RoomManager, sceneManager: SceneManager):
        super().__init__()
        self.rect = size
        self.roomName = roomName
        self.roomManager = roomManager
        self.sceneManager = sceneManager
        self.roomID = roomID
        self.image = pygame.Surface(self.rect.size)
        self.color = (129, 143, 129)
        self.image.fill(self.color)

        #instance des cards :
        self.numberPlayer = roomManager.getConnectedUsersNumberInRoom(roomID)
        self.numberPlayerText = Text((str(self.numberPlayer) + " joueurs connectés"), 17, (self.rect.width /1.5, self.rect.y + 19) , (0,0,0), False)
        self.button = Button(
            pygame.rect.Rect(self.rect.width - 75, self.rect.y + self.rect.height/2 - 20 , 100, 40), 
            self.onButtonPressed, None, None, None, "Rejoindre", defaultColor=(164, 212, 162), hoverColor=(119, 161, 117),textColor=(0,0,0), fontSize= 20)
        
        self.text = Text(roomName , 30, (self.rect.x + 10, self.rect.y + 15), (0,0,0), False )
        self.image.blit(self.text.image, (self.text.rect.x - self.rect.x, self.text.rect.y - self.rect.y))
        self.image.blit(self.numberPlayerText.image, (self.numberPlayerText.rect.x - self.rect.x, self.numberPlayerText.rect.y - self.rect.y))

    def onButtonPressed(self):
        self.roomManager.createConnection(self.roomID)
        self.sceneManager.setAsCurrentScene(InRoomScene(self.sceneManager, self.roomManager, False))

    def update(self):
        self.button.update()
        self.image.blit(self.button.image, (self.button.rect.x - self.rect.x, self.button.rect.y - self.rect.y))