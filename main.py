import pygame
from dotenv import load_dotenv
from scenes.HomeScene import HomeScene
from ui.SceneManager import SceneManager
from utility.RoomManager import RoomManager
import utility.gameInitialisation
import utility.eventManager
from utility.SQLProvider import SQLProvider
import sys


load_dotenv()
pygame.init()

WIDTH, HEIGHT = 900, 500

screen = pygame.display.set_mode((WIDTH, HEIGHT))
sceneManager = SceneManager(screen)
roomManager = RoomManager(utility.gameInitialisation.sqlProvider, '')
homeScene = HomeScene(sceneManager, roomManager)
sceneManager.setAsCurrentScene(homeScene)

screen.fill((255, 255, 255))

while True:
    for event in pygame.event.get():
        utility.eventManager.update(event)

        if event.type == pygame.QUIT:
            roomID= roomManager.currentRoomID
            roomCreator = roomManager.getRoomCreator()
            roomManager.closeConnection()
            if roomManager.username == roomCreator:
                roomManager.closeRoom(roomID)
            pygame.quit()
            sys.exit() # Si les erreurs n'apparaissent pas, supprimer cette ligne
         
    sceneManager.update()
    sceneManager.draw()
    pygame.display.flip()