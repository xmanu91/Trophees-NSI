from utility.ErrorHandler import ErrorHandlerUi, errorEventType
from utility.RoomManager import RoomManager
from ui.SceneManager import SceneManager
from scenes.HomeScene import HomeScene
import utility.gameInitialisation
from utility.tools import getPath
from dotenv import load_dotenv
from utility import consolLog
from ui.Button import Button
import utility.eventManager
import utility.SQLProvider
import pygame
import sys
import os

if getattr(sys, 'frozen', False):
    dotenv_path = os.path.join(sys._MEIPASS, '.env')
else:
    dotenv_path = '.env'

load_dotenv(dotenv_path=dotenv_path)

pygame.init()
pygame.display.set_caption("Inkspired v1.? (Pre-release)")
pygame.display.set_icon(pygame.image.load(getPath("assets/icons/Inkspired.png")))

WIDTH, HEIGHT = 900, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
errorHandler = ErrorHandlerUi()
utility.eventManager.addEventHandler(errorEventType, errorHandler.raiseError)

sceneManager = SceneManager(screen)
Button.sceneManager = sceneManager

roomManager = RoomManager(utility.gameInitialisation.sqlProvider, '')
homeScene = HomeScene(sceneManager, roomManager)
sceneManager.setAsCurrentScene(homeScene)

screen.fill((255, 255, 255))

while True:
    for event in pygame.event.get():
        utility.eventManager.update(event)

        if event.type == pygame.QUIT:
            if roomManager.currentRoomID != None:
                roomID= roomManager.currentRoomID
                roomCreator = roomManager.getRoomCreator()
                roomManager.closeConnection()
                if roomManager.username == roomCreator:
                    roomManager.closeRoom(roomID)
            utility.gameInitialisation.sqlProvider.closeConnection()
            pygame.quit()
            consolLog.info("Quit")
            sys.exit() # Si les erreurs n'apparaissent pas, supprimer cette ligne
         
    sceneManager.update()
    sceneManager.draw()
    errorHandler.spriteGroup.update()
    errorHandler.spriteGroup.draw(screen)
    pygame.display.flip()