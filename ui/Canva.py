import pygame
from scenes import PaintingScene
import utility.eventManager as eventManager
from utility.tools import centerCoordinates

class Canva(pygame.sprite.Sprite):
    def __init__(self,x,y,width,height,backgroundColor,drawColor,brushSize = 5):
        super().__init__()
        self.selectedColor = drawColor
        self.drawColor = drawColor
        self.image = pygame.Surface((width, height))
        self.backgroundColor = backgroundColor
        self.image.fill(self.backgroundColor)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.__previousPoint = None
        self.brushSize = brushSize
        self.allowDraw = True
        self.darknessValue = 100
        eventManager.addEventHandler(pygame.MOUSEWHEEL, self.onMouseWheel)

    def update(self):
        mousePositionX, mousePositionY = pygame.mouse.get_pos()
        mousePosition = (mousePositionX - self.rect.x + self.brushSize, mousePositionY - self.rect.y + self.brushSize) # Correction des coordonnes + centrage

        if self.allowDraw and self.rect.collidepoint((mousePositionX, mousePositionY)):
            if pygame.mouse.get_pressed(3)[0]:
                if self.__previousPoint:
                    pygame.draw.circle(self.image, self.drawColor, centerCoordinates(self.__previousPoint, self.brushSize), self.brushSize)
                    pygame.draw.line(self.image, self.drawColor, centerCoordinates(self.__previousPoint, self.brushSize), centerCoordinates(mousePosition, self.brushSize), self.brushSize*2)
                    pygame.draw.circle(self.image, self.drawColor, centerCoordinates(mousePosition, self.brushSize), self.brushSize)
                    self.__previousPoint = mousePosition
                else:
                    pygame.draw.circle(self.image, self.drawColor, centerCoordinates(mousePosition, self.brushSize), self.brushSize)
                    self.__previousPoint = mousePosition
            else:
                self.__previousPoint = None

        if pygame.mouse.get_pressed(3)[1]:
                try:
                    self.setBrushColor(self.image.get_at(centerCoordinates(mousePosition, self.brushSize)))
                except Exception as Error: # Dans le cas ou la souris n'est pas sur le canva
                    print(Error)

    def onMouseWheel(self, e):
        if e.y > 0:
            self.brushSize += 1
        else:
            if self.brushSize != 1:
                self.brushSize -= 1

    def setBrushSize(self, size):
        self.brushSize = size

    def setBrushColor(self, color):
        self.drawColor = color

    def setSelectedColor(self, color):
        self.selectedColor = color
        self.gradientDarkness = [(0, 0, 0)]
        self.darknessValue = 100
        for gradient in range(1, 20):
            self.gradientDarkness.append((color[0] * gradient // 20, color[1] * gradient // 20, color[2] * gradient // 20))

    def changeDarkness(self, value):
        self.darknessValue += value
        if self.darknessValue < 0:
            self.darknessValue = 0
        elif self.darknessValue > 100:
            self.darknessValue = 100

        index = (self.darknessValue//5)-1
        if index < 0: index = 0
        self.setBrushColor(self.gradientDarkness[index])  

    def getBrushColor(self):
        return self.drawColor
    
    def setBackgroundColor(self, color):
        self.backgroundColor = color
        self.image.fill(color)

    def save(self):
        pygame.image.save(self.image, "canva.png") # Pensez a changer le chemin et le nom   

    def load(self, path):
        self.image = pygame.image.load(path).convert_alpha()
        self.rect = self.image.get_rect()