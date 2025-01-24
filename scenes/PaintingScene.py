from ui.Scene import Scene
from ui.Text import Text
from ui.Button import Button 
from ui.SceneManager import SceneManager
from ui.Image import Image
from ui.TextInput import TextInput
from ui.ProgressBar import ProgressBar
from ui.Canva import Canva
import pygame
import threading
from ui.Shape import Shape
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

        self.colorPreview = Shape(pygame.Rect(30, 290, 140, 25), (0, 0, 0))

        self.red = Shape(pygame.Rect(87.5-50, 360, 25, 100), (255, 0, 0))
        self.green = Shape(pygame.Rect(87.5, 360, 25, 100), (0, 255, 0))
        self.blue = Shape(pygame.Rect(87.5+50, 360, 25, 100), (0, 0, 255))

        self.buttonRedPlus = Button(pygame.Rect(87.5-50+2, 330, 21, 21), lambda: self.addPlusOneToColor("red"), None, None, None, "+", 14, (0,0,0), (7, 1), (255, 255, 255), (144, 144, 144))
        self.buttonRedMinus = Button(pygame.Rect(87.5-50+2, 470, 21, 21), lambda: self.decreaseOneToColor("red"), None, None, None, "-", 14, (0,0,0), (9, 0), (255, 255, 255), (144, 144, 144))
        self.buttonGreenPlus = Button(pygame.Rect(87.5+2, 330, 21, 21), lambda: self.addPlusOneToColor("green"), None, None, None, "+", 14, (0,0,0), (7, 1), (255, 255, 255), (144, 144, 144))
        self.buttonGreenMinus = Button(pygame.Rect(87.5+2, 470, 21, 21), lambda: self.decreaseOneToColor("green"), None, None, None, "-", 14, (0,0,0), (9, 0), (255, 255, 255), (144, 144, 144))
        self.buttonBluePlus = Button(pygame.Rect(87.5+50+2, 330, 21, 21), lambda: self.addPlusOneToColor("blue"), None, None, None, "+", 14, (0,0,0), (7, 1), (255, 255, 255), (144, 144, 144))
        self.buttonBlueMinus = Button(pygame.Rect(87.5+50+2, 470, 21, 21), lambda: self.decreaseOneToColor("blue"), None, None, None, "-", 14, (0,0,0), (9, 0), (255, 255, 255), (144, 144, 144))

        self.spriteGroup.add(self.red, self.green, self.blue, self.buttonRedPlus, self.buttonRedMinus, self.buttonGreenPlus, 
        self.buttonGreenMinus, self.buttonBluePlus, self.buttonBlueMinus, self.theme, self.colorPreview)

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

    def addPlusOneToColor(self, color: str):
        square = getattr(self, color)
        delta = 5
        if square.rect.height * 2.55 + delta < 255:
            square.changeRect(pygame.Rect(square.rect.x, square.rect.y - delta, square.rect.width, (square.rect.height + delta))) 
        else:
            square.changeRect(pygame.Rect(square.rect.x, 360, square.rect.width, 100))

        newColor = (int(self.red.rect.height * 2.55), int(self.green.rect.height * 2.55), int(self.blue.rect.height * 2.55))
        print(int(self.red.rect.height * 2.55), int(self.green.rect.height * 2.55), int(self.blue.rect.height * 2.55))
        self.canva.setBrushColor(newColor)
        self.colorPreview.changeColor(newColor)

    def decreaseOneToColor(self, color: str):
        square = getattr(self, color)
        delta = 5
        if square.rect.height * 2.55 - delta > 0:
            square.changeRect(pygame.Rect(square.rect.x, square.rect.y + delta, square.rect.width, square.rect.height - delta))
        

            newColor = (int(self.red.rect.height * 2.55), int(self.green.rect.height * 2.55), int(self.blue.rect.height * 2.55))
            print(int(self.red.rect.height * 2.55), int(self.green.rect.height * 2.55), int(self.blue.rect.height * 2.55))
            self.canva.setBrushColor(newColor)
            self.colorPreview.changeColor(newColor)
