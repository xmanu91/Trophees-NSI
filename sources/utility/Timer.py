import time
from typing import Callable

class Timer():
    def __init__(self, timerDuration: int, textTimer, action: Callable):
        self.timerDuration = timerDuration
        self.textTimer = textTimer
        self.action: Callable = action
        self.startTime: None | float = None
    
    def start(self) -> None:
        self.startTime = time.time()

    def update(self):
        if self.startTime:
            elapsedTime = time.time() - self.startTime
            if elapsedTime < self.timerDuration:
                self.textTimer.setText(str(int(self.timerDuration - elapsedTime)))
            else:
                self.startTime = None
                self.action()