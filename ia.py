import echec
from echec import Echec

"""
def reverse_minimax_decision(etat, profondeur):

def reverse_max_value(etat, profondeur):

def reverse_min_value(etat, profondeur):


def reverse_alpha_beta_decision(etat, profondeur):
def reverse_max_value_alpha_beta(etat, alpha, beta, profondeur):
def reverse_min_value_alpha_beta(etat, alpha, beta, profondeur):


def fin_de_partie(etat):


def evaluer(etat):

def generer_coups(etat):

def appliquer_coup(etat, coup):
"""

class IA:

    def __init__(self, couleur, profondeur):
        self.couleur = couleur
        self.profondeur = profondeur

    def recup_mouv(self, jeu:Echec):

        mouv_dispo = jeu.tous_mouv_valides(self.couleur)

        if not mouv_dispo:
            return None
        if len(mouv_dispo) == 1:
            return mouv_dispo[0]

        meilleur_score, meilleur_mouv = float('-inf'), mouv_dispo[0]

        for mouv in mouv_dispo:

            jeu.faire_mouv(mouv)
            score = self.reverse_mini_max(jeu, self.profondeur, True, self.couleur)
            jeu.annuler_mouv()

            if score > meilleur_score:
                meilleur_score = score
                meilleur_mouv = mouv

            if score == float('+inf'):
                break

        return meilleur_mouv

    def nb_pieces_en_vie(self, jeu:Echec, couleur):

        res = 0
        if couleur == "blanc":
            for k, v in jeu.pieces_blanches:
                if v is not None:
                    res += 1
        else:
            for k, v in jeu.pieces_noires:
                if v is not None:
                    res += 1

        return res

    def heuristique(self, jeu: Echec, couleur):

        nb_j1 = self.nb_pieces_en_vie(jeu, couleur)
        if couleur == "noir":
            nb_j2 = self.nb_pieces_en_vie(jeu, "blanc")
        else:
            nb_j2 = self.nb_pieces_en_vie(jeu, "noir")

        if nb_j1 == 0:
            return float('+inf')
        if nb_j2 == 0:
            return float('-inf')

        if len(jeu.tous_mouv_valides(couleur)) == 0:
            return float('+inf')
        #TODO rajouter une vérif si l'autre joueur n'a plus de pièces,
        #probablement à ajouter quand on change le type de la couleur vers un int

        return nb_j2 - nb_j1

    def reverse_mini_max(self, jeu: Echec, profondeur, est_maximisant, couleur):

        #print(f'profondeur : {profondeur}')

        if jeu.partie_terminee() or profondeur == 0:
            return self.heuristique(jeu, couleur)

        if est_maximisant:
            meilleur_score = float('-inf')
            for mouv in jeu.tous_mouv_valides(couleur):
                jeu.faire_mouv(mouv)
                if couleur == "blanc":
                    c = "noir"
                else:
                    c = "blanc"
                score = self.reverse_mini_max(jeu, profondeur - 1, False, c)
                jeu.annuler_mouv()
                meilleur_score = max(meilleur_score, score)

            return meilleur_score

        else:
            meilleur_score = float('-inf')
            for mouv in jeu.tous_mouv_valides(couleur):
                jeu.faire_mouv(mouv)
                if couleur == "blanc":
                    c = "noir"
                else:
                    c = "blanc"
                score = self.reverse_mini_max(jeu, profondeur - 1, True, c)
                jeu.annuler_mouv()
                meilleur_score = min(meilleur_score, score)

            return meilleur_score