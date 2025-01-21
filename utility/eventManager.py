import pygame

eventHandlers = {pygame.QUIT: [pygame.quit]}

def addEventHandler(event, action):
    if event not in eventHandlers:
        eventHandlers[event] = [action]
    else:
        eventHandlers[event].append(action)
    
def update(event):
    for handledEvent in eventHandlers:
        if event.type == handledEvent:
            for i in range(len(eventHandlers[handledEvent])):
                eventHandlers[handledEvent][i](event)
                