import pygame
import time

class ProgressBar(pygame.sprite.Sprite):
    def __init__(self, rect: pygame.Rect, color: pygame.Color, durationInSeconds: int, endAction):
        super().__init__()
        self.rect = rect
        self.color = color
        self.duration = durationInSeconds
        self.image = pygame.Surface((self.rect.width, self.rect.height))
        self.image.fill(self.color)
        self.endAction = endAction
        self.value = 0  
        self.startTime = None  

    def update(self):
        if self.startTime is not None:
            elapsedTime = time.time() - self.startTime
            if self.value < self.duration:
                self.value = elapsedTime
                self.image = pygame.Surface((self.rect.width * (self.value / self.duration), self.rect.height))
                self.image.fill(self.color)
            else:
                self.endAction()

    def run_start(self):
        self.value = 0 
        self.startTime = time.time()