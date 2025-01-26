from ui.Button import Button
from ui.Shape import Shape
from ui.Text import Text
import pygame

from scenes.PaintingSceneComponent.PickPalette import PickPalette
from scenes.PaintingSceneComponent.PresetPalette import PresetPalette

class ToolBar():
    def __init__(self, canva, spriteGroup, theme):
        self.canva = canva
        self.spriteGroup = spriteGroup
        self.theme = theme

        # Création de la barre d'outil
        self.background = Shape(pygame.Rect(0, 0, 200, 900), (144, 144, 255))
        self.spriteGroup.add(self.background)

        themeFontSize = int((16 / len(self.theme))*25) # Calc de la taille de la police en fonction de la longueur du theme
        themeXPos = (430 - themeFontSize * len(self.theme)) // 2 # Calc de la position x du theme
        self.theme = Text(self.theme, themeFontSize, (themeXPos, 0), (255,255,255), False)

        self.colorPreview = Shape(pygame.Rect(30, 245, 140, 25), (0, 0, 0))
        self.spriteGroup.add(self.theme, self.colorPreview)

        self.darknessPreview = Shape(pygame.Rect(30, 470, 140, 25), (0, 0, 0))
        self.spriteGroup.add(self.darknessPreview)

        self.presetPalette = PresetPalette(self.canva, self.spriteGroup, self.colorPreview, self.darknessPreview)
        self.pickPalette = PickPalette(self.canva, self.spriteGroup, self.colorPreview, self.darknessPreview)

        self.darknessIncreaseButton = Button(pygame.Rect(177, 475, 15, 15), lambda: (self.canva.changeDarkness(5), self.darknessPreview.changeColor(self.canva.getBrushColor())), None, None, None, "+", 14, (0, 0, 0), (4, -2), (255, 255, 255), (144, 144, 144))
        self.spriteGroup.add(self.darknessIncreaseButton)

        self.darknessDecreaseButton = Button(pygame.Rect(7, 475, 15, 15), lambda: (self.canva.changeDarkness(-5), self.darknessPreview.changeColor(self.canva.getBrushColor())), None, None, None, "-", 14, (0, 0, 0), (6, -2), (255, 255, 255), (144, 144, 144))
        self.spriteGroup.add(self.darknessDecreaseButton) 

        self.previousColor = self.canva.getBrushColor()         
            
    def update(self):
        self.pickPalette.update()

        # Dev tool
        mousePosition = pygame.mouse.get_pos()
        if pygame.mouse.get_pressed(5)[4]:
            print(mousePosition)