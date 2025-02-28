from typing import Callable
import pygame
from utility.tools import getPath
from ui.SceneManager import SceneManager

class Button(pygame.sprite.Sprite):

    sceneManager = None

    def __init__(
            self, 
            buttonRect: pygame.rect.RectType, 
            action: Callable, 
            image: pygame.Surface | None, 
            hoverImage: pygame.Surface | None, 
            imageCoordinates: tuple[int, int] | None, 
            text: str, 
            fontSize: int = 14,
            textColor: pygame.Color = (0,0,0),
            textCoordinates: tuple[int, int] | None = None, 
            defaultColor: pygame.Color | None = None, 
            hoverColor: pygame.Color | None = None, 
            ErrorButton: bool = False
            ): 
        super().__init__()
        self.defaultColor = defaultColor  
        self.hoverColor = hoverColor  
        self.rect = buttonRect
        self.action = action
        self.ErrorButton = ErrorButton

        # Surface definition
        if image!= None:
            self.spriteImage = pygame.transform.scale(image, buttonRect.size).convert_alpha()
            self.hoverImage = pygame.transform.scale(hoverImage, buttonRect.size).convert_alpha()
            self.image = pygame.transform.scale(image, buttonRect.size).convert_alpha()
            self.imageCoordinates = pygame.Rect(imageCoordinates, self.image.get_size())
        else:
            self.image = pygame.Surface(buttonRect.size) 
        
        self.rect = buttonRect  

        #Button text
        self.font = pygame.font.Font(getPath("assets/fonts/Papernotes.ttf"), fontSize)
        self.surface_text = self.font.render(text, True, textColor)
        self.textCoordinates= textCoordinates or (self.rect.width/2 - self.surface_text.get_width() / 2, self.rect.height/2 - self.surface_text.get_height() / 2)
        
        self.isUsable = False
        self.disabled = False
        self.previousState = False

        if self.ErrorButton:
            group = self.sceneManager.getSpriteGroup()
            for sprite in group:
                if type(sprite) == type(self):
                    sprite.disabled = True

    def kill(self):
        group = self.sceneManager.getSpriteGroup()
        for sprite in group:
            if type(sprite) == type(self):
                sprite.disabled = False
        super().kill()

    def update(self):
        mousePosition = pygame.mouse.get_pos()
        isMousePressed = pygame.mouse.get_pressed()[0]

        #Hover
        if self.rect.collidepoint(mousePosition) and self.previousState == False and self.isUsable == True and self.disabled == False: 
            if self.hoverColor:
                self.image.fill(self.hoverColor)
            elif self.hoverImage:
                self.image = self.hoverImage
                self.rect = self.imageCoordinates
            
            if isMousePressed:
                if self.action:
                    self.action()

        else: 
            if self.defaultColor:
                self.image.fill(self.defaultColor)
            else:
                self.image = self.spriteImage
                self.rect = self.imageCoordinates

        if self.previousState == False:
            self.isUsable = True
        else:
            self.isUsable = False

        self.previousState = isMousePressed
        self.image.blit(self.surface_text, self.textCoordinates)

