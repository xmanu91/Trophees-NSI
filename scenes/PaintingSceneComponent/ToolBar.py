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

        self.colorPreview = Shape(pygame.Rect(30, 250, 140, 25), (0, 0, 0))
        self.spriteGroup.add(self.theme, self.colorPreview)

        self.presetPalette = PresetPalette(self.canva, self.spriteGroup, self.colorPreview)

        self.pickPalette = PickPalette(self.canva, self.spriteGroup, self.colorPreview)

        self.darkness = Shape(pygame.Rect(30, 470, 140, 25), (0, 0, 0))
        self.darknessValue = 100
        self.darkness.changeColor((abs(self.darknessValue-100), abs(self.darknessValue-100), abs(self.darknessValue-100)))
        self.spriteGroup.add(self.darkness)

        self.darknessIncreaseButton = Button(pygame.Rect(180, 470, 15, 15), lambda: self.changeDarkness(5), None, None, None, "+", 14, (0, 0, 0), (7, 1), (255, 255, 255), (144, 144, 144))
        self.spriteGroup.add(self.darknessIncreaseButton)

        self.darknessDecreaseButton = Button(pygame.Rect(5, 470, 15, 15), lambda: self.changeDarkness(-5), None, None, None, "-", 14, (0, 0, 0), (7, 1), (144, 144, 144), (144, 144, 144))
        self.spriteGroup.add(self.darknessDecreaseButton)        

    def changeDarkness(self, value):
        self.darknessValue += value
        if self.darknessValue < 0:
            self.darknessValue = 0
        elif self.darknessValue > 100:
            self.darknessValue = 100

    def update(self):
        self.pickPalette.update()

        # Dev tool
        if pygame.mouse.get_pressed(5)[4]:
            print(mousePosition)