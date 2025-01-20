import pygame

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
        self.brushSize = brushSize

    def update(self):
            # J'ai sorti mousePosition de la boucle pour pouvoir l'utiliser même si la souris n'a pas encore fait clique droit
            mousePosition = pygame.mouse.get_pos()

            # Permet de dessiner
            if pygame.mouse.get_pressed(3)[0]:
                if self.__previousPoint:
                    pygame.draw.circle(self.image, self.drawColor, centerCoordinates(self.__previousPoint, self.brushSize/2), 4.25)
                    pygame.draw.line(self.image, self.drawColor, centerCoordinates(self.__previousPoint, self.brushSize), centerCoordinates(mousePosition, self.brushSize), 10)
                    pygame.draw.circle(self.image, self.drawColor, centerCoordinates(mousePosition, self.brushSize/2), 4.25)
                    self.__previousPoint = mousePosition
                else:
                    pygame.draw.circle(self.image, self.drawColor, centerCoordinates(mousePosition, self.brushSize/2), 4.25)
                    self.__previousPoint = mousePosition
            else:
                self.__previousPoint = None # Possible outil

            if pygame.mouse.get_pressed(3)[1]:
                setBrushColor(self.image.get_at(mousePosition))



    def setBrushSize(self, size):
        self.brushSize = size

    def setBrushColor(self, color):
        self.drawColor = color
    
    def setBackgroundColor(self, color):
        self.backgroundColor = color
        self.image.fill(color)