import pygame
import sys
from dotenv import load_dotenv
from ui.HomeScene import HomeScene
from ui.SceneManager import SceneManager

load_dotenv()
pygame.init()


WIDTH, HEIGHT = 900, 500

screen = pygame.display.set_mode((WIDTH, HEIGHT))
sceneManager = SceneManager(screen)
homeScene = HomeScene(sceneManager)
sceneManager.setAsCurrentScene(homeScene)
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    sceneManager.update()
    sceneManager.draw()
    pygame.display.flip()