from ui.Image import Image
from ui.Button import Button
from ui.Shape import Shape
from ui.Text import Text
from ui.Canva import Canva
import pygame
from utility.tools import removeAlpha

from scenes.PaintingSceneComponent.PickPalette import PickPalette
from scenes.PaintingSceneComponent.PresetPalette import PresetPalette
from scenes.PaintingSceneComponent.DarknessPreview import DarknessPreview

class ToolBar():
    def __init__(self, canva: Canva, spriteGroup: pygame.sprite.Group, theme: str):
        self.canva = canva
        self.spriteGroup = spriteGroup
        self.theme = theme

        # Création de la barre d'outil
        self.background = Image("assets/brown paper.png", pygame.Rect(0, 0, 200, 900))
        self.spriteGroup.add(self.background)

        postIt = Image("assets/post-it.png", pygame.Rect(5, 15, 391*0.5, 124*0.5))

        eraserSprite = Image("assets/gomme.png", pygame.Rect(0, 0, 155, 50))
        self.eraser = Button(pygame.Rect(-50, 91, 155, 50), lambda: self.changeTool('eraser'), eraserSprite.image, eraserSprite.image, (-44, 91), "")

        brushSprite = Image("assets/pinceau.png", pygame.Rect(0, 0, 225, 25))
        self.brush = Button(pygame.Rect(-50, 172, 225, 25), lambda: self.changeTool('brush'), brushSprite.image, brushSprite.image, (-44, 172), "")

        colorPickerSprite = Image("assets/pipette.png", pygame.Rect(0, 0, 250, 98))
        self.colorPicker = Button(pygame.Rect(-50, 197, 250, 98), lambda: self.changeTool('colorpicker'), colorPickerSprite.image, colorPickerSprite.image, (-44, 197), "")

        bucketSprite = Image("assets/seau.png", pygame.Rect(0, 0, 225, 225))
        self.bucket = Button(pygame.Rect(-11, 426, 225, 225), lambda: self.changeTool('bucket'), bucketSprite.image, bucketSprite.image, (-11, 426), "")

        self.pickPalette = PickPalette(self.canva, self.spriteGroup)

        self.theme = Text(self.theme, 16, (2 + 391*0.5/2, 10+ 124*0.5 /2), (0 ,0, 0), True)

        self.previousColor = self.canva.getBrushColor()  

        self.spriteGroup.add(postIt, self.theme, self.eraser, self.brush, self.colorPicker, self.bucket)       
        
    def changeTool(self, tool: str):
        if tool == self.canva.selectedTool:
            return
        buttons = {"eraser": self.eraser, "brush": self.brush, "colorpicker": self.colorPicker, "bucket": self.bucket}
        for button in buttons:
            if button == tool:
                if button == "bucket":
                    buttons[button].imageCoordinates.y = 400
                else:
                    buttons[button].imageCoordinates.x = -30
            else:    
                if button == "bucket":
                    buttons[button].imageCoordinates.y = 426
                else:
                    buttons[button].imageCoordinates.x = -50
            
        self.canva.setSelectedTool(tool)

    def update(self):
        self.pickPalette.update()
        # Dev tool
        mousePosition = pygame.mouse.get_pos()
        if pygame.mouse.get_pressed(5)[4]:
            print(mousePosition)