#https://gist.github.com/rsheldiii/2993225


cardinaux_echec = [(1, 0), (0, 1), (-1, 0), (0, -1)]
diagonales_echec = [(1, 1), (-1, 1), (1, -1), (-1, -1)]

def coords_vers_notation(pos):
    """Convertit des coordonnées (x, y) en notation d'échecs (ex: (4, 3) -> 'e4')."""
    x, y = pos
    lettre = chr(x + ord('a'))# Convertit 0 -> 'a', 1 -> 'b', ..., 7 -> 'h'
    chiffre = str(y + 1)# Ajoute 1 car les rangées vont de 1 à 8
    return lettre + chiffre

def notation_vers_coords(notation):
    """Convertit une notation d'échecs (ex: 'e4') en coordonnées (x, y)."""
    if len(notation) != 2 or not notation[0].isalpha() or not notation[1].isdigit():
        raise ValueError("Format de position invalide.")
    
    lettre, chiffre = notation[0].lower(), notation[1]
    x = ord(lettre) - ord('a')# Convertit 'a' -> 0, 'b' -> 1, ..., 'h' -> 7
    y = int(chiffre) - 1# Soustrait 1 car les rangées vont de 0 à 7
    
    if not (0 <= x < 8 and 0 <= y < 8):
        raise ValueError("Coordonnées hors limites.")
    
    return (x, y)


class Mouv:

    def __init__(self, pos_dep, pos_arr, echiquier):

        self.dep = pos_dep
        self.arr = pos_arr
        self.piece_supp = None

        #on regarde si la case a une piece
        if pos_arr in echiquier and echiquier[pos_arr] is not None:
            self.piece_supp = echiquier[pos_arr]

    def __str__(self):
        print(f'Départ : {self.dep}, arrivée : {self.arr}, pièce supprimée : {self.piece_supp}')

class Echec:

    def __init__(self):
        self.tour = "blanc"
        self.echiquier = {}
        self.pieces_noires = {}
        self.pieces_blanches = {}
        self.mouv_faits = []
        self.placer_pieces()

    def recup_etat(self):
        # Créer une représentation unique de l'état actuel du jeu
        etat = {pos: (piece.couleur, piece.nom) for pos, piece in self.echiquier.items()}
        return frozenset(etat.items()), self.tour

    def placer_pieces(self):
        for i in range(8):
            self.echiquier[(i, 1)] = Pion("blanc", "P", (i, 1), 1)
            self.pieces_blanches[(i, 1)] = Pion("blanc", "P", (i, 1), 1)

            self.echiquier[(i, 6)] = Pion("noir", "P", (i, 6), -1)
            self.pieces_noires[(i, 6)] = Pion("noir", "P", (i, 6), -1)

        pieces = [Tour, Cavalier, Fou, Reine, Roi, Fou, Cavalier, Tour]
        noms = ["R", "N", "B", "Q", "K", "B", "N", "R"]

        for i in range(8):
            self.echiquier[(i, 0)] = pieces[i]("blanc", noms[i], (i, 0))
            self.pieces_blanches[(i, 0)] = pieces[i]("blanc", noms[i], (i, 0))

            self.echiquier[(i, 7)] = pieces[i]("noir", noms[i], (i, 7))
            self.pieces_noires[(i, 7)] = pieces[i]("noir", noms[i], (i, 7))

    def afficher_echiquier(self):
        print("  a b c d e f g h")
        for y in range(7, -1, -1):
            print(y + 1, end=" ")
            for x in range(8):
                piece = self.echiquier.get((x, y), " ")
                print(piece, end=" ")
            print()
        print()

    def peut_capturer(self, echiquier, couleur):
        for pos, piece in echiquier.items():
            if piece.couleur == couleur:
                for mouv in piece.mouvements_dispo(*piece.position, echiquier, couleur):
                    if mouv in echiquier and echiquier[mouv].couleur != couleur:
                        return True
        return False

    def partie_terminee(self):
        blanc, noir = False, False
        for piece in self.echiquier.values():
            if piece is not None:
                if piece.couleur == "blanc":
                    blanc = True
                elif piece.couleur == "noir":
                    noir = True
        if not blanc:
            print("Les blancs ont gagné.")
            return True
        if not noir:
            print("Les noirs ont gagné.")
            return True
        return False

    def tous_mouv_valides(self, couleur):

        mouv = []
        mouv_cap = []

        pieces = self.pieces_noires if couleur == "noir" else self.pieces_blanches

        for k,v in pieces.items():
            if v is not None:
                for m in v.mouvements_dispo(v.position[0], v.position[1], self.echiquier, v.couleur):
                    mv = Mouv(k, m, self.echiquier)
                    if mv.piece_supp is not None:
                        mouv_cap.append(mv)
                    mouv.append(mv)

        if mouv_cap:
            return mouv_cap
        else:
            return mouv

    def faire_mouv(self, mouv: Mouv):

        piece = self.echiquier.get(mouv.dep)
        if piece is None:
            return

        if piece.couleur == "blanc":
            self.pieces_blanches.pop(mouv.dep, None)
            if mouv.arr in self.pieces_noires and self.pieces_noires[mouv.arr] is not None:
                mouv.piece_supp = self.pieces_noires.pop(mouv.arr)
            self.pieces_blanches[mouv.arr] = piece
        else:
            self.pieces_noires.pop(mouv.dep, None)
            if mouv.arr in self.pieces_blanches:
                mouv.piece_supp = self.pieces_blanches.pop(mouv.arr)
            self.pieces_noires[mouv.arr] = piece

        self.echiquier.pop(mouv.dep, None)
        self.echiquier[mouv.arr] = piece
        piece.position = mouv.arr

        self.tour = "noir" if self.tour == "blanc" else "blanc"
        self.mouv_faits.append(mouv)

    def annuler_mouv(self):
        if not self.mouv_faits:
            return

        mouv = self.mouv_faits.pop()

        piece = self.echiquier.pop(mouv.arr, None)
        if piece is None:
            return  # Rien à annuler

        self.echiquier[mouv.dep] = piece
        piece.position = mouv.dep

        if piece.couleur == "blanc":
            self.pieces_blanches[mouv.dep] = piece
            self.pieces_blanches.pop(mouv.arr, None)
        else:
            self.pieces_noires[mouv.dep] = piece
            self.pieces_noires.pop(mouv.arr, None)

        if mouv.piece_supp is not None:
            self.echiquier[mouv.arr] = mouv.piece_supp
            if mouv.piece_supp.couleur == "blanc":
                self.pieces_blanches[mouv.arr] = mouv.piece_supp
            else:
                self.pieces_noires[mouv.arr] = mouv.piece_supp

        self.tour = "noir" if self.tour == "blanc" else "blanc"


class Piece:
    def __init__(self, couleur, nom, pos):
        self.nom = nom.upper() if couleur == "blanc" else nom.lower()
        self.couleur = couleur
        self.position = pos

    def __repr__(self):
        return self.nom

    def __str__(self):
        return self.nom

    def mouvement_valide(self, posfin, echiquier):
        return posfin in self.mouvements_dispo(self.position[0], self.position[1], echiquier, self.couleur)

    def mouvements_dispo(self, pos_x, pos_y, echiquier, couleur):
        print("pas de mouvements dispo pour pièce générale")
        return None

    def pos_valide(self, pos):
        x, y = pos
        return 0 <= x < 8 and 0 <= y < 8

    def pas_rencontre(self, pos, echiquier, couleur, intervalles):
        mouv = []
        for x, y in intervalles:
            xtemp, ytemp = pos[0] + x, pos[1] + y
            while self.pos_valide((xtemp, ytemp)):
                cible = echiquier.get((xtemp, ytemp))
                if cible is None:
                    mouv.append((xtemp, ytemp))
                elif cible.couleur != couleur:
                    mouv.append((xtemp, ytemp))
                    break
                else:
                    break
                xtemp, ytemp = xtemp + x, ytemp + y
        return mouv

    def pos_sans_conflit(self, echiquier, couleur, pos):
        if self.pos_valide(pos) and (pos not in echiquier or echiquier[pos].couleur != couleur):
            return True
        return False

def pos_cavalier(x, y):
    return [
        (x + 2, y + 1), (x + 2, y - 1),
        (x - 2, y + 1), (x - 2, y - 1),
        (x + 1, y + 2), (x + 1, y - 2),
        (x - 1, y + 2), (x - 1, y - 2)
    ]

def pos_roi(x, y):
    return [
        (x + 1, y), (x + 1, y + 1), (x + 1, y - 1),
        (x, y + 1), (x, y - 1), (x - 1, y),
        (x - 1, y + 1), (x - 1, y - 1)
    ]

class Roi(Piece):
    def mouvements_dispo(self, pos_x, pos_y, echiquier, couleur):
        return [(x, y) for x, y in pos_roi(pos_x, pos_y) if self.pos_sans_conflit(echiquier, couleur, (x, y))]

class Cavalier(Piece):
    def mouvements_dispo(self, pos_x, pos_y, echiquier, couleur):
        if couleur is None:
            couleur = self.couleur
        return [(x, y) for x, y in pos_cavalier(pos_x, pos_y) if self.pos_sans_conflit(echiquier, couleur, (x, y))]
class Fou(Piece):
    def mouvements_dispo(self, pos_x, pos_y, echiquier, couleur):
        if couleur is None:
            couleur = self.couleur
        return self.pas_rencontre((pos_x, pos_y), echiquier, couleur, diagonales_echec)

class Reine(Piece):
    def mouvements_dispo(self, pos_x, pos_y, echiquier, couleur):
        if couleur is None:
            couleur = self.couleur
        return self.pas_rencontre((pos_x, pos_y), echiquier, couleur, cardinaux_echec + diagonales_echec)

class Tour(Piece):
    def mouvements_dispo(self, pos_x, pos_y, echiquier, couleur):
        if couleur is None:
            couleur = self.couleur
        return self.pas_rencontre((pos_x, pos_y), echiquier, couleur, cardinaux_echec)

class Pion(Piece):
    def __init__(self, couleur, nom, pos, direction):
        super().__init__(couleur, nom, pos)
        self.direction = direction

    def mouvements_dispo(self, pos_x, pos_y, echiquier, couleur):
        mouv = []
        # Prises diagonales
        for dx in [-1, 1]:
            target_pos = (pos_x + dx, pos_y + self.direction)
            if target_pos in echiquier and echiquier[target_pos].couleur != self.couleur and self.pos_sans_conflit(echiquier, couleur, (pos_x + dx, pos_y + self.direction)):
                mouv.append((pos_x + dx, pos_y + self.direction))
        # Avancer d'une case
        if (pos_x, pos_y + self.direction) not in echiquier:
            mouv.append((pos_x, pos_y + self.direction))
            # Bouger de 2 cases au début

            if (self.couleur == "blanc" and pos_y == 1) or (self.couleur == "noir" and pos_y == 6):
                if (pos_x, pos_y + 2 * self.direction) not in echiquier:
                    mouv.append((pos_x, pos_y + 2 * self.direction))
        return mouv
