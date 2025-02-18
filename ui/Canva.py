from utility.tools import centerCoordinates
import utility.eventManager as eventManager
import pygame
import os

class Canva(pygame.sprite.Sprite):
    def __init__(self,rect: pygame.Rect, backgroundColor: pygame.Color,drawColor: pygame.Color, username: str,  brushSize: int = 10):
        super().__init__()
        self.selectedColor: pygame.Color = drawColor
        self.drawColor: pygame.Color = drawColor
        self.rect: pygame.Rect = rect
        self.image: pygame.Surface = pygame.Surface(self.rect.size)
        self.backgroundColor: pygame.Color = backgroundColor
        self.image.fill(self.backgroundColor)
        self.__previousPoint = None
        self.brushSize: int = brushSize
        self.allowDraw: bool = True
        self.darknessValue: int = 100
        self.username = username
        eventManager.addEventHandler(pygame.MOUSEWHEEL, self.onMouseWheel)

    def update(self):
        mousePositionX, mousePositionY = pygame.mouse.get_pos()
        mousePosition = (mousePositionX - self.rect.x, mousePositionY - self.rect.y) # Correction des coordonnes + centrage
        
        if self.allowDraw:
            if pygame.mouse.get_pressed(3)[0] and self.rect.collidepoint((mousePositionX, mousePositionY)):  
                self.__circleBrushSize = int((self.brushSize/2)-1)
                if self.__previousPoint:
                    pygame.draw.circle(self.image, self.drawColor, self.__previousPoint, self.__circleBrushSize)
                    pygame.draw.line(self.image, self.drawColor, self.__previousPoint, mousePosition, self.brushSize)
                    pygame.draw.circle(self.image, self.drawColor, mousePosition, self.__circleBrushSize)
                    self.__previousPoint = mousePosition
                else:
                    pygame.draw.circle(self.image, self.drawColor, mousePosition, self.__circleBrushSize)
                    self.__previousPoint = mousePosition
            else:
                self.__previousPoint = None

        if pygame.mouse.get_pressed(3)[1]:
                try:
                    self.setBrushColor(self.image.get_at(mousePosition))
                except Exception as Error: # Dans le cas ou la souris n'est pas sur le canva
                    print(Error)

    def onMouseWheel(self, e):
        if e.y > 0:
            self.brushSize += 1
        else:
            if self.brushSize != 1:
                self.brushSize -= 1

    def setBrushSize(self, size: int):
        self.brushSize = size

    def setBrushColor(self, color: pygame.Color):
        self.drawColor = color

    def setSelectedColor(self, color: pygame.Color):
        self.selectedColor = color
        self.darknessValue = 100

    def getSelectedColor(self) -> pygame.Color:
        return self.selectedColor

    def changeDarkness(self, value: int):
        self.darknessValue += value
        if self.darknessValue < 0:
            self.darknessValue = 0
        elif self.darknessValue > 100:
            self.darknessValue = 100

        color = self.getSelectedColor()
        self.setBrushColor((color[0] * self.darknessValue//100, 
                            color[1] * self.darknessValue//100, 
                            color[2] * self.darknessValue//100))  

    def getBrushColor(self) -> pygame.Color:
        return self.drawColor
    
    def setBackgroundColor(self, color: pygame.Color):
        self.backgroundColor = color
        self.image.fill(color)

    def save(self, path: str):
        imagePath = os.path.join(path, self.username.strip() + "_drawing.png")
        pygame.image.save(self.image, imagePath)

    def load(self, path: str):
        self.image = pygame.image.load(path).convert_alpha()
        self.rect = self.image.get_rect()