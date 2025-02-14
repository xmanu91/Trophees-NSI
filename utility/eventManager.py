import pygame
import sys

eventHandlers = {}

def addEventHandler(event, action):
    if event not in eventHandlers:
        eventHandlers[event] = [action]
    else:
        eventHandlers[event].append(action)
    
def update(event):
    fixedHandledEvents = eventHandlers
    for handledEvent in fixedHandledEvents:
        if event.type == handledEvent:
            for i in range(len(fixedHandledEvents[handledEvent])):
                fixedHandledEvents[handledEvent][i](event)
                