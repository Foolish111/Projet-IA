from echec import Echec
import random
import time

class TimeUp(Exception):
    pass

class IA:
    """
    Classe parente IA, permet de gérer les IA, leurs méthodes communes.
    """

    def __init__(self, couleur):
        self.couleur = couleur
        self.profondeur = None
        self.table_transposition = {}
        self.limite_temps = 5
        self.debut_temps_coup = None

    def recup_mouv(self, jeu:Echec):
        """
        Permet de récupérer le meilleur coup possible que l'IA peut jouer, à l'aide d'alpha beta, pour cela
        on récupère la liste de tous les coups possibles que l'IA peut jouer, on la mélange pour éviter de jouer toujours les mêmes coups
        à chaque partie, et pour chaque coup on regarde son score à l'aide d'alpha beta, puis on sélectionne le coup avec le score le plus élevé.
        Il y a une limite de temps, de 5 secondes par coup pour que les parties se fassent dans un temps raisonnable.

        :param jeu: l'objet Echec responsable de la gestion de la partie
        :return: le meilleur coup possible
        """

        self.debut_temps_coup = time.time()

        mouv_dispo = jeu.tous_mouv_valides(self.couleur)
        random.shuffle(mouv_dispo)

        if not mouv_dispo:
            return None
        if len(mouv_dispo) == 1:
            return mouv_dispo[0]

        meilleur_score, meilleur_mouv = float('-inf'), mouv_dispo[0]

        try:
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

        except TimeUp:
            jeu.annuler_mouv()
            pass

        return meilleur_mouv

    def nb_pieces_en_vie(self, jeu:Echec, couleur):
        """
        Retourne le nombre pièces encore en vie de l'IA
        :param jeu: l'objet Echec responsable de la gestion de la partie
        :param couleur: la couleur de l'IA
        :return: le nombre pièces encore en vie de l'IA
        """

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
        pass

    def reverse_mini_max(self, jeu: Echec, profondeur, est_maximisant, couleur):
        """
        Algorithme minimax
        :param jeu: l'objet Echec responsable de la gestion de la partie
        :param profondeur: profondeur maximale de recherche du meilleur coup
        :param est_maximisant: booléen pour savoir si on doit minimiser ou maximiser le score
        :param couleur: la couleur du joueur
        :return: le score du coup
        """


        if jeu.partie_terminee() or self.profondeur == 0:
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
        """
        Algorithme minimax avec alpha beta. Ici nous avons aussi implémenté une table de transposition qui permet
        de ne pas refaire les calculs si on arrive sur un état du jeu déjà trouvé.
        """

        if self.debut_temps_coup and time.time() - self.debut_temps_coup > self.limite_temps:
            raise TimeUp("Temps dépassé pour ce coup")

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

        try:
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

        except TimeUp:
            jeu.annuler_mouv()
            self.table_transposition[etat] = (meilleur_score, profondeur, "approx")
            return meilleur_score

class IAFacile(IA):
    """
    IA facile, profondeur 2, heuristique basique.
    """


    def __init__(self, couleur):
        super().__init__(couleur)
        self.profondeur = 2

    def heuristique(self, jeu: Echec, couleur):
        """
        Heuristique très basique, on regarde d'abord si on a déjà perdu/gagné, si c'est le cas on retourne une valeur très haute/basse.
        Sinon on retourne la différence entre le nombre de pièces adervses et nos pièces, l'adervsaire doit avoir plus de pièces que nous
        donc on cherchera à maximiser cette différence.
        :param jeu:
        :param couleur:
        :return:
        """

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

        return len(pieces_adverses) - len(pieces_couleur)

class IAMoyenne(IA):
    """
    IA moyenne, profondeur de 4, heuristique un peu plus précise.
    """

    def __init__(self, couleur):
        super().__init__(couleur)
        self.profondeur = 4

    def heuristique(self, jeu: Echec, couleur):
        """
        Comme l'heuristique précédente on regarde d'abord si on a gagné/perdu. Ensuite on retourne
        la même différence que pour l'heuristique facile, sauf que cette fois-ci les pièces sont pondérées
        Cela nous permet de récompenser la capture de certaines pièces, plus importantes.
        :return: La différence du nombre de pièces entre les deux joueurs, pondérées par leur valeur.
        """
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
            valeurs = {"P": 1, "N": 2, "B": 3, "R": 3, "Q": 5, "K": 1}
            return valeurs[p.nom.upper()]

        # Score = nombre de nos pièces (on veut s'en débarrasser) - nombre de leurs pièces (on veut qu'ils en perdent)
        score_self = sum(valeur_piece(p) for p in pieces_couleur.values() if p)
        score_adv = sum(valeur_piece(p) for p in pieces_adverses.values() if p)

        return score_adv - score_self

class IADifficile(IA):
    """
    IA difficile, profondeur 6, heuristique beaucoup plus précise.
    """

    def __init__(self, couleur):
        super().__init__(couleur)
        self.profondeur = 6

    def heuristique(self, jeu: Echec, couleur):
        """
        Cette fois-ci on regarde aussi le nombre de coups possibles que les deux joueurs ont,
        on cherche à maximiser cette valeur pour l'adversaire et à la minimiser pour nous, étant
        donné que si nous n'avons plus de coups à jouer nous gagnons.
        """

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
            valeurs = {"P": 1, "N": 2, "B": 3, "R": 3, "Q": 5, "K": 1}
            return valeurs[p.nom.upper()]

        # Score = nombre de nos pièces (on veut s'en débarrasser) - nombre de leurs pièces (on veut qu'ils en perdent)
        score_self = sum(valeur_piece(p) for p in pieces_couleur.values() if p)
        score_adv = sum(valeur_piece(p) for p in pieces_adverses.values() if p)

        # Mobilite : on veut pouvoir bouger pour se faire capturer → bonus si beaucoup de coups possibles
        # En fait je pense qu'il faut limiter les coups, plus one se rapproche de 0 et plus on gagne
        mobilite_self = len(coups_couleur)
        mobilite_adv = len(coups_adverses)

        return (score_adv - score_self) + 0.1 * (mobilite_adv - mobilite_self)