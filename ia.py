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
        self.valeurs = {
    "P": 1,  # Pion
    "N": 3,  # Cavalier (Knight)
    "B": 3,  # Fou (Bishop)
    "R": 5,  # Tour (Rook)
    "Q": 9,  # Reine (Queen)
    "K": 100  # Roi (King) — très élevé car essentiel
}


    def recup_mouv(self, jeu:Echec):

        mouv_dispo = jeu.tous_mouv_valides(self.couleur)

        if not mouv_dispo:
            return None
        if len(mouv_dispo) == 1:
            return mouv_dispo[0]

        meilleur_score, meilleur_mouv = float('-inf'), mouv_dispo[0]

        for mouv in mouv_dispo:

            jeu.faire_mouv(mouv)
            #score = self.reverse_mini_max(jeu, self.profondeur, True, self.couleur)
            score = self.reverse_alpha_beta(jeu, self.profondeur, float('-inf'), float('+inf'), True, self.couleur)
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
            for k, v in jeu.pieces_blanches.items():
                if v is not None:
                    res += 1
        else:
            for k, v in jeu.pieces_noires.items():
                if v is not None:
                    res += 1

        return res

    def heuristique(self, jeu: Echec, couleur):
        pieces_couleur = jeu.pieces_blanches if couleur == "blanc" else jeu.pieces_noires
        pieces_adverses = jeu.pieces_noires if couleur == "blanc" else jeu.pieces_blanches

        coups_couleur = jeu.tous_mouv_valides(couleur)
        coups_adverses = jeu.tous_mouv_valides("noir" if couleur == "blanc" else "blanc")

        # Cas de fin de partie
        if len(pieces_couleur) == 0 or len(coups_couleur) == 0:
            return -1000  # Défaite
        if len(pieces_adverses) == 0 or len(coups_adverses) == 0:
            return 1000  # Victoire

        # Évaluation positionnelle
        def valeur_piece(p):
            valeurs = {"P": 1, "N": 3, "B": 3, "R": 5, "Q": 9, "K": 100}
            return valeurs[p.nom.upper()]

        def score_total(pieces):
            return sum(valeur_piece(p) for p in pieces.values() if p)

        score_self = score_total(pieces_couleur)
        score_adv = score_total(pieces_adverses)

        mobilite_self = len(coups_couleur)
        mobilite_adv = len(coups_adverses)

        return (score_self - score_adv) + 0.1 * (mobilite_self - mobilite_adv)

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
            meilleur_score = float('+inf')
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

    def reverse_alpha_beta(self, jeu: Echec, profondeur, alpha, beta, est_maximisant, couleur):

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
                score = self.reverse_alpha_beta(jeu, profondeur - 1, alpha, beta, False, c)
                jeu.annuler_mouv()
                meilleur_score = max(meilleur_score, score)
                alpha = max(alpha, score)
                if beta <= alpha:
                    break
            return meilleur_score

        else:
            meilleur_score = float('+inf')
            for mouv in jeu.tous_mouv_valides(couleur):
                jeu.faire_mouv(mouv)
                if couleur == "blanc":
                    c = "noir"
                else:
                    c = "blanc"
                score = self.reverse_alpha_beta(jeu, profondeur - 1, alpha, beta, False, c)
                jeu.annuler_mouv()
                meilleur_score = min(meilleur_score, score)
                beta = min(beta, score)
                if beta <= alpha:
                    break
            return meilleur_score