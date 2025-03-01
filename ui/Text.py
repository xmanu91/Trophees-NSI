import pygame
from utility.tools import getPath

class Text(pygame.sprite.Sprite):
    def __init__(
        self, 
        text: str, 
        fontSize: int,
        textCoordinates: tuple[int, int],
        color: tuple[int, int, int],
        isCentered: bool = True,
        fontFamily: str | None = None,
        ): 
        super().__init__()
        self.text = text
        self.fontSize = fontSize
        self.color = color
        
        if fontFamily != None:
            self.font = pygame.font.Font(getPath(f"assets/fonts/{fontFamily}"), fontSize)  
        else:
            self.font = pygame.font.Font(getPath(f"assets/fonts/Papernotes.ttf"), fontSize)  

        self.image = self.font.render(self.text, True, self.color)
        self.rect = self.image.get_rect()

        if isCentered :
            self.rect.center =  textCoordinates
        else : 
            self.rect.topleft = textCoordinates

    def setText(self, text: str):
        self.text = text
        self.image = self.font.render(self.text, True, self.color)
            