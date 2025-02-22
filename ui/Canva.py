from typing import Literal
from utility.tools import centerCoordinates
import utility.eventManager as eventManager
from collections import deque
import pygame
import os

class Canva(pygame.sprite.Sprite):
    def __init__(self,rect: pygame.Rect, backgroundColor: pygame.Color,drawColor: pygame.Color, username: str,  brushSize: int = 10):
        super().__init__()
        self.selectedColor: pygame.Color = drawColor # Couleur selectionné de base (sans darkness)
        self.drawColor: pygame.Color = drawColor # Couleur effective
        self.rect: pygame.Rect = rect
        self.image: pygame.Surface = pygame.Surface(self.rect.size)
        self.backgroundColor: pygame.Color = backgroundColor
        self.image.fill(self.backgroundColor)
        self.__previousPoint = None
        self.brushSize: int = brushSize
        self.allowDraw: bool = True
        self.darknessValue: int = 100
        self.username = username
        self.selectedTool = "brush"
        eventManager.addEventHandler(pygame.MOUSEWHEEL, self.onMouseWheel)

    def update(self):
        mousePositionX, mousePositionY = pygame.mouse.get_pos()
        mousePosition = (mousePositionX - self.rect.x, mousePositionY - self.rect.y) # Correction des coordonnes + centrage
        
        if self.allowDraw:
            if pygame.mouse.get_pressed(3)[0] and self.rect.collidepoint((mousePositionX, mousePositionY)):  
                match self.selectedTool:
                    case "brush":
                        self.setBrushColor(self.selectedColor)
                        self.__circleBrushSize = int((self.brushSize/2)-1)
                        if self.__previousPoint:
                            pygame.draw.circle(self.image, self.drawColor, self.__previousPoint, self.__circleBrushSize)
                            pygame.draw.line(self.image, self.drawColor, self.__previousPoint, mousePosition, self.brushSize)
                            pygame.draw.circle(self.image, self.drawColor, mousePosition, self.__circleBrushSize)
                            self.__previousPoint = mousePosition
                        else:
                            pygame.draw.circle(self.image, self.drawColor, mousePosition, self.__circleBrushSize)
                            self.__previousPoint = mousePosition
                    case "bucket":
                        self.holyBucket(mousePosition[0], mousePosition[1], self.drawColor, self.image)
                    case "eraser":
                        self.setBrushColor((255, 255, 255))
                        self.__circleBrushSize = int((self.brushSize/2)-1)
                        if self.__previousPoint:
                            pygame.draw.circle(self.image, self.drawColor, self.__previousPoint, self.__circleBrushSize)
                            pygame.draw.line(self.image, self.drawColor, self.__previousPoint, mousePosition, self.brushSize)
                            pygame.draw.circle(self.image, self.drawColor, mousePosition, self.__circleBrushSize)
                            self.__previousPoint = mousePosition
                        else:
                            pygame.draw.circle(self.image, self.drawColor, mousePosition, self.__circleBrushSize)
                            self.__previousPoint = mousePosition
                    case "colorpicker":
                        try:
                            color = self.image.get_at(mousePosition)
                            self.setBrushColor(color)
                            self.setSelectedColor(color)
                        except Exception as Error: # Dans le cas ou la souris n'est pas sur le canva
                            print(Error)

            else:
                self.__previousPoint = None

            if pygame.mouse.get_pressed(3)[2]:
                try:
                    self.holyBucket(mousePosition[0], mousePosition[1], self.drawColor, self.image)
                except Exception as Error:
                    print(Error)

        if pygame.mouse.get_pressed(3)[1]:
                try:
                    color = self.image.get_at((mousePosition[0], mousePosition[1]))
                    self.setBrushColor(color)
                    self.setSelectedColor(color)
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
    
    def setSelectedTool(self, tool: Literal["brush"] | Literal["bucket"] | Literal["colorpicker"] | Literal["eraser"]):
        self.selectedTool = tool

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

    def holyBucket(self, x, y, color, toile):
        baseColor = toile.get_at((x, y))
        if baseColor == color:
            return
        PAS = set() # C'est une liste, BEAUCOUP plus rapide
        pixels = deque() # Pareil mais c'est une file
        pixels.append((x, y))

        while pixels:
            x, y = pixels.popleft()
            if (x, y) in PAS:
                continue
            PAS.add((x, y))

            if 0<=x<self.rect.width and 0<=y<self.rect.height and toile.get_at((x, y)) == baseColor: 
                toile.set_at((x, y), color) 
                pixels.append((x+1, y))
                pixels.append((x-1, y))
                pixels.append((x, y+1))
                pixels.append((x, y-1))