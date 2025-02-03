from ui.Button import Button
from ui.Canva import Canva
from ui.Shape import Shape

from scenes.PaintingSceneComponent.DarknessPreview import DarknessPreview

import pygame

class PresetPalette():
    def __init__(self, canva: Canva, spriteGroup: pygame.sprite.Group, colorPreview: Shape, darknessPreview: DarknessPreview):
        self.canva = canva
        self.spriteGroup = spriteGroup
        self.colorPreview = colorPreview
        self.darknessPreview = darknessPreview
        
        listColor = [   [(224,0,0), (224,84,0), (255,255,60), (111,224,0), (26,238,0)], 
                        [(0,224,142), (0,173,224), (0,53,224), (116,0,224), (200,0,224)], 
                        [(0, 0, 0), (50, 50, 50), (100, 100, 100), (175, 175, 175), (255, 255, 255)]    ]

        listColorButton = []
        for liste in listColor:
            for color in liste:
                index = listColor.index(liste)
                newColorButton = Button(pygame.Rect(15+25*liste.index(color)+11*liste.index(color), 60+11*index+25*index, 25, 25), lambda selfColor=color: (self.canva.setBrushColor(selfColor), self.colorPreview.changeColor(selfColor), self.canva.setSelectedColor(selfColor), self.darknessPreview.changeColor(selfColor)), None, None, None, "", 14, (0, 0, 0), (7, 1), color, (144, 144, 144))
                listColorButton.append(newColorButton)
                self.spriteGroup.add(listColorButton[-1])
