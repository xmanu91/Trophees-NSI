import pygame

class Button(): 
    def __init__(self, default_color, hover_color, width, height, x, y, action, image, x_image, y_image, text, x_text, y_text):

        self.default_color = default_color  
        self.hover_color = hover_color  
        self.width = width 
        self.height = height 
        self.x = x
        self.y = y
        self.action = action
        #image plus sa position :
        self.image = pygame.image.load("image.png").convert_alpha() 
        self.x_image = x_image
        self.y_image = y_image
        # texte + sa position :
        self.text = text 
        self.x_text = x_text
        self.y_text = y_text


        self.surface = pygame.Surface((self.width, self.height)) #Surface du bouton
        self.position = pygame.Rect((self.x, self.y, self.width, self.height))  #Position du bouton sur l'écran
        self.position_image = self.image.get_rect(topleft=(self.x_image, self.y_image)) #Position de l'image

        self.font = pygame.font.Font(None, 36)  # police par défaut, taille 36 pixels
        self.surface_text = self.font.render(self.text, True, (0, 0, 0))  # texte en noir
        self.position_text = self.surface_text.get_rect(topleft=(self.x_text, self.y_text)) # position du texte
        


    def update(self): #la fonction qui sera mise à jour en boucle à chaque frame
        pos = pygame.mouse.get_pos() #prend la position du curseur
        mouse_pressed = pygame.mouse.get_pressed()[0] # vérifie si le bouton gauche de la souris est pressé

        if self.position.collidepoint(pos): #si curseur touche un bouton
            self.surface.fill(self.hover_color) 
            if mouse_pressed :  
                self.surface.fill((255,0,0))
 # on changera cette couleur quand on verra la palette de couleur qu'on utilisera sur l'écran 

                if self.action:
                    self.action() 

        else :  #s'execute si le curseur ne touche pas/plus le bouton
            self.surface.fill(self.default_color) 

