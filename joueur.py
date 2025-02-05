from typing import Self


class joueur:

    """
    Classe permettant de représenter le joueur, pour l'instant plus une idée qu'une réelle implémentation
    """

    def __init__(self, nom:str, points_de_vie: int, anim_attente:list[str], anim_attaques:list[str], coups:list[str]):
        """
        :param nom: une chaîne de caractères pour le nom du joueur
        :param points_de_vie: un entier représentant les points de vie du joueur
        :param anim_attente: une liste de chaînes de caractères, on peut imaginer que ces chaines sont des chemins vers des sprites
        :param anim_attaques: pareil, pour les attaques
        :param coups: une liste de coups (chaînes de caractères) que le joueur peut donner
        """

        self.pts_vie = points_de_vie
        self.anim_att = anim_attente
        self.anim_atq = anim_attaques
        self.coups = coups
        self.etat = None #on va se servir de cette variable pour determiner l'état du joueur lorsqu'il prend un coup

    def donner_cout(self, cout:tuple[str, int], joueur2:Self):
        """
        Méthode qui gère les coups reçus du joueur adverse, si le joueur se protège avant le coup alors le coup ne fait que 20% de ses dégâts, 100% sinon.
        :param cout: un tuple représentant le coup reçu, le nom du coup et ses dégâts
        :param joueur2: le joueur adverse, peut-être utile plus tard
        :return:
        """
        if self.etat == 'parade':
            self.pts_vie -= 0.2 * cout[1]
        else:
            self.pts_vie -= cout[1]

        if self.pts_vie <= 0:
            #faire en sorte que la partie soit terminée et donner la victoire au joueur 2
            #mettre à jour l'affichage des deux joueurs (animation de défaite/fin de victoire)
            return

        #mettre à jour l'affichage du joueur1





