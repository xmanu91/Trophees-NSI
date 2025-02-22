from ui import Image
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
        self.background = Image.Image("assets/brown paper.png", pygame.Rect(0, 0, 200, 900))
        self.spriteGroup.add(self.background)

        themeFontSize = int((16 / len(self.theme))*25) # Calc de la taille de la police en fonction de la longueur du theme
        themeXPos = (430 - themeFontSize * len(self.theme)) // 2 # Calc de la position x du theme
        self.theme = Text(self.theme, themeFontSize, (themeXPos, 0), (255,255,255), False)

        self.colorPreview = Shape(pygame.Rect(30, 245, 140, 25), (0, 0, 0))
        self.spriteGroup.add(self.theme, self.colorPreview)

        self.darknessPreview = DarknessPreview(pygame.Rect(30, 470, 140, 25))
        self.spriteGroup.add(self.darknessPreview)

        bucketIcon = Image.Image("assets/icons/seau.png", pygame.Rect(10,200, 30, 30))
        self.bucketTool = Button(bucketIcon.rect, lambda: self.changeTool('bucket'), bucketIcon.image, bucketIcon.image, bucketIcon.rect.topleft, "")
        self.spriteGroup.add(self.bucketTool)

        brushIcon = Image.Image("assets/icons/pinceau.png", pygame.Rect(50,200, 30, 30))
        self.brushTool = Button(brushIcon.rect, lambda: self.changeTool('brush'), brushIcon.image, brushIcon.image, brushIcon.rect.topleft, "")
        self.spriteGroup.add(self.brushTool)

        eraserIcon = Image.Image("assets/icons/gomme.png", pygame.Rect(100,200, 30, 30))
        self.eraserTool = Button(eraserIcon.rect, lambda: self.changeTool('eraser'), eraserIcon.image, eraserIcon.image, eraserIcon.rect.topleft, "")
        self.spriteGroup.add(self.eraserTool)

        colorPickerIcon = Image.Image("assets/icons/colorpicker.png", pygame.Rect(150,200, 30, 30))
        self.colorPickerTool = Button(colorPickerIcon.rect, lambda: self.changeTool('colorpicker') , colorPickerIcon.image, colorPickerIcon.image, colorPickerIcon.rect.topleft, "")
        self.spriteGroup.add(self.colorPickerTool)

        self.presetPalette = PresetPalette(self.canva, self.spriteGroup, self.colorPreview, self.darknessPreview) # Carrés
        self.pickPalette = PickPalette(self.canva, self.spriteGroup, self.colorPreview, self.darknessPreview) # Cercle

        self.darknessIncreaseButton = Button(pygame.Rect(177, 475, 15, 15), lambda: (self.canva.changeDarkness(-5), self.darknessPreview.changeColor(self.canva.getBrushColor()), self.colorPreview.changeColor(self.canva.getBrushColor())), None, None, None, "+", 14, (0, 0, 0), (4, 2), (255, 255, 255), (144, 144, 144))
        self.spriteGroup.add(self.darknessIncreaseButton)

        self.darknessDecreaseButton = Button(pygame.Rect(7, 475, 15, 15), lambda: (self.canva.changeDarkness(5), self.darknessPreview.changeColor(self.canva.getBrushColor()), self.colorPreview.changeColor(self.canva.getBrushColor())), None, None, None, "-", 14, (0, 0, 0), (6, 2), (255, 255, 255), (144, 144, 144))
        self.spriteGroup.add(self.darknessDecreaseButton) 

        self.previousColor = self.canva.getBrushColor()         
        
    def changeTool(self, tool: str):
        if tool == self.canva.selectedTool:
            return
        buttons = {"colorpicker": self.colorPickerTool, "brush": self.brushTool, "bucket": self.bucketTool, "eraser": self.eraserTool}
        for button in buttons:
            if button == tool:
                buttons[button].imageCoordinates = pygame.Rect(buttons[button].imageCoordinates.left - 5, buttons[button].imageCoordinates.top - 5, 40, 40)
                buttons[button].image = pygame.transform.scale(buttons[button].image, (40, 40))
                buttons[button].spriteImage = pygame.transform.scale(buttons[button].image, (40, 40))
                buttons[button].hoverImage = pygame.transform.scale(buttons[button].image, (40, 40))
            else:
                if button == self.canva.selectedTool:
                    buttons[button].imageCoordinates = pygame.Rect(buttons[button].imageCoordinates.left + 5, buttons[button].imageCoordinates.top + 5, 40, 40)
                buttons[button].image = pygame.transform.scale(buttons[button].image, (30, 30))
                buttons[button].spriteImage = pygame.transform.scale(buttons[button].image, (30, 30))
                buttons[button].hoverImage = pygame.transform.scale(buttons[button].image, (30, 30))
        self.canva.setSelectedTool(tool)

    def update(self):
        self.pickPalette.update()

        if self.canva.selectedColor != self.colorPreview.color:
            self.colorPreview.changeColor(self.canva.selectedColor)

        # Dev tool
        mousePosition = pygame.mouse.get_pos()
        if pygame.mouse.get_pressed(5)[4]:
            print(mousePosition)