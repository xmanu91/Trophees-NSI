from typing import Callable
import threading
import time

class Timer():
    def __init__(self, timerDuration: int, textTimer, action: Callable):
        self.timerDuration = timerDuration
        self.textTimer = textTimer
        self.action = action
    
    def startTimer(self):
        threading.Thread(target=self.timer, daemon=True).start()
    
    def timer(self):
        timer = 0
        while timer < self.timerDuration:
            time.sleep(1)
            timer += 1
            self.textTimer.setText(str(self.timerDuration - timer))
        self.action()