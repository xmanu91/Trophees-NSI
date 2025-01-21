import pygame
import sys
from dotenv import load_dotenv
from scenes.HomeScene import HomeScene
from ui.SceneManager import SceneManager
import utility.eventManager
from scenes.VoteScene import VoteScene
from utility.VotesManager import VotesManager
import utility.gameInitialisation

load_dotenv()
pygame.init()


WIDTH, HEIGHT = 900, 500

screen = pygame.display.set_mode((WIDTH, HEIGHT))
sceneManager = SceneManager(screen)
votesManager = VotesManager(utility.gameInitialisation.sqlProvider, '1', 'Username')

homeScene = HomeScene(sceneManager)
voteScene = VoteScene(sceneManager)

sceneManager.setAsCurrentScene(voteScene)

while True:
    for event in pygame.event.get():
        utility.eventManager.update(event)

    sceneManager.update()
    sceneManager.draw()
    pygame.display.flip()