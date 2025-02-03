from utility.tools import centerCoordinates
from ui.Image import Image
from ui.Canva import Canva
from scenes.PaintingSceneComponent.DarknessPreview import DarknessPreview
from ui.Shape import Shape
import pygame

class PickPalette():
    def __init__(self, canva: Canva, spriteGroup: pygame.sprite.Group, colorPreview: Shape, darknessPreview: DarknessPreview):
        self.canva = canva
        self.spriteGroup = spriteGroup
        self.colorPreview = colorPreview
        self.darknessPreview = darknessPreview

        self.colorPalette = Image("assets/colorPalette.png", pygame.Rect(10, 280, 180, 180))
        self.colorPaletteImage = self.colorPalette.image
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
                    self.canva.setSelectedColor(newColor)
                    self.colorPreview.changeColor(newColor)
                    self.darknessPreview.changeColor(newColor)
        else:   
            self.canva.allowDraw = True