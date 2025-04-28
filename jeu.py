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
        choix = int(input("Votre choix ?"))

        while True:
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

        while True:

            if self.plateau.partie_terminee():
                print('A gagné !')
                break

            for j in joueurs:

                self.plateau.afficher_echiquier()
                mouv = j.recup_mouv(self.plateau)

                self.plateau.faire_mouv(mouv)

                if self.plateau.partie_terminee():
                    print('A gagné !')
                    break

e = Echec()
Jeu(e)