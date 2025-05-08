import os
import time
from concurrent.futures import ProcessPoolExecutor, as_completed
from itertools import product

from echec import Echec
from ia import IA
from ia import IAFacile, IAMoyenne, IADifficile

def determiner_gagnant(plateau):
    blanc = len(plateau.pieces_blanches)
    noir = len(plateau.pieces_noires)

    if blanc == 0:
        return "blanc"
    elif noir == 0:
        return "noir"
    elif blanc < noir:
        return "blanc"
    elif noir < blanc:
        return "noir"
    else:
        return "match nul"
    
def jouer_partie(args):
    IAs = {"1": IAFacile, "2": IAMoyenne, "3": IADifficile}
    p1, p2 = args


    ia1 = IAs[p1]("blanc")
    ia2 = IAs[p2]("noir")

    #ia1 = IA("blanc", p1)
    #ia2 = IA("noir", p2)

    def simulate():
        plateau = Echec()
        nombre_coups = 0
        MAX_COUPS = 300
        debut = time.time()
        coups_sans_capture = 0

        while nombre_coups < MAX_COUPS:
            t1_blanc = len(plateau.pieces_blanches)
            t1_noir = len(plateau.pieces_noires)
            for couleur in ["blanc", "noir"]:
                mouv_dispo = plateau.tous_mouv_valides(couleur)
                if not mouv_dispo:
                    return determiner_gagnant(plateau), nombre_coups, time.time() - debut

                mouv = ia1.recup_mouv(plateau) if couleur == "blanc" else ia2.recup_mouv(plateau)
                if mouv is None:
                    return "noir" if couleur == "blanc" else "blanc", nombre_coups, time.time() - debut

               
                plateau.faire_mouv(mouv)
                nombre_coups += 1

                t2_blanc = len(plateau.pieces_blanches)
                t2_noir = len(plateau.pieces_noires)

                if t2_blanc < t1_blanc or t2_noir < t1_noir:
                    coups_sans_capture = 0
                else:
                    coups_sans_capture += 1


                if plateau.partie_terminee():

                    return determiner_gagnant(plateau), nombre_coups, time.time() - debut

                if coups_sans_capture >= 50:
                    return determiner_gagnant(plateau), nombre_coups, time.time() - debut

        return "match nul", nombre_coups, time.time() - debut

    return (p1, p2, *simulate())

def generer_resultats(nom_fichier="rapport_tournoi.txt"):
    profondeurs = ["1", "2", "3"]
    NB_PARTIES_PAR_COUPLE = 1
    NB_COUPLES = len(profondeurs) * (len(profondeurs) - 1)
    NB_PARTIES_TOTAL = NB_PARTIES_PAR_COUPLE * NB_COUPLES

    resultats = {(p1, p2): {"blanc": 0, "noir": 0, "match nul": 0} for p1 in profondeurs for p2 in profondeurs if p1 != p2}
    stats_coups = {(p1, p2): [] for p1 in profondeurs for p2 in profondeurs if p1 != p2}
    stats_temps = {(p1, p2): [] for p1 in profondeurs for p2 in profondeurs if p1 != p2}

    victoires_par_ia = {p: 0 for p in profondeurs}
    total_par_ia = {p: 0 for p in profondeurs}
    total_coups = 0
    total_temps = 0

    taches = []
    for p1 in profondeurs:
        for p2 in profondeurs:
            if p1 != p2:
                taches.extend([(p1, p2)] * NB_PARTIES_PAR_COUPLE)

    print(f"Lancement du tournoi avec {len(taches)} parties")
    print(f"Utilisation de {os.cpu_count()} coeurs")

    debut_total = time.time()
    parties_completes = 0

    with ProcessPoolExecutor(max_workers=os.cpu_count()) as executor:
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

                parties_completes += 1
                print(f"Parties jouées : {parties_completes}/{len(taches)}")

            except Exception as e:
                print(f"Erreur dans une partie : {e}")

    fin_total = time.time()

    def generer_rapport(resultats, victoires_par_ia, total_par_ia, stats_coups, stats_temps, profondeurs):
        with open("rapport_tournoi.txt", "w", encoding="utf-8") as f:
            f.write("=== RÉSULTATS PAR MATCH (Blanc vs Noir) ===\n")
            f.write("P1 - P2 | Victoires Blanc | Victoires Noir | Matchs Nuls | Coups Moyens | Durée Moyenne (s)\n")
            f.write("-" * 80 + "\n")
            for (p1, p2), valeurs in resultats.items():
                blanc = valeurs["blanc"]
                noir = valeurs["noir"]
                nul = valeurs["match nul"]
                moy_coups = round(sum(stats_coups[(p1, p2)]) / len(stats_coups[(p1, p2)]), 1) if stats_coups[(p1, p2)] else 0
                moy_temps = round(sum(stats_temps[(p1, p2)]) / len(stats_temps[(p1, p2)]), 2) if stats_temps[(p1, p2)] else 0
                f.write(f"IA{p1} vs IA{p2} | {blanc:4d} | {noir:4d} | {nul:4d} | {moy_coups:5.1f} | {moy_temps:6.2f}\n")
            f.write("\n")

            f.write("=== STATISTIQUES GLOBALES PAR IA ===\n")
            f.write("Profondeur | Victoires | Total matchs | Taux de victoire (%)\n")
            f.write("-" * 50 + "\n")
            for p in profondeurs:
                v = victoires_par_ia[p]
                t = total_par_ia[p]
                taux_victoire = round((v / t) * 100, 1) if t > 0 else 0
                f.write(f"IA{p}        | {v:3d}       | {t:4d}          | {taux_victoire:5.1f}\n")

        print("Rapport généré sous le nom 'rapport_tournoi.txt'")

    generer_rapport(resultats, victoires_par_ia, total_par_ia, stats_coups, stats_temps, profondeurs)

    print(f"Temps total : {fin_total - debut_total:.2f} secondes")
    print(f"Moyenne de coups par partie : {total_coups // len(taches)}")
    print(f"Moyenne de temps par partie : {total_temps / len(taches):.2f}s")

    return nom_fichier

if __name__ == "__main__":
    fichier_resultats = generer_resultats()