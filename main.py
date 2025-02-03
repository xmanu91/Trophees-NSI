import pygame
import sys
from dotenv import load_dotenv
from scenes.HomeScene import HomeScene
from scenes.PaintingScene import PaintingScene
from ui.SceneManager import SceneManager
from utility.VotesManager import VotesManager
import utility.gameInitialisation
import utility.eventManager

load_dotenv()
pygame.init()

WIDTH, HEIGHT = 900, 500

screen = pygame.display.set_mode((WIDTH, HEIGHT))
sceneManager = SceneManager(screen)

homeScene = HomeScene(sceneManager)
paintingScene = PaintingScene(sceneManager)

sceneManager.setAsCurrentScene(paintingScene)
screen.fill((255, 255, 255))

while True:
    for event in pygame.event.get():
        utility.eventManager.update(event)
         
    sceneManager.update()
    sceneManager.draw()
    pygame.display.flip()