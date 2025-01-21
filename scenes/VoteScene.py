from ui.Scene import Scene
from ui.Text import Text
from ui.Button import Button 
from ui.SceneManager import SceneManager
from ui.Image import Image
from ui.TextInput import TextInput
import pygame

class VoteScene(Scene):
    def __init__(self, sceneManager: SceneManager):
        super().__init__()
        screenWidth, screenHeight = sceneManager.surface.get_width(), sceneManager.surface.get_height()
        background = Image('assets/votebackground.png', pygame.Rect(0,0, screenWidth, screenHeight))
        
        drawing = Image("assets/temp/image1.png", pygame.Rect(40, 40, screenWidth - 80, screenHeight - 80))

        vote1 = Button(pygame.rect.Rect(40, 468, 75, 25), lambda: sendVote("Vote 1"), None, None, None, "Vote 1", defaultColor=(255,255,0),  hoverColor=(119,169,198),textColor=(0,0,0), fontSize= 25)
        vote2 = Button(pygame.rect.Rect(125, 468, 75, 25), lambda: sendVote("Vote 2"), None, None, None, "Vote 2", defaultColor=(255,255,0),  hoverColor=(119,169,198),textColor=(0,0,0), fontSize= 25)
        vote3 = Button(pygame.rect.Rect(210, 468, 75, 25), lambda: sendVote("Vote 3"), None, None, None, "Vote 3", defaultColor=(255,255,0),  hoverColor=(119,169,198),textColor=(0,0,0), fontSize= 25)
        vote4 = Button(pygame.rect.Rect(295, 468, 75, 25), lambda: sendVote("Vote 4"), None, None, None, "Vote 4", defaultColor=(255,255,0),  hoverColor=(119,169,198),textColor=(0,0,0), fontSize= 25)
        vote5 = Button(pygame.rect.Rect(380, 468, 75, 25), lambda: sendVote("Vote 5"), None, None, None, "Vote 5", defaultColor=(255,255,0),  hoverColor=(119,169,198),textColor=(0,0,0), fontSize= 25)
        vote6 = Button(pygame.rect.Rect(465, 468, 75, 25), lambda: sendVote("Vote 6"), None, None, None, "Vote 6", defaultColor=(255,255,0),  hoverColor=(119,169,198),textColor=(0,0,0), fontSize= 25)
        vote7 = Button(pygame.rect.Rect(550, 468, 75, 25), lambda: sendVote("Vote 7"), None, None, None, "Vote 7", defaultColor=(255,255,0),  hoverColor=(119,169,198),textColor=(0,0,0), fontSize= 25)
        vote8 = Button(pygame.rect.Rect(635, 468, 75, 25), lambda: sendVote("Vote 8"), None, None, None, "Vote 8", defaultColor=(255,255,0),  hoverColor=(119,169,198),textColor=(0,0,0), fontSize= 25)
        vote9 = Button(pygame.rect.Rect(720, 468, 75, 25), lambda: sendVote("Vote 9"), None, None, None, "Vote 9", defaultColor=(255,255,0),  hoverColor=(119,169,198),textColor=(0,0,0), fontSize= 25)
        vote10 = Button(pygame.rect.Rect(805, 468, 75, 25), lambda: sendVote("Vote 10"), None, None, None, "Vote 10", defaultColor=(255,255,0),  hoverColor=(119,169,198),textColor=(0,0,0), fontSize= 25)

        self.spriteGroup.add(background, drawing, vote1, vote2, vote3, vote4, vote5, vote6, vote7, vote8, vote9, vote10)

        def sendVote(note):
            print(note)