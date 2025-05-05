import echec
from echec import Echec
import random

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
    "K": 2  # Roi (King) 
}
        self.table_transposition = {}

    def recup_mouv(self, jeu:Echec):

        mouv_dispo = jeu.tous_mouv_valides(self.couleur)
        random.shuffle(mouv_dispo)

        if not mouv_dispo:
            return None
        if len(mouv_dispo) == 1:
            return mouv_dispo[0]

        meilleur_score, meilleur_mouv = float('-inf'), mouv_dispo[0]

        for mouv in mouv_dispo:

            jeu.faire_mouv(mouv)
            self.table_transposition = {}
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
        if len(pieces_couleur) == 0:
            return 1000  # On a perdu → donc on a gagné → favoriser ce cas
        if len(pieces_adverses) == 0:
            return -1000  # L'adversaire a perdu → on a perdu → mauvais
        if not coups_couleur:
            if len(pieces_couleur) < len(pieces_adverses):
                return 1000  # Moins de pièces → gagne
            else:
                return -1000  # Plus de pièces → perd
        if not coups_adverses:
            if len(pieces_adverses) < len(pieces_couleur):
                return -1000  # Adversaire gagne → on perd
            else:
                return 1000  # Il a plus de pièces → il perd → nous gagnons

        # Évaluation positionnelle
        def valeur_piece(p):
            valeurs = {"P": 1, "N": 2, "B": 2, "R": 3, "Q": 4, "K": 5}
            return valeurs[p.nom.upper()]

        # Score = nombre de nos pièces (on veut s'en débarrasser) - nombre de leurs pièces (on veut qu'ils en perdent)
        score_self = sum(valeur_piece(p) for p in pieces_couleur.values() if p)
        score_adv = sum(valeur_piece(p) for p in pieces_adverses.values() if p)

        # Mobilite : on veut pouvoir bouger pour se faire capturer → bonus si beaucoup de coups possibles
        # En fait je pense qu'il faut limiter les coups, plus one se rapproche de 0 et plus on gagne
        mobilite_self = len(coups_couleur)
        mobilite_adv = len(coups_adverses)

        return (score_adv - score_self) + 0.1 * (mobilite_adv - mobilite_self)

    def reverse_mini_max(self, jeu: Echec, profondeur, est_maximisant, couleur):

        if jeu.partie_terminee() or profondeur == 0:
            return self.heuristique(jeu, couleur)

        if est_maximisant:
            meilleur_score = float('-inf')
            mouv_valides = jeu.tous_mouv_valides(couleur)
            random.shuffle(mouv_valides)
            for mouv in mouv_valides:
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
            mouv_valides = jeu.tous_mouv_valides(couleur)
            random.shuffle(mouv_valides)
            for mouv in mouv_valides:
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

        etat = jeu.recup_etat()
        if etat in self.table_transposition:
            score_stocke, profondeur_stockee, flag = self.table_transposition[etat]
            if profondeur_stockee >= profondeur:
                if flag == "exact":
                    return score_stocke
                elif flag == "borne_inf":
                    alpha = max(alpha, score_stocke)
                elif flag == "borne_sup":
                    beta = min(beta, score_stocke)
                if alpha >= beta:
                    return score_stocke

        if jeu.partie_terminee() or profondeur == 0:
            score = self.heuristique(jeu, couleur)
            self.table_transposition[etat] = (score, profondeur, "exact")
            return score

        if est_maximisant:
            meilleur_score = float('-inf')
            mouv_valides = jeu.tous_mouv_valides(couleur)
            random.shuffle(mouv_valides)
            for mouv in mouv_valides:
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
            flag = "exact" if meilleur_score == alpha else "borne_inf"
            self.table_transposition[etat] = (meilleur_score, profondeur, flag)
            return meilleur_score

        else:
            meilleur_score = float('+inf')
            mouv_valides = jeu.tous_mouv_valides(couleur)
            random.shuffle(mouv_valides)
            for mouv in mouv_valides:
                jeu.faire_mouv(mouv)
                if couleur == "blanc":
                    c = "noir"
                else:
                    c = "blanc"
                score = self.reverse_alpha_beta(jeu, profondeur - 1, alpha, beta, True, c)
                jeu.annuler_mouv()
                meilleur_score = min(meilleur_score, score)
                beta = min(beta, score)
                if beta <= alpha:
                    break
            flag = "exact" if meilleur_score == beta else "borne_sup"
            self.table_transposition[etat] = (meilleur_score, profondeur, flag)
            return meilleur_score