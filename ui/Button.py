import pygame

class Button(pygame.sprite.Sprite): 
    def __init__(self, default_color,hover_color, width, height, x, y, image, action):

        self.default_color = default_color  #couleur de base du bouton
        self.hover_color = hover_color  #couleur quand on passe le curseur sur le bouton
        self.width = width #largeur du bouton
        self.height = height #hauteur du bouton
        self.image = pygame.image.load("image.png").convert_alpha() #On load une image
        self.rect = self.image.get_rect(topleft=(x, y))  #Pour placer l'image, on place son point en haut à gauche avec x y 
        self.action = action #on instancira un fonction pour chaque bouton 
        self.alpha = 128  #définie une transparence de 50%, la valeur changera, on verra comment ça rend !

    def update(self): #la fonction qui sera mise à jour en bouclle à chaque frame
        pos = pygame.mouse.get_pos() #prend la position du curseur
        mouse_pressed = pygame.mouse.get_pressed()[0] # vérifie si le bouton gauche de la souris est pressé

        if self.rect.collidepoint(pos):  # s'execute si le curseur touche un bouton
            self.image.fill(self.hover_color) # met de la couleur sur le bouton quand on passe dessus avec le curseur
            self.image.set_alpha(self.alpha) # ajoute de la transparence ppour toujours voir l'image

            if mouse_pressed :  # s'execute si le bouton gauche de la souris est pressé
                self.image.fill((255,0,0)) # rend le bouton rouge
                self.image.set_alpha(self.alpha) # set la transparence
                pygame.Surface.convert_alpha(self.image) # ajoute la transparence

                if self.action: #s'execute si il y a une action instancier au bouton en question (je l'ai mis apart pour prévenir des potentiels bugs)
                    self.action() # execute donc l'action

        else :  #s'execute si le curseur ne touche pas/plus le bouton
            self.image.fill(self.default_color) # on met sa couleur par défaut 
            self.image.set_alpha(self.alpha) # set la transparence
            pygame.Surface.convert_alpha(self.image)  # ajoute la transparence 


