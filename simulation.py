
import os
import time
from concurrent.futures import ProcessPoolExecutor, as_completed
from itertools import product
from echec import Echec
from ia import IA

def jouer_partie(args):
    p1, p2 = args
    
    ia1 = IA("blanc", p1)
    ia2 = IA("noir", p2)

    class JeuSilencieux:
        def __init__(self):
            self.plateau = Echec()
            self.gagnant = None
            self.nombre_coups = 0
            self.duree = 0

        def main(self):
            debut_partie = time.time()
            while True:
                for couleur in ["blanc", "noir"]:
                    mouv_dispo = self.plateau.tous_mouv_valides(couleur)
                    

                    if not mouv_dispo:
                        nb_blanc = len(self.plateau.pieces_blanches)
                        nb_noir = len(self.plateau.pieces_noires)
                        
                        if nb_blanc == 0:
                            self.gagnant = "blanc"
                        elif nb_noir == 0:
                            self.gagnant = "noir"
                        elif nb_blanc < nb_noir:
                            self.gagnant = "blanc"
                        elif nb_noir < nb_blanc:
                            self.gagnant = "noir"
                        else:
                            self.gagnant = "match nul"
                        break


                    if couleur == "blanc":
                        mouv = ia1.recup_mouv(self.plateau)
                    else:
                        mouv = ia2.recup_mouv(self.plateau)

                    if mouv is None:
                        self.gagnant = "noir" if couleur == "blanc" else "blanc"
                        break

                    self.plateau.faire_mouv(mouv)
                    self.nombre_coups += 1

                    if self.plateau.partie_terminee():
                        if len(self.plateau.pieces_blanches) == 0:
                            self.gagnant = "blanc"
                        elif len(self.plateau.pieces_noires) == 0:
                            self.gagnant = "noir"
                        else:
                            self.gagnant = "match nul"
                        break
            self.duree = time.time() - debut_partie
            return self.gagnant, self.nombre_coups, self.duree

    jeu = JeuSilencieux()
    jeu.main()
    return (p1, p2, jeu.gagnant, jeu.nombre_coups, jeu.duree)

def generer_resultats(nom_fichier="resultats_tournoi.csv"):
    profondeurs = [1, 2, 3]
    NB_PARTIES = 50

    resultats = {}
    stats_coups = {}
    stats_temps = {}
    
    for p1 in profondeurs:
        for p2 in profondeurs:
            if p1 != p2:
                resultats[(p1, p2)] = {"blanc": 0, "noir": 0, "match nul": 0}
                stats_coups[(p1, p2)] = []
                stats_temps[(p1, p2)] = []

    victoires_par_ia = {p: 0 for p in profondeurs}
    total_par_ia = {p: 0 for p in profondeurs}
    total_coups = 0
    total_temps = 0

    taches = []
    for p1 in profondeurs:
        for p2 in profondeurs:
            if p1 != p2:
                for _ in range(NB_PARTIES):
                    taches.append((p1, p2))

    debut = time.time()
    print(f"Lancement du tournoi avec {len(taches)} parties")
    print(f"Utilisation de {os.cpu_count()} coeurs")

    with ProcessPoolExecutor() as executor:
        futures = [executor.submit(jouer_partie, tache) for tache in taches]

        for future in as_completed(futures):
            try:
                p1, p2, res, coups, duree = future.result()
                resultats[(p1, p2)][res] += 1
                stats_coups[(p1, p2)].append(coups)
                stats_temps[(p1, p2)].append(duree)
                total_coups += coups
                total_temps += duree

                if res == "blanc":
                    victoires_par_ia[p1] += 1
                elif res == "noir":
                    victoires_par_ia[p2] += 1
                    
                total_par_ia[p1] += 1
                total_par_ia[p2] += 1
            except Exception as e:
                print(f"Erreur dans une partie : {e}")

    fin = time.time()

    def generer_rapport_txt(resultats, victoires_par_ia, total_par_ia, winrate, stats_coups, profondeurs, nom_fichier="rapport_tournoi.txt"):
        with open(nom_fichier, "w", encoding="utf-8") as f:

            f.write("=== RESULTATS PAR MATCH (Blanc vs Noir) ===\n")
            f.write("P1 - P2 | Victoires Blanc | Victoires Noir | Matchs Nuls | Coups Moyens\n")
            f.write("-" * 60 + "\n")
            for (p1, p2), valeurs in resultats.items():
                blanc = valeurs["blanc"]
                noir = valeurs["noir"]
                nul = valeurs["match nul"]
                moy_coups = round(sum(stats_coups[(p1, p2)]) / len(stats_coups[(p1, p2)]), 1) if stats_coups[(p1, p2)] else 0
                f.write(f"IA{p1} vs IA{p2} | {blanc:4d} | {noir:4d} | {nul:4d} | {moy_coups:5.1f}\n")
            f.write("\n")

            f.write("=== STATISTIQUES GLOBALES PAR IA ===\n")
            f.write("Profondeur | Victoires | Total matchs | Taux de victoire (%)\n")
            f.write("-" * 50 + "\n")
            for p in profondeurs:
                w = winrate[p]
                v = victoires_par_ia[p]
                t = total_par_ia[p]
                f.write(f"IA{p:1d}        | {v:3d}       | {t:4d}          | {w:5.1f}\n")

    print(f"Rapport texte généré sous le nom '{nom_fichier}'")

    print(f"Temps total : {fin - debut:.2f} secondes")
    print(f"Moyenne de coups par partie : {total_coups // len(taches)}")
    print(f"Moyenne de temps par partie : {total_temps / len(taches):.2f}s")

    return nom_fichier

if __name__ == "__main__":
    fichier_resultats = generer_resultats()
