import pygame
import utility.eventManager as eventManager

def centerCoordinates(coordinates, gap):
    return (coordinates[0]-gap, coordinates[1] - gap)

class Canva(pygame.sprite.Sprite):
    def __init__(self,x,y,width,height,backgroundColor,drawColor,brushSize = 5):
        super().__init__()
        self.drawColor = drawColor
        self.image = pygame.Surface((width, height))
        self.backgroundColor = backgroundColor
        self.image.fill(self.backgroundColor)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.__previousPoint = None
        self.brushSize = 5
        self.allowDraw = True
        eventManager.addEventHandler(pygame.KEYDOWN, self.onKeyDown)
        eventManager.addEventHandler(pygame.MOUSEWHEEL, self.onMouseWheel)

    def update(self):
        mousePosition = pygame.mouse.get_pos()

        if self.allowDraw:
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
            self.setBrushColor(self.image.get_at(mousePosition))

    def onMouseWheel(self, e):
        if e.y > 0:
            self.brushSize += 1
        else:
            if self.brushSize != 1:
                self.brushSize -= 1

    def onKeyDown(self, e):
        if e.key == pygame.K_s:
            self.save()
        if e.key == pygame.K_k:
            self.load("canva.png")
        if e.key == pygame.K_r:
            self.allowDraw = not self.allowDraw

    def setBrushSize(self, size):
        self.brushSize = size

    def setBrushColor(self, color):
        self.drawColor = color
    
    def setBackgroundColor(self, color):
        self.backgroundColor = color
        self.image.fill(color)

    def save(self):
        pygame.image.save(self.image, "canva.png")    

    def load(self, path):
        self.image = pygame.image.load(path).convert_alpha()
        self.rect = self.image.get_rect()