import pygame
import shutil
import sys
import os

def centerCoordinates(coordinates, gap):
    return (coordinates[0]-gap, coordinates[1]-gap)

#Found on the internet
def fill_gradient(surface, color, gradient, rect=None, vertical=True, forward=True):
    """fill a surface with a gradient pattern
    Parameters:
    color -> starting color
    gradient -> final color
    rect -> area to fill; default is surface's rect
    vertical -> True=vertical; False=horizontal
    forward -> True=forward; False=reverse
    
    Pygame recipe: http://www.pygame.org/wiki/GradientCode
    """
    if rect is None: rect = surface.get_rect()
    x1,x2 = rect.left, rect.right
    y1,y2 = rect.top, rect.bottom
    if vertical: h = y2-y1
    else:        h = x2-x1
    if forward: a, b = color, gradient
    else:       b, a = color, gradient
    rate = (
        float(b[0]-a[0])/h,
        float(b[1]-a[1])/h,
        float(b[2]-a[2])/h
    )
    fn_line = pygame.draw.line
    if vertical:
        for line in range(y1,y2):
            color = (
                min(max(a[0]+(rate[0]*(line-y1)),0),255),
                min(max(a[1]+(rate[1]*(line-y1)),0),255),
                min(max(a[2]+(rate[2]*(line-y1)),0),255)
            )
            fn_line(surface, color, (x1,line), (x2,line))
    else:
        for col in range(x1,x2):
            color = (
                min(max(a[0]+(rate[0]*(col-x1)),0),255),
                min(max(a[1]+(rate[1]*(col-x1)),0),255),
                min(max(a[2]+(rate[2]*(col-x1)),0),255)
            )
            fn_line(surface, color, (col,y1), (col,y2))

def createDirectory(path: str):
    if not os.path.exists(path):
        os.mkdir(path) 

def initialiseDirectory(path: str):
    if os.path.isdir(path):
        shutil.rmtree(path)            
    if not os.path.exists(path):
        os.mkdir(path)

def getPath(relativePath: str):
    base_path = getattr(sys, '_MEIPASS', os.path.abspath("."))
    return os.path.join(base_path, relativePath)

def removeAlpha(color: tuple):
    return (color[0], color[1], color[2])

def getScalingFactors(x, y, screenWidth, screenHeight): # Parce que j'ai la flemme de chercher le bon coef alors que je connais déjà les coords que je veux utiliser
    return x*screenWidth/900, y*screenHeight/500

def getScalingFactorsX(x, screenWidth):
    return x*screenWidth/900

def getScalingFactorsY(y, screenHeight):
    return y*screenHeight/500