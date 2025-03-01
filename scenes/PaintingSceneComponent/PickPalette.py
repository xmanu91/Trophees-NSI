import pygame

from ui.Circle import Circle
from ui.Image import Image
from ui.Canva import Canva
from ui.Shape import Shape

class PickPalette():
    def __init__(self, canva: Canva, spriteGroup: pygame.sprite.Group):
        self.canva = canva
        self.spriteGroup = spriteGroup

        self.colorPalette = Image("assets/images/palette.png", pygame.Rect(5, 290, 378*0.5, 261*0.5))
        self.colorPaletteImage = self.colorPalette.image

        self.colorShapes = {"blue": Shape(pygame.Rect(42, 317, 41, 39), (0,0,0,0)),
                            "green": Shape(pygame.Rect(42, 365, 41, 39), (0,0,0,0)),
                            "red": Shape(pygame.Rect(90, 365, 41, 39), (0,0,0,0)),
                            "black": Shape(pygame.Rect(89, 317, 41, 39), (0,0,0,0)),
                            "white": Shape(pygame.Rect(138, 317, 41, 39), (0,0,0,0))}
        
        self.mix = Circle(pygame.Rect(138, 364, 42, 42), self.canva.getBrushColor())
        self.colors = {"blue": (0,0,40), "red": (40,0,0), "green": (0, 40, 0), "black": (-20, -20, -20), "white": (20,20,20)}
        self.spriteGroup.add(self.colorPalette, self.colorShapes['blue'], self.colorShapes['red'], self.colorShapes['green'], self.colorShapes['black'], self.colorShapes['white'], self.mix)

        self.clicked = False
    
    def multiply(self, matrix_a,matrix_b):
        print(matrix_a, matrix_b)
        result = [0 for _ in matrix_a]

        # Perform matrix multiplication
        for i in range(len(matrix_a)):
            result[i] = max(0, min(matrix_a[i]+matrix_b[i], 255))

        return result

    def update(self):
        self.mix.changeColor(self.canva.getBrushColor())

        mousePositionX, mousePositionY = pygame.mouse.get_pos()
        mousePosition = (mousePositionX, mousePositionY)
        if not self.canva.rect.collidepoint(mousePosition):
            self.canva.allowDraw = False
            for color in self.colorShapes:
                if self.colorShapes[color].rect.collidepoint(mousePosition):
                    if pygame.mouse.get_pressed(3)[0] and (self.canva.selectedTool=="brush" or self.canva.selectedTool=="bucket"):
                        if self.clicked==False:
                            self.clicked = True
                            actualColor = [float(_) for _ in self.canva.getBrushColor()]
                            if (actualColor == [0.0, 0.0, 0.0] or actualColor == [255.0, 255.0, 255.0]) and color!="white" and color!="black":
                                newColor = [abs(_) for _ in self.colors[color]]
                            else:
                                newColor = self.multiply(actualColor, self.colors[color])
                            self.canva.setBrushColor(newColor)
                            self.canva.setSelectedColor(newColor)
                    else:
                        self.clicked = False
        else:   
            self.canva.allowDraw = True