import pygame

from ui.Shape import Shape
from ui.Text import Text
from ui.Button import Button

import utility.consolLog as consolLog
errorEventType = pygame.event.custom_type()

def raiseAnError(error, action=None):
    pygame.event.post(pygame.event.Event(errorEventType, error=error, action=action))
    consolLog.warn(error)

class ErrorHandlerUi:
    def __init__(self):
        self.spriteGroup = pygame.sprite.Group()  

    def raiseError(self, e):
        self.spriteGroup.add(Shape(pygame.Rect(0,0, pygame.display.get_window_size()[0],  pygame.display.get_window_size()[1]), (0,0,0, int(255*0.40))))
        if e.action == None:
            self.errorWindow = ErrorWindow(e.error, self.closeError)
            self.spriteGroup.add(self.errorWindow)
        else:
            self.errorWindow = ErrorWindow(e.error, lambda: (self.closeError(), e.action()))
            self.spriteGroup.add(self.errorWindow)
    
    def closeError(self):
        self.spriteGroup.empty()
        self.errorWindow.kill()
        

class ErrorWindow(pygame.sprite.Sprite):
    def __init__(self, error, action):
        super().__init__()
        self.rect = pygame.Rect(pygame.display.get_window_size()[0]/2, pygame.display.get_window_size()[1]/2, 300, 150)
        self.errorText = Text(error, 16, (0, 25), (255,255,255), True)
        self.rect.width = self.errorText.rect.w + 50 
        self.image = pygame.Surface(self.rect.size)
        self.image.fill((255,0,0))

        self.rect.x = pygame.display.get_window_size()[0]/2 - self.rect.w/2
        self.rect.y = pygame.display.get_window_size()[1]/2 - self.rect.h/2
        
        self.errorText.rect.centerx = self.rect.width/2
        self.button = Button(pygame.Rect(self.rect.centerx - 50, self.rect.bottom - 75, 100, 50), action, None, None, None, "D'accord", defaultColor=(255,255,255),  hoverColor=(119,169,198), textColor=(0,0,0), ErrorButton=True)

        self.image.blit(self.errorText.image, self.errorText.rect)

    def update(self):
        self.button.update()
        self.image.blit(self.button.image, (self.rect.width/2 - 50, self.rect.height - 75, 100, 50))

    def kill(self):
        self.button.kill()
