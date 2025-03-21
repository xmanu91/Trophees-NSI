import pygame
from utility.tools import getPath

class Text(pygame.sprite.Sprite):
    def __init__(
        self, 
        text: str, 
        fontSize: int,
        textCoordinates: tuple[float, float],
        color: pygame.Color,
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
            self.rect.center = (int(textCoordinates[0]), int(textCoordinates[1]))
        else : 
            self.rect.topleft = (int(textCoordinates[0]), int(textCoordinates[1]))

    def setText(self, text: str) -> None:
        self.text = text
        self.image = self.font.render(self.text, True, self.color)
            