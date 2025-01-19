import pygame
import sys

pygame.init()
screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption('Champ de saisie de texte')

blanc = (255, 255, 255)
police = pygame.font.Font(None, 32)

input_box = pygame.Rect(30, 100, 140, 32)
couleur_active = pygame.Color('lightskyblue3')
couleur_inactive = pygame.Color('dodgerblue2')
couleur = couleur_inactive
actif = False
texte = ''

finished = False
while not finished:
    for event in pygame.event.get():
        print(event)
        if event.type == pygame.QUIT:
            finished = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            if input_box.collidepoint(event.pos):
                actif = not actif
            else:
                actif = False
            couleur = couleur_active if actif else couleur_inactive
        if event.type == pygame.KEYDOWN:
            if actif:
                if event.key == pygame.K_RETURN:
                    print(texte)
                    texte = ''
                elif event.key == pygame.K_BACKSPACE:
                    texte = texte[:-1]
        if event.type == pygame.TEXTINPUT:
            if actif:
                texte += event.text

    screen.fill((30, 30, 30))
    surface_texte = police.render(texte, True, couleur)
    largeur = max(200, surface_texte.get_width()+10)
    input_box.w = largeur

    screen.blit(surface_texte, (input_box.x+5, input_box.y+5))
    pygame.draw.rect(screen, couleur, input_box, 2)

    pygame.display.flip()

pygame.quit()
sys.exit()
