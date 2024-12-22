import pygame

class Button(): 
    def __init__(self, default_color, hover_color, buttonRect, action, image, imageCoordinates, text, textCoordinates):
        self.default_color = default_color  
        self.hover_color = hover_color  
        self.buttonRect = pygame.Rect(buttonRect)
        self.action = action

        # image + sa position :
        self.image = pygame.image.load(image).convert_alpha() # j'ai mis "convert_alpha() pour gérer une potentiel transparence"
        self.imageCoordinates = pygame.Rect(imageCoordinates, self.image.get_size()) # imageCoordinates = x,y et self.image.get_size() = width, height

        # texte + sa position :
        self.font = pygame.font.Font(None, 36)  # police par défaut, taille 36 pixels
        self.surface_text = self.font.render(text, True, (0, 0, 0))  # texte en noir
        self.textCoordinates = pygame.Rect(textCoordinates, self.surface_text.get_size()) 

        # surface du bouton :
        self.surface = pygame.Surface(self.buttonRect.size) # self.buttonRect.size = (width, height)

    def update(self):  # la fonction qui sera mise à jour en boucle à chaque instant
        pos = pygame.mouse.get_pos()  # prend la position du curseur
        mouse_pressed = pygame.mouse.get_pressed()[0]  # vérifie si le bouton gauche de la souris est pressé

        if self.buttonRect.collidepoint(pos):  # si le curseur touche un bouton
            self.surface.fill(self.hover_color)
            if mouse_pressed:  
                self.surface.fill((255, 0, 0))  # couleur du clic (rouge, on changera la couleur je pense)
                if self.action:
                    self.action()
        else:  # s'exécute si le curseur ne touche pas/plus le bouton
            self.surface.fill(self.default_color)
