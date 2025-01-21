import pygame

eventHandlers = {pygame.QUIT: pygame.quit}

    
    
def addEventHandler(event, action):
    eventHandlers[event] = action
    
def update(event):
    for handler in eventHandlers:
        if event.type == handler:
            eventHandlers[handler](event)