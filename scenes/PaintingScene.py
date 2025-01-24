import utility.eventManager as eventManager
from ui.SceneManager import SceneManager
from ui.TextInput import TextInput
from ui.Button import Button
from ui.Scene import Scene
from ui.Image import Image
from ui.Shape import Shape
from ui.Canva import Canva
from ui.Text import Text
import threading
import pygame

import time

class PaintingScene(Scene):
    def __init__(self, sceneManager: SceneManager):
        super().__init__()
        screenWidth, screenHeight = sceneManager.surface.get_width(), sceneManager.surface.get_height()
        self.background = Image("assets/background_theme.png", pygame.Rect(0,0, screenWidth, screenHeight))
        self.startTimer()
        self.timerDuration = 1
        self.theme = "Le système solaire"
        self.textTheme = Text(self.theme, 32, (450, 250-16), (255,255,255), True)
        self.textTimer = Text(str(self.timerDuration), 32, (450, 250+16), (255,255,255), True)

        self.spriteGroup.add(self.background, self.textTimer, self.textTheme)

    def setCanva(self):
        self.canva = Canva(200, 0, 900-200, 500, (255, 255, 255), (0, 0, 0))
        self.spriteGroup.add(self.canva)

        # Création de la barre d'outil
        self.background = Shape(pygame.Rect(0, 0, 200, 900), (144, 144, 255))
        self.spriteGroup.add(self.background)

        themeFontSize = int((16 / len(self.theme))*25) # Calc de la taille de la police en fonction de la longueur du theme
        themeXPos = (430 - themeFontSize * len(self.theme)) // 2 # Calc de la position x du theme
        self.theme = Text(self.theme, themeFontSize, (themeXPos, 0), (255,255,255), False)

        listColor = [[(224,0,0), (224,84,0), (255,255,60), (111,224,0), (26,238,0)], [(0,224,142), (0,173,224), (0,53,224), (116,0,224), (200,0,224)], [(0, 0, 0), (50, 50, 50), (100, 100, 100), (175, 175, 175), (255, 255, 255)]]
        listColorButton = []
        for liste in listColor:
            print(liste)
            for color in liste:
                print(color)
                index = listColor.index(liste)
                newColorButton = Button(pygame.Rect(15+25*liste.index(color)+11*liste.index(color), 60+11*index+25*index, 25, 25), lambda selfColor=color: (self.canva.setBrushColor(selfColor), self.colorPreview.changeColor(selfColor)), None, None, None, "", 14, (0, 0, 0), (7, 1), color, (144, 144, 144))
                listColorButton.append(newColorButton)
                self.spriteGroup.add(listColorButton[-1])

        self.colorPreview = Shape(pygame.Rect(30, 250, 140, 25), (0, 0, 0))
    
        self.spriteGroup.add(self.theme, self.colorPreview)

        self.colorPalette = Image("assets/colorPalette.png", pygame.Rect(10, 310, 180, 180))
        self.colorPaletteImage = self.colorPalette.get_image()
        self.spriteGroup.add(self.colorPalette)

    def startTimer(self):
        threading.Thread(target=self.timer, daemon=True).start()

    def timer(self):
        print("Start timer")
        timer = 0
        while timer < self.timerDuration:
            time.sleep(1)
            timer += 1
            self.textTimer.setText(str(self.timerDuration - timer))
        print("End timer")
        self.setCanva()

    def centerCoordinates(self, coordinates, gap):
        return (coordinates[0]-gap, coordinates[1] - gap)

    def update(self):
        mousePositionX, mousePositionY = pygame.mouse.get_pos()
        mousePosition = (mousePositionX - 10, mousePositionY - 310)
        if not self.canva.rect.collidepoint(mousePosition):
            if pygame.mouse.get_pressed(3)[0]:
                    try:
                        print("Changing")
                        print(mousePosition)
                        newColor = self.colorPaletteImage.get_at(self.centerCoordinates(mousePosition, self.canva.brushSize))
                        self.canva.setBrushColor(newColor)
                        self.colorPreview.changeColor(newColor)
                        print("Changed")
                    except Exception as Error: # Dans le cas ou la souris n'est pas sur le canva
                        print(Error)
