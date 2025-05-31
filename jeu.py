from joueur import Joueur
from ia import IAFacile, IAMoyenne, IADifficile
from echec import Echec, Mouv

class Jeu:
    """
    Classe principale du jeu, permet de lancer une partie
    """

    def __init__(self, plateau):
        self.plateau = plateau
        self.main()

    def main(self):
        """
        Fonction principale du jeu pour lancer la partie et sélectionner le type de partie.
        """
        print("Bonjour, veuillez choisir le type de jeu :")
        print("1. Joueur contre Joueur")
        print("2. Joueur contre IA")
        print("3. IA contre IA")

        IAs = {"1":IAFacile, "2":IAMoyenne, "3":IADifficile}

        while True:
            choix = int(input("Votre choix ?"))
            match choix:

                case 1:
                    j1 = Joueur("blanc")
                    j2 = Joueur("noir")
                    break
                case 2:
                    diff = input('Difficulté de l\'ia ? (1 = facile, 2 = moyenne, 3 = difficile)')
                    choix = input('IA qui commence ? O/N :')
                    if diff not in IAs:
                        print("Veuillez choisir une difficulté cohérente.")
                        continue
                    match choix:
                        case "O":
                            j1 = IAs[diff]("blanc")
                            j2 = Joueur("noir")
                            break
                        case "N":
                            j2 = IAs[diff]("noir")
                            j1 = Joueur("blanc")
                            break
                        case _:
                            print("Veuillez faire un choix correct.")
                case 3:
                    diff1 = input('Difficulté de l\'ia 1 (blanc) ? (1 = facile, 2 = moyenne, 3 = difficile)')
                    diff2 = input('Difficulté de l\'ia 2 (noir) ? (1 = facile, 2 = moyenne, 3 = difficile)')
                    if diff1 not in IAs or diff2 not in IAs:
                        print("Veuillez choisir une difficulté cohérente.")
                        continue
                    j1 = IAs[diff1]("blanc")
                    j2 = IAs[diff2]("noir")
                    break
                case _:
                    print("Veuillez faire un choix correct.")

        joueurs = []
        joueurs.append(j1)
        joueurs.append(j2)

        compteur = 0
        coups_sans_capture = 0

        while True:
            jc = None
            for j in joueurs:
                print(f'Coup numéro {compteur}')
                jc = j
                self.plateau.afficher_echiquier()
                mouv = j.recup_mouv(self.plateau)

                if mouv is None or not self.plateau.tous_mouv_valides(j.couleur):
                    print(f"Le joueur {j.couleur} ne peut plus jouer.")
                    # Gagne si a le moins de pièces
                    nb_blanc = len(self.plateau.pieces_blanches)
                    nb_noir = len(self.plateau.pieces_noires)
                    if nb_blanc < nb_noir:
                        print("Le joueur blanc a gagné !")
                    elif nb_noir < nb_blanc:
                        print("Le joueur noir a gagné !")
                    else:
                        print("Match nul (même nombre de pièces).")
                    return

                self.plateau.faire_mouv(mouv)
                compteur += 1

                if mouv.piece_supp is not None:
                    coups_sans_capture = 0
                else:
                    coups_sans_capture += 1

                if self.plateau.partie_terminee():
                    break

            if self.plateau.partie_terminee():
                break
            if coups_sans_capture >= 50:
                if len(self.plateau.pieces_noires) < len(self.plateau.pieces_blanches):
                    print("Les noirs ont gagné (moins de pièces).")
                elif len(self.plateau.pieces_blanches) < len(self.plateau.pieces_noires):
                    print("Les blancs ont gagné (moins de pièces).")
                else:
                    print("Match nul (50 coups sans capture)")
                break
e = Echec()
Jeu(e)