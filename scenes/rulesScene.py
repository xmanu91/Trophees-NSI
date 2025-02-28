from utility.tools import getScalingFactors, getScalingFactorsX, getScalingFactorsY
from ui.SceneManager import SceneManager
import utility.consolLog as consolLog
from ui.Button import Button 
from ui.Scene import Scene
from ui.Image import Image
from ui.Text import Text
import pygame

class rulesScene(Scene):
    def __init__(self, sceneManager: SceneManager, roomManager, previousScene):
        super().__init__()
        self.sceneManager = sceneManager
        self.roomManager = roomManager
        self.previousScene = previousScene
        self.screenWidth, self.screenHeight = sceneManager.surface.get_width(), sceneManager.surface.get_height()
        self.spriteGroup = pygame.sprite.Group()
        self.background = Image("assets/backgrounds/paperBackground_1.png", pygame.Rect(0,0, self.screenWidth, self.screenHeight))
        
        self.text = Text("Comment jouer ?", 40, (self.screenWidth/2, self.screenHeight*0.1), (0,0,0), True)
        
        self.one = Text("1. Choisissez un pseudo", 20, getScalingFactors(135, 200, self.screenWidth, self.screenHeight), (0,0,0), True)
        self.two = Text("2. Créer/Rejoingner une room", 20, getScalingFactors(450, 250, self.screenWidth, self.screenHeight), (0,0,0), True)
        self.three = Text("3. Dessinez", 20, getScalingFactors(750, 220, self.screenWidth, self.screenHeight), (0,0,0), True)
        self.four = Text("4. Votez", 20, getScalingFactors(230, 450, self.screenWidth, self.screenHeight), (0,0,0), True)
        self.five = Text("5. Gagner !", 20, getScalingFactors(560, 460, self.screenWidth, self.screenHeight), (0,0,0), True)

        self.image1 = Image("assets/images/help1.png", pygame.Rect(getScalingFactorsX(20, self.screenWidth), getScalingFactorsY(75, self.screenHeight), 250*1.2, 90*1.2))
        self.image2 = Image("assets/images/help2.png", pygame.Rect(getScalingFactorsX(340, self.screenWidth), getScalingFactorsY(100, self.screenHeight), 200*1.2, 110*1.2))
        self.image3 = Image("assets/images/help3.png", pygame.Rect(getScalingFactorsX(610, self.screenWidth), getScalingFactorsY(50, self.screenHeight), 210*1.2, 130*1.2))
        self.image4 = Image("assets/images/help4.png", pygame.Rect(getScalingFactorsX(120, self.screenWidth), getScalingFactorsY(260, self.screenHeight), 200*1.1, 160*1.1))
        self.image5 = Image("assets/images/help5.png", pygame.Rect(getScalingFactorsX(420, self.screenWidth), getScalingFactorsY(275, self.screenHeight), 230*1.2, 140*1.2))
        
        self.backButton = Button(pygame.Rect(self.screenWidth*0.975 - 100, self.screenHeight*0.95-30, 100, 30), self.back, None, None, None, "Retour", 25, (0,0,0), defaultColor=(255,255,255),  hoverColor=(119,169,198))        
        self.spriteGroup.add(self.background, self.text, self.one, self.two, self.three, self.four, self.five, self.backButton, self.image1, self.image2, self.image3, self.image4, self.image5)

    def back(self):
        self.sceneManager.setAsCurrentScene(self.previousScene)

    def update(self):
        if pygame.mouse.get_pressed(5)[4]:
            if self.previousState == False:
                consolLog.warn(pygame.mouse.get_pos())
            self.previousState = True
        else:
            self.previousState = False