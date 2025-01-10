import pygame

class Text(pygame.sprite.Sprite):
    def __init__(
        self, 
        text: str, 
        fontSize: int,
        textCoordinates: tuple[int, int],
        color: tuple[int, int, int],
        isCentered: bool = True,
        fontFamily: str = 'arial',
        ): 
        super().__init__()
        self.text = text
        self.fontSize = fontSize
        self.color = color
        self.font = pygame.font.Font(pygame.font.match_font('arial'), fontSize)  
        self.image = self.font.render(self.text, True, self.color)
        self.rect = self.image.get_rect()

        if isCentered :
            self.rect.center =  textCoordinates
        else : 
            self.rect.topleft = textCoordinates