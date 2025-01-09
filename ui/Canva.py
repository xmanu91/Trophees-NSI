import pygame

def centerCoordinates(coordinates, gap):
    return (coordinates[0]-gap, coordinates[1] - gap)

class Canva(pygame.sprite.Sprite):
    def __init__(self,x,y,width,height,backgroundColor,drawColor):
        super().__init__()
        self.drawColor=drawColor
        self.image = pygame.Surface((width, height))
        self.image.fill(backgroundColor)
        self.rect = self.image.get_rect()
        self.rect.x= x
        self.rect.y= y
        self.__previousPoint = None


    def update(self):
            # J'ai sorti mousePosition de la boucle pour pouvoir l'utiliser même si la souris n'a pas encore fait clique droit
            mousePosition = pygame.mouse.get_pos()

            # Permet de dessiner
            if pygame.mouse.get_pressed(3)[0]:
                if self.__previousPoint:
                    pygame.draw.circle(self.image, self.drawColor, centerCoordinates(self.__previousPoint, 5/2), 4.25)
                    pygame.draw.line(self.image, self.drawColor, centerCoordinates(self.__previousPoint, 5), centerCoordinates(mousePosition, 5), 10)
                    pygame.draw.circle(self.image, self.drawColor, centerCoordinates(mousePosition, (5/2)), 4.25)
                    self.__previousPoint = mousePosition
            else:
                self.__previousPoint = None