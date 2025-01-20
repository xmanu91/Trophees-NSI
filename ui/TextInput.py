import pygame

class TextInput(pygame.sprite.Sprite):
    def __init__(self, rect, defaultColor, selectColor, screenBgColor=(30, 30, 30)):
        super().__init__()
        self.rect = rect
        self.textInput = ""
        self.defaultColor = defaultColor
        self.selectColor = selectColor
        self.currentColor = defaultColor
        self.font = pygame.font.Font(None, 32)
        self.surfaceTextInput = self.font.render(self.textInput, True, self.defaultColor)
        self.actif = False
        self.screenBgColor = screenBgColor
    
    def update(self, screen, event):
        """
        /!\ InputText.update(screen, event) Doit etre appeler dans la boucle : 'for event in pygame.event.get()'
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.actif = not self.actif
            else:
                self.actif = False
            self.currentColor = self.selectColor if self.actif else self.defaultColor
        if event.type == pygame.KEYDOWN:
            if self.actif and event.unicode != '\r':
                if event.key == pygame.K_RETURN:
                    self.textInput = ''
                elif event.key == pygame.K_BACKSPACE:
                    self.textInput = self.textInput[:-1]
        if event.type == pygame.TEXTINPUT:
            if self.actif:
                self.textInput += event.text

        screen.fill(self.screenBgColor) # Permet d'agrandir le rect sans artéfacts (pixels de couleur indésirable)
        self.surfaceTextInput = self.font.render(self.textInput, True, self.currentColor) # Changement du texte
        self.rect.w = max(self.rect.w, self.surfaceTextInput.get_width()+10) # Agrandissement du rect

        screen.blit(self.surfaceTextInput, (self.rect.x+5, self.rect.y+5)) # Actualisation du texte
        pygame.draw.rect(screen, self.currentColor, self.rect, 2) # Affichage du rect
        pygame.display.flip()

    def getText(self):
        return self.textInput