import pygame
import os

from ui.SceneManager import SceneManager
from ui.ProgressBar import ProgressBar
from ui.Button import Button 
from ui.Image import Image
from ui.Scene import Scene
from ui.Text import Text

from utility.gameInitialisation import sqlProvider
from utility.VotesManager import VotesManager
from utility.RoomManager import RoomManager
from utility.GameManager import GameManager
from utility import consolLog

from scenes.WinnerScene import WinnerScene
from time import sleep
import tempfile

class VoteScene(Scene):
    def __init__(self, sceneManager: SceneManager, roomManager: RoomManager, gameManager: GameManager):
        super().__init__()
        self.gameManager = gameManager
        self.tempdir = self.gameManager.getTempDir()
        self.sceneManager = sceneManager
        self.roomManager = roomManager
        self.votesManager = VotesManager(sqlProvider, roomManager.currentRoomID, roomManager.username, self.tempdir, self.roomManager)
        self.drawnList = []
        self.index = 0

        while len(self.drawnList) != self.roomManager.getConnectedUsersNumberInRoom(self.roomManager.currentRoomID)-1:
            sleep(0.5)
            pygame.mouse.set_cursor((pygame.SYSTEM_CURSOR_WAITARROW))
            self.votesManager.getDrawings()
            self.drawnList = []

            for drawn in os.listdir(self.tempdir.name):
                self.drawnList.append(drawn)

            consolLog.info(self.drawnList)

        pygame.mouse.set_cursor((pygame.SYSTEM_CURSOR_ARROW))
        consolLog.info("Tous les dessins sont recupérés.")

        self.screenWidth, self.screenHeight = sceneManager.surface.get_width(), sceneManager.surface.get_height()
        self.background = Image('assets/backgrounds/wallBackground_3.png', pygame.Rect(0, 0, self.screenWidth, self.screenHeight))
        
        self.drawRect = pygame.Rect(self.screenWidth /2 - self.screenWidth*0.35, 40, self.screenWidth*0.7, self.screenHeight*0.7)
        self.drawing = Image(os.path.join(self.tempdir.name, self.drawnList[self.index]), self.drawRect)

        self.note = 1

        # Création des boutons avec une boucle
        self.vote_buttons = []
        for i in range(1, 11):  # De 1 à 10
            button = Button(
                pygame.rect.Rect((self.screenWidth / 11 * i) - 20, 440, 40, 40),  # Position et taille
                lambda note=i: self.setNote(note),  # Fonction de rappel avec la note
                None, None, None,  # Autres paramètres inutilisés
                str(i),  # Texte du bouton
                defaultColor=(255, 255, 255),  # Couleur par défaut
                hoverColor=(119, 169, 198),  # Couleur au survol
                textColor=(0, 0, 0),  # Couleur du texte
                fontSize=25  # Taille de la police
            )
            self.vote_buttons.append(button)  # Ajouter le bouton à la liste

        durationPerVote = 5
        self.progressBar = ProgressBar(pygame.Rect(0, 0, 900, 10), (0,255,0), durationPerVote, lambda: self.nextDrawing(self.note))
        self.progressBar.run_start()

        # Ajout des éléments au groupe de sprites
        self.spriteGroup.add(self.background, self.drawing, self.progressBar, *self.vote_buttons)

    def setNote(self, note: int):
        self.note = note

        # Mettre à jour la couleur des boutons
        for i, button in enumerate(self.vote_buttons, start=1):
            if i == note:
                button.defaultColor = (0, 240, 28)  # Couleur pour le bouton sélectionné
            else:
                button.defaultColor = (255, 255, 255)  # Couleur par défaut

    def nextDrawing(self, note: int):
        consolLog.info(self.votesManager.participants, self.index+1, note)  # Debug
        self.votesManager.vote(self.votesManager.participants[self.index], note, self.roomManager.currentRound)

        if self.index < len(self.votesManager.participants)-1:
            self.progressBar.run_start()  # Re-start de la ProgressBar
            self.setNote(1)  # Reset de la note

            # Réinitialiser la couleur de tous les boutons
            for button in self.vote_buttons:
                button.defaultColor = (255, 255, 255)

            self.index += 1
            self.spriteGroup.remove(self.drawing)
            self.drawing = Image(os.path.join(self.tempdir.name, self.drawnList[self.index]), self.drawRect)
            self.spriteGroup.add(self.drawing)
            pygame.display.flip()
        else:
            self.sceneManager.setAsCurrentScene(WinnerScene(self.sceneManager, self.votesManager, self.gameManager, self.roomManager))