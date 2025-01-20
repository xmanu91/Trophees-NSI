import pygame
from time import sleep
from Canva import Canva

pygame.init()
screen = pygame.display.set_mode((900,500))

canva=Canva(0,0,900,500,(255,255,255),(0,0,0))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

    canva.update()
    screen.blit(canva.image, canva.rect)
    pygame.display.flip()