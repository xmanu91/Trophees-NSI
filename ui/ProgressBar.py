import pygame
import time
import threading
import utility.eventManager as eventManager

class ProgressBar(pygame.sprite.Sprite):
    def __init__(self, rect: pygame.Rect, color: pygame.Color, durationInSeconds: int, endAction):
        super().__init__()
        self.rect = rect
        self.color = color
        self.duration = durationInSeconds
        self.image = pygame.Surface((self.rect.width, self.rect.height))
        self.image.fill(self.color)
        self.endAction = endAction

    def start(self):
        timer = time.time()
        while self.value < self.duration:

            for event in pygame.event.get():    # Detection de la fermeture pygame afin de stopper la thread
                if event.type == pygame.QUIT:   # A changer
                    return

            self.value = float(time.time() - timer)
            self.image = pygame.Surface((self.rect.width * (self.value / self.duration), self.rect.height))
            self.image.fill(self.color)
        
        self.endAction()

    def run_start(self):
        self.value = 0
        thread = threading.Thread(target=self.start)
        thread.start()