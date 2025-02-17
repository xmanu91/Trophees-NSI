import pygame
import utility.eventManager as eventManager

class TextInput(pygame.sprite.Sprite):
    def __init__(self, rect: pygame.Rect, borderColor: pygame.Color, selectColor: pygame.Color, textColor: pygame.Color, backgroundColor: pygame.Color, placeholder: str="", fontSize: int=32):
        super().__init__()
        self.rect = rect
        self.textInput = placeholder
        self.placeHolder = placeholder
        self.defaultBorderColor = borderColor
        self.currentBorderColor = borderColor
        self.selectColor = selectColor
        self.backgroundColor = backgroundColor
        self.textColor = textColor
        self.placeHolderColor = (50, 50, 50)
        self.fontSize = fontSize
        self.font = pygame.font.Font(None, fontSize)
        self.image = self.font.render(self.textInput, True, self.placeHolderColor)
        self.actif = False
        eventManager.addEventHandler(pygame.MOUSEBUTTONDOWN, self.onMouseButtonDown)
        eventManager.addEventHandler(pygame.KEYDOWN, self.onKeyDown)
        eventManager.addEventHandler(pygame.TEXTINPUT, self.onTextInput)
    
    def onMouseButtonDown(self, e):
        if self.rect.collidepoint(e.pos):
                self.actif = not self.actif
                if self.textInput == self.placeHolder and self.actif:
                    self.textInput = ""
        else:
            self.actif = False
            if self.textInput == "":
                self.textInput = self.placeHolder
        self.currentBorderColor = self.selectColor if self.actif else self.defaultBorderColor

    def onKeyDown(self, e):
            if self.actif and e.unicode != '\r':
                if e.key == pygame.K_RETURN:
                    self.textInput = ''
                elif e.key == pygame.K_BACKSPACE:
                    if self.textInput == self.placeHolder:
                        self.textInput = ""
                    self.textInput = self.textInput[:-1]
                    if self.textInput == "":
                        self.textInput = self.placeHolder

    def onTextInput(self, e):
        if self.actif:
            self.textInput += e.text

    def update(self):
        self.image = pygame.Surface(self.rect.size)
        self.image.fill(self.backgroundColor)
        self.image.blit(self.font.render(self.textInput, True, self.textColor).convert_alpha(), (10,self.rect.h /2 - (self.fontSize/3)))
        pygame.draw.rect(self.image, self.currentBorderColor, (0,0,self.rect.w,self.rect.h), 2) # Affichage du rect

    def getText(self):
        return self.textInput