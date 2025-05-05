from joueur import Joueur
from ia import IA
from echec import Echec, Mouv

class Jeu:

    def __init__(self, plateau):
        self.plateau = plateau
        self.main()

    def main(self):

        print("Bonjour, veuillez choisir le type de jeu :")
        print("1. Joueur contre Joueur")
        print("2. Joueur contre IA")
        print("3. IA contre IA")


        while True:
            choix = int(input("Votre choix ?"))
            match choix:

                case 1:
                    j1 = Joueur("blanc")
                    j2 = Joueur("noir")
                    break
                case 2:
                    prof = int(input('Profondeur de l\'ia ?'))
                    choix = input('IA qui commence ? O/N')
                    if choix == 'O':
                        j1 = IA('blanc',prof)
                        j2 = Joueur('noir')
                    else:
                        j1 = Joueur('blanc')
                        j2 = IA('noir', prof)
                    break
                case 3:
                    prof1 = int(input('Profondeur de l\'ia 1 ?'))
                    prof2 = int(input('Profondeur de l\'ia 2 ?'))
                    j1 = IA('blanc', prof1)
                    j2 = IA('noir', prof2)
                    break
                case _:
                    print('Veuillez entrer un choix valide.')

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
                print("Match nul (50 coups sans capture)")
                break
e = Echec()
Jeu(e)