from typing import Callable
import pygame

class Button(pygame.sprite.Sprite): 
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
            ):
        super().__init__()
        self.defaultColor = defaultColor  
        self.hoverColor = hoverColor  
        self.rect = buttonRect
        self.action = action

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
        self.font = pygame.font.Font(pygame.font.match_font('arial'), fontSize)
        self.surface_text = self.font.render(text, True, textColor)
        self.textCoordinates= textCoordinates or (self.rect.width/2 - self.surface_text.get_width() / 2, self.rect.height/2 - self.surface_text.get_height() / 2)
        
        self.actionned = False

    def update(self): 
        mousePosition = pygame.mouse.get_pos()
        isMousePressed = pygame.mouse.get_pressed()[0]

        #Hover
        if self.rect.collidepoint(mousePosition): 
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            if self.hoverColor:
                self.image.fill(self.hoverColor)
            elif self.hoverImage:
                self.image = self.hoverImage

            if isMousePressed:  
                if self.action and self.actionned!=True:
                    self.actionned = True
                    self.action()
            else:
                self.actionned = False
        else: 
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
            if self.defaultColor:
                self.image.fill(self.defaultColor)
            else:
                self.image = self.spriteImage
        
        self.image.blit(self.surface_text, self.textCoordinates)
