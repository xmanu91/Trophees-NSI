import pygame
import sys
from dotenv import load_dotenv
from scenes.HomeScene import HomeScene
from scenes.PaintingScene import PaintingScene
from scenes.WinnerScene import WinnerScene
from scenes.PodiumScene import PodiumScene
from ui.SceneManager import SceneManager
from utility.VotesManager import VotesManager
from utility.RoomManager import RoomManager
import utility.gameInitialisation
import utility.eventManager
from utility.SQLProvider import SQLProvider

load_dotenv()
pygame.init()

WIDTH, HEIGHT = 900, 500

screen = pygame.display.set_mode((WIDTH, HEIGHT))
sceneManager = SceneManager(screen)
sqlManager = SQLProvider()
roomManager = RoomManager(sqlManager, "Username")
votesManager = VotesManager(sqlManager, "RoomID", "Username")

homeScene = HomeScene(sceneManager, roomManager)
paintingScene = PaintingScene(sceneManager)
winnerScene = WinnerScene(sceneManager, votesManager)
podiumScene = PodiumScene(sceneManager, votesManager)

sceneManager.setAsCurrentScene(homeScene)
screen.fill((255, 255, 255))

while True:
    for event in pygame.event.get():
        utility.eventManager.update(event)

        if event.type == pygame.QUIT:
            print("Quit")
            pygame.quit()
            sys.exit()
         
    sceneManager.update()
    sceneManager.draw()
    pygame.display.flip()