import pygame
import utility.eventManager as eventManager
from utility.tools import getPath

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
        self.font = pygame.font.Font(getPath("assets/fonts/Papernotes.ttf"), fontSize)
        self.image = self.font.render(self.textInput, True, self.placeHolderColor)
        self.actif = False
        eventManager.addEventHandler(pygame.MOUSEBUTTONDOWN, self.onMouseButtonDown)
        eventManager.addEventHandler(pygame.KEYDOWN, self.onKeyDown)
        eventManager.addEventHandler(pygame.TEXTINPUT, self.onTextInput)
    
    def onMouseButtonDown(self, event) -> None:
        if self.rect.collidepoint(event.pos):
                self.actif = not self.actif
                if self.textInput == self.placeHolder and self.actif:
                    self.textInput = ""
        else:
            self.actif = False
            if self.textInput == "":
                self.textInput = self.placeHolder
        self.currentBorderColor = self.selectColor if self.actif else self.defaultBorderColor

    def onKeyDown(self, event) -> None:
            if self.actif and event.unicode != '\r':
                if event.key == pygame.K_RETURN:
                    self.textInput = ''
                elif event.key == pygame.K_BACKSPACE:
                    if self.textInput == self.placeHolder:
                        self.textInput = ""
                    self.textInput = self.textInput[:-1]

    def onTextInput(self, event) -> None:
        if self.actif:
            self.textInput += event.text

    def setPlaceholder(self, text) -> None:
        self.placeHolder = text
    
    def setText(self, text) -> None:
        self.textInput = text
        
    def update(self) -> None:
        self.image = pygame.Surface(self.rect.size)
        self.image.fill(self.backgroundColor)
        self.image.blit(self.font.render(self.textInput, True, self.textColor).convert_alpha(), (10,self.rect.h /2 - (self.fontSize/3)))
        pygame.draw.rect(self.image, self.currentBorderColor, (0,0,self.rect.w,self.rect.h), 2) # Affichage du rect

    def getText(self) -> str:
        return self.textInput