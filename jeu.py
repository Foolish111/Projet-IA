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

        compteur = 0

        while True:
            jc = None
            for j in joueurs:

                print(f'Coût numéro {compteur}')
                jc = j
                self.plateau.afficher_echiquier()
                mouv = j.recup_mouv(self.plateau)

                if mouv is None or not self.plateau.tous_mouv_valides(j.couleur):
                    break

                cmpt_noires = len(self.plateau.pieces_noires)
                cmpt_blanches = len(self.plateau.pieces_blanches)

                self.plateau.faire_mouv(mouv)

                compteur += 1

                if self.plateau.partie_terminee():
                    break


            if self.plateau.partie_terminee() or compteur > 50:
                if jc.couleur == "blanc":
                    if not self.plateau.tous_mouv_valides(jc.couleur) or len(self.plateau.pieces_blanches) < len(self.plateau.pieces_noires):
                        print(f'Le joueur {jc.couleur} a gagné !')
                        break
                    elif not self.plateau.tous_mouv_valides("noir") or len(self.plateau.pieces_noires) < len(self.plateau.pieces_blanches):
                        print(f'Le joueur noir a gagné !')
                        break
                    else:
                        print(f'Match nul !')
                        break
                else:
                    if not self.plateau.tous_mouv_valides(jc.couleur) or len(self.plateau.pieces_noires) < len(self.plateau.pieces_blanches):
                        print(f'Le joueur {jc.couleur} a gagné !')
                        break
                    elif not self.plateau.tous_mouv_valides("blanc") or len(self.plateau.pieces_blanches) < len(self.plateau.pieces_noires):
                        print(f'Le joueur noir a gagné !')
                        break
                    else:
                        print(f'Match nul !')
                        break


e = Echec()
Jeu(e)