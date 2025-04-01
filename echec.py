#https://gist.github.com/rsheldiii/2993225

cardinaux_echec = [(1,0), (0,1), (-1,0), (0,-1)]
diagonales_echec = [(1,1), (-1,1), (1,-1), (-1,-1)]

class Echec:

    def __init__(self):
        self.tour = "blanc"
        self.echiquier = {}
        self.placer_pieces()


    def placer_pieces(self):
        for i in range(0,8):
            self.echiquier[(i,1)] = Pion("blanc", "pion", 1)
            self.echiquier[(i,6)] = Pion("noir", "pion", -1)

        pieces = [Tour, Cavalier, Fou, Reine, Roi, Fou, Cavalier, Tour]
        pieces_noms = ["T", "C", "F", "Q", "K", "F", "C", "T"]

        for i in range(0,8):
            self.echiquier[(i,0)] = pieces[i]("blanc", pieces_noms[i])
            self.echiquier[((7-i), 7)] = pieces[i]("noir", pieces_noms[i])

class Piece:

    def __init__(self, couleur, nom):
        self.nom = nom
        self.couleur = couleur
        self.position = None

    def mouvement_valide(self, posfin, echiquier):
        if posfin in self.mouvements_dispo(self.position[0], self.position[1], echiquier, couleur = self.couleur):
            return True
        return False

    def mouvements_dispo(self, pos_x, pos_y, echiquier, couleur):
        print("pas de mouvements dispo pour pièce générale")
        return None

    def pos_valide(self, pos):
        if pos[0] < 8 and pos[0] >= 0 and pos[1] < 8 and pos[1] >= 0:
            return True
        return False

    #ajouter fonction pour regarder si piece ne traverse pas une autre piece
    def pas_rencontre(self, pos, echiquier, couleur, intervalles):
        mouv = []
        for x, y in intervalles:
            xtemp, ytemp = pos[0] + x, pos[1] + y
            cible = echiquier.get((xtemp, ytemp))
            if cible is None: mouv.append((xtemp, ytemp))
            elif cible.couleur != couleur:
                mouv.append((xtemp, ytemp))
                break
            else:
                break
            xtemp, ytemp = xtemp + x, ytemp + y
        return mouv

    def pos_sans_conflit(self, echiquier, couleur, pos):
        if self.pos_valide(pos) and (pos not in echiquier) or echiquier[pos].couleur != couleur:
            return True
        return False

def pos_cavalier(x1, y1, x2, y2):
    return [(x1+x2, y1+y2), (x1-x2, y1+y2), (x1+x2, y1-y2), (x1-x2, y1-y2), (x1+y2, x2+y1), (x1-y2, x2+y1), (x1+y2, x2-y1), (x1-y2, x2-y1)]

def pos_roi(x, y):
    return [(x+1, y), (x+1, y+1), (x+1, y-1), (x, y+1), (x, y-1), (x-1, y), (x-1, y+1), (x-1, y-1)]

class Roi(Piece):
    def mouvements_dispo(self, pos_x, pos_y, echiquier, couleur):
        return [(x,y) for x,y in pos_roi(pos_x,pos_y) if self.pos_sans_conflit(echiquier, couleur, (x,y))]

class Cavalier(Piece):
    def mouvements_dispo(self, pos_x, pos_y, echiquier, couleur):
        if couleur is None: couleur = self.couleur
        return [(x,y) for x,y in pos_cavalier(pos_x,pos_y, 2, 1) if self.pos_sans_conflit(echiquier, couleur, (x,y))]

class Fou(Piece):
    def mouvements_dispo(self, pos_x, pos_y, echiquier, couleur):
        if couleur is None: couleur = self.couleur
        return self.pas_rencontre((pos_x, pos_y), echiquier, couleur, diagonales_echec)

class Reine(Piece):
    def mouvements_dispo(self, pos_x, pos_y, echiquier, couleur):
        if couleur is None: couleur = self.couleur
        return self.pas_rencontre((pos_x, pos_y), echiquier, couleur, cardinaux_echec+diagonales_echec)

class Tour(Piece):
    def mouvements_dispo(self, pos_x, pos_y, echiquier, couleur):
        if couleur is None: couleur = self.couleur
        return self.pas_rencontre((pos_x, pos_y), echiquier, couleur, cardinaux_echec)

class Pion(Piece):

    def __init__(self, couleur, nom, direction):
        self.nom = nom
        self.couleur = couleur
        self.direction = direction

    def mouvements_dispo(self, pos_x, pos_y, echiquier, couleur):
        mouv = []
        if (pos_x +1, pos_y+self.direction) in echiquier and self.pos_sans_conflit(echiquier, couleur, (pos_x+1, pos_y+self.direction)):
            mouv.append((pos_x+1, pos_y+self.direction))
        if (pos_x - 1, pos_y + self.direction) in echiquier and self.pos_sans_conflit(echiquier, couleur, (pos_x - 1, pos_y + self.direction)):
            mouv.append((pos_x - 1, pos_y + self.direction))
        if (pos_x, pos_y+self.direction) not in echiquier and couleur == self.couleur:
            mouv.append((pos_x, pos_y+self.direction))
        return mouv