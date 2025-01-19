import pygame
import sys

class TextInput(pygame.sprite.Sprite):
    def __init__(self, rect, text, defaultColor, selectColor):
        super().__init__()
        self.rect = rect
        self.text = text
        self.defaultColor = defaultColor
        self.selectColor = selectColor
        self.currentColor = defaultColor
        self.font = pygame.font.Font(None, 32)
        self.surface_text = self.font.render(self.text, True, self.defaultColor)
    
    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.rect.collidepoint(event.pos):
                    actif = not actif
                else:
                    actif = False
                self.currentColor = self.selectColor if actif else self.defaultColor
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