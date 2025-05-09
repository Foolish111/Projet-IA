import echec
from echec import Echec

class Joueur:
    """
    Classe pour gérer un joueur humain.
    """


    def __init__(self, couleur):
        self.couleur = couleur

    def recup_mouv(self, jeu: Echec):
        """
        Classe pour récupérer le coup du joueur basé sur son entrée. On regarde ensuite si le coup est valide et si c'est le cas on
        le joue.
        :param jeu: l'objet Echec responsable de la gestion de la partie
        """


        while True:

            pos = input(f"Au tour des {self.couleur}s. Position de la pièce à bouger ? (ex: e2) ")
            try:
                pos_piece = echec.notation_vers_coords(pos)
                piece = jeu.echiquier.get(pos_piece)
                if piece is None or piece.couleur != self.couleur:
                    print("Position invalide ou ce n'est pas votre pièce.")
                    continue
            except ValueError:
                print("Format de position invalide. Veuillez entrer une position valide (ex: e2).")
                continue

            nouvelle_pos_notation = input("Nouvelle position ? (ex: e4) ")
            try:
                nouvelle_pos = echec.notation_vers_coords(nouvelle_pos_notation)
            except ValueError:
                print("Format de position invalide. Veuillez entrer une position valide (ex: e4).")
                continue

            if piece.mouvement_valide(nouvelle_pos, jeu.echiquier):
                if jeu.peut_capturer(jeu.echiquier, self.couleur) and (
                    nouvelle_pos not in jeu.echiquier or jeu.echiquier[nouvelle_pos].couleur == piece.couleur
                ):
                    print("Vous devez capturer une pièce si possible.")
                    continue

                mouv = echec.Mouv(pos_piece, nouvelle_pos, jeu.echiquier)

                return mouv

            else:
                if not piece.mouvements_dispo(pos_piece[0], pos_piece[1], jeu.echiquier, piece.couleur):
                    print(f"Le joueur {piece.couleur} ne peut plus se déplacer, il gagne donc la partie !")
                    break
                print("Mouvement impossible.")