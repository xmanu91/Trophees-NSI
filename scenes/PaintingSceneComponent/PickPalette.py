from utility.tools import centerCoordinates
from ui.Image import Image
import pygame

class PickPalette():
    def __init__(self, canva, spriteGroup, colorPreview):
        self.canva = canva
        self.spriteGroup = spriteGroup
        self.colorPreview = colorPreview

        self.colorPalette = Image("assets/colorPalette.png", pygame.Rect(10, 280, 180, 180))
        self.colorPaletteImage = self.colorPalette.get_image()
        self.spriteGroup.add(self.colorPalette)
    
    def update(self):
        mousePositionX, mousePositionY = pygame.mouse.get_pos()
        mousePosition = (mousePositionX, mousePositionY)
        if not self.canva.rect.collidepoint(mousePosition):
            self.canva.allowDraw = False
            if self.colorPalette.rect.collidepoint(mousePosition):
                mousePosition = (mousePositionX - self.colorPalette.rect.x + self.canva.brushSize, mousePositionY - self.colorPalette.rect.y + self.canva.brushSize)
                if pygame.mouse.get_pressed(3)[0]:
                    newColor = self.colorPaletteImage.get_at(centerCoordinates(mousePosition, self.canva.brushSize))
                    self.canva.setBrushColor(newColor)
                    self.colorPreview.changeColor(newColor)
        else:   
            self.canva.allowDraw = True