from typing import Self,Optional,Tuple,Dict 

# Classe de base pour toutes les pièces
class Piece:
    def __init__(self, couleur: str):
        self.couleur = couleur  # "blanc" ou "noir"

    def peut_se_deplacer(self, pos_actuelle: str, pos_cible: str, plateau: Dict[str, 'Piece']) -> bool:
        """
        Doit être implémentée par chaque sous-classe.
        Vérifie si la pièce peut se déplacer de pos_actuelle vers pos_cible.
        """
        raise NotImplementedError

    def deplacer(self, pos_actuelle: str, pos_cible: str, plateau: Dict[str, 'Piece']):
        """
        Déplace la pièce de pos_actuelle vers pos_cible si c'est possible.
        """
        if self.peut_se_deplacer(pos_actuelle, pos_cible, plateau):
            plateau[pos_cible] = plateau.pop(pos_actuelle)
        else:
            print("Déplacement impossible.")
    


class Reine(Piece):
    def peut_se_deplacer(self, pos_actuelle: str, pos_cible: str, plateau: Dict[str, 'Piece']) -> bool:


class Pion(Piece):
    def peut_se_deplacer(self, pos_actuelle: str, pos_cible: str, plateau: Dict[str, 'Piece']) -> bool:



class Fou(Piece):
    def peut_se_deplacer(self, pos_actuelle: str, pos_cible: str, plateau: Dict[str, 'Piece']) -> bool:



class Roi(Piece):
    def peut_se_deplacer(self, pos_actuelle: str, pos_cible: str, plateau: Dict[str, 'Piece']) -> bool:



class Tour(Piece):
    def peut_se_deplacer(self, pos_actuelle: str, pos_cible: str, plateau: Dict[str, 'Piece']) -> bool:



class Cavalier(Piece):
    def peut_se_deplacer(self, pos_actuelle: str, pos_cible: str, plateau: Dict[str, 'Piece']) -> bool:



class Echec:
    def __init__(self):
        self.joueur1: Dict[str, Piece] = {}  # Dictionnaire pour les pièces du joueur 1 ("blanc")
        self.joueur2: Dict[str, Piece] = {}  # Dictionnaire pour les pièces du joueur 2 ("noir")
        self.plateau: Dict[str, Piece] = {}


    def initialiser_pieces(self):
        """
        Initialise les pièces sur le plateau.
        """

    def jouer_tour(self, joueur: Dict[str, Piece], adversaire: Dict[str, Piece]):
        """
        Gère un tour de jeu pour un joueur.
        """

    def verifier_pat(self) -> Optional[str]:
        """
        Vérifie s'il y a pat.
        """

    def verifier_victoire(self) -> Optional[str]:
        """
        Vérifie si un joueur a gagné.
        Retourne "blanc", "noir" ou "Egalite".
        """
    def doit_capturer(joueur: Dict[str, Piece], adversaire: Dict[str, Piece], plateau: Dict[str, Piece]) -> Optional[Tuple[str, str]]:
    """
    Vérifie si un joueur a une obligation de capture et retourne le premier mouvement valide de capture trouvé.
    
    :param joueur: Dictionnaire des pièces du joueur.
    :param adversaire: Dictionnaire des pièces de l'adversaire
    """
    
    def afficher_plateau(self):




def choisir_niveau_ia():
    print("Choisissez le niveau de l'IA :")
    print("1. Débutant")
    print("2. Intermédiaire")
    print("3. Expert")

    niveau = input("Entrez le niveau (1, 2 ou 3) : ")
    if niveau in ["1", "2", "3"]:
        return ["debutant", "intermediaire", "expert"][int(niveau) - 1]
    else:
        print("Niveau invalide. Veuillez réessayer.")
        return choisir_niveau_ia()

def choisir_mode_jeu():
    print("Bienvenue dans le jeu d'échecs !")
    print("Veuillez choisir un mode de jeu :")
    print("1. Jouer contre un autre joueur humain.")
    print("2. Jouer contre une IA (niveaux : débutant, intermédiaire, expert).")
    print("3. Lancer un tournoi entre plusieurs IAs.")

    choix = input("Entrez votre choix (1, 2 ou 3) : ")

    if choix == "1":
        return "joueur_vs_joueur"
    elif choix == "2":
        niveau_ia = choisir_niveau_ia()
        return f"joueur_vs_ia_{niveau_ia}"
    elif choix == "3":
        return "tournoi_ia"
    else:
        print("Choix invalide. Veuillez réessayer.")
        return choisir_mode_jeu()


if __name__ == "__main__":
    main()