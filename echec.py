cardinaux_echec = [(1, 0), (0, 1), (-1, 0), (0, -1)]
diagonales_echec = [(1, 1), (-1, 1), (1, -1), (-1, -1)]

def coords_vers_notation(pos):
    """Convertit des coordonnées (x, y) en notation d'échecs (ex: (4, 3) -> 'e4')."""
    x, y = pos
    lettre = chr(x + ord('a'))  # Convertit 0 -> 'a', 1 -> 'b', ..., 7 -> 'h'
    chiffre = str(y + 1)        # Ajoute 1 car les rangées vont de 1 à 8
    return lettre + chiffre

def notation_vers_coords(notation):
    """Convertit une notation d'échecs (ex: 'e4') en coordonnées (x, y)."""
    if len(notation) != 2 or not notation[0].isalpha() or not notation[1].isdigit():
        raise ValueError("Format de position invalide.")
    
    lettre, chiffre = notation[0].lower(), notation[1]
    x = ord(lettre) - ord('a')  # Convertit 'a' -> 0, 'b' -> 1, ..., 'h' -> 7
    y = int(chiffre) - 1        # Soustrait 1 car les rangées vont de 0 à 7
    
    if not (0 <= x < 8 and 0 <= y < 8):
        raise ValueError("Coordonnées hors limites.")
    
    return (x, y)

class Echec:
    def __init__(self):
        self.tour = "blanc"
        self.echiquier = {}
        self.placer_pieces()
        self.main()

    def placer_pieces(self):
        for i in range(8):
            self.echiquier[(i, 1)] = Pion("blanc", "P", (i, 1), 1)
            self.echiquier[(i, 6)] = Pion("noir", "P", (i, 6), -1)

        pieces = [Tour, Cavalier, Fou, Reine, Roi, Fou, Cavalier, Tour]
        noms = ["R", "N", "B", "Q", "K", "B", "N", "R"]

        for i in range(8):
            self.echiquier[(i, 0)] = pieces[i]("blanc", noms[i], (i, 0))
            self.echiquier[(i, 7)] = pieces[i]("noir", noms[i], (i, 7))

    def afficher_echiquier(self):
        print("  a b c d e f g h")
        for y in range(7, -1, -1):
            print(y + 1, end=" ")
            for x in range(8):
                piece = self.echiquier.get((x, y), " ")
                print(piece, end=" ")
            print()

    def peut_capturer(self, echiquier, couleur):
        """Vérifie si un joueur peut capturer une pièce."""
        for pos, piece in echiquier.items():
            if piece.couleur == couleur:
                for mouv in piece.mouvements_dispo(*piece.position, echiquier, couleur):
                    if mouv in echiquier and echiquier[mouv].couleur != couleur:
                        return True
        return False

    def partie_terminee(self):
        """Vérifie si la partie est terminée selon les règles de l'antichess."""
        blanc, noir = False, False
        for piece in self.echiquier.values():
            if piece.couleur == "blanc":
                blanc = True
            elif piece.couleur == "noir":
                noir = True
        if not blanc:
            print("Le joueur noir a gagné !")
            return True
        if not noir:
            print("Le joueur blanc a gagné !")
            return True
        return False

    def main(self):
        while True:
            self.afficher_echiquier()
            
            # Demander la position de départ en notation d'échecs
            pos = input(f"Au tour des {self.tour}s. Position de la pièce à bouger ? (ex: e2) ")
            try:
                pos_piece = notation_vers_coords(pos)  # Conversion en coordonnées (x, y)
                piece = self.echiquier.get(pos_piece)
                if piece is None or piece.couleur != self.tour:
                    print("Position invalide ou ce n'est pas votre pièce.")
                    continue
            except ValueError:
                print("Format de position invalide. Veuillez entrer une position valide (ex: e2).")
                continue

            # Demander la position cible en notation d'échecs
            nouvelle_pos_notation = input("Nouvelle position ? (ex: e4) ")
            try:
                nouvelle_pos = notation_vers_coords(nouvelle_pos_notation)  # Conversion en coordonnées (x, y)
            except ValueError:
                print("Format de position invalide. Veuillez entrer une position valide (ex: e4).")
                continue

            # Valider le mouvement
            if piece.mouvement_valide(nouvelle_pos, self.echiquier):
                # Vérifier si une capture est obligatoire dans l'antichess
                if self.peut_capturer(self.echiquier, self.tour) and (
                    nouvelle_pos not in self.echiquier or self.echiquier[nouvelle_pos].couleur == piece.couleur
                ):
                    print("Vous devez capturer une pièce si possible.")
                    continue

                # Effectuer le mouvement
                self.echiquier[nouvelle_pos] = piece
                del self.echiquier[pos_piece]
                piece.position = nouvelle_pos

                # Changer de tour
                self.tour = "noir" if self.tour == "blanc" else "blanc"

            else:
                print("Mouvement impossible.")

            # Vérifier si la partie est terminée
            if self.partie_terminee():
                break

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
        if posfin in self.mouvements_dispo(self.position[0], self.position[1], echiquier, couleur=self.couleur):
            return True
        return False

    def mouvements_dispo(self, pos_x, pos_y, echiquier, couleur):
        print("pas de mouvements dispo pour pièce générale")
        return None

    def pos_valide(self, pos):
        if pos[0] < 8 and pos[0] >= 0 and pos[1] < 8 and pos[1] >= 0:
            return True
        return False

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
            if self.pos_sans_conflit(echiquier, couleur, (pos_x + dx, pos_y + self.direction)):
                mouv.append((pos_x + dx, pos_y + self.direction))
        # Avancer d'une case
        if (pos_x, pos_y + self.direction) not in echiquier:
            mouv.append((pos_x, pos_y + self.direction))
            # Double pas initial
            if (self.couleur == "blanc" and pos_y == 1) or (self.couleur == "noir" and pos_y == 6):
                if (pos_x, pos_y + 2 * self.direction) not in echiquier:
                    mouv.append((pos_x, pos_y + 2 * self.direction))
        return mouv

Echec()

