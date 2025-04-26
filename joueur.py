import echec
from echec import Echec

class Joueur:

    def __init__(self, couleur):
        self.couleur = couleur

    def recup_mouv(self, jeu: Echec):

        while True:
            print("Votre coup ?")
