# simulation.py

import os
import time
import csv
from concurrent.futures import ProcessPoolExecutor, as_completed
from itertools import product
import matplotlib.pyplot as plt
import pandas as pd
from echec import Echec
from ia import IA

def jouer_partie(args):
    """Simule une partie entre deux IA de profondeurs p1 (blanc) et p2 (noir)"""
    p1, p2 = args
    
    # Initialisation des IA
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
                    
                    # Gestion du pat et fin de partie
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

                    # Récupération du coup avec tri par captures d'abord
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

    # Initialisation des compteurs
    resultats = {}
    stats_coups = {}
    stats_temps = {}
    
    for p1 in profondeurs:
        for p2 in profondeurs:
            resultats[(p1, p2)] = {"blanc": 0, "noir": 0, "match nul": 0}
            stats_coups[(p1, p2)] = []
            stats_temps[(p1, p2)] = []

    victoires_par_ia = {p: 0 for p in profondeurs}
    total_par_ia = {p: 0 for p in profondeurs}
    total_coups = 0
    total_temps = 0

    # Génération des tâches
    taches = []
    for p1 in profondeurs:
        for p2 in profondeurs:
            for _ in range(NB_PARTIES):
                taches.append((p1, p2))

    # Lancement du tournoi
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

    # Calcul des winrates
    winrate = {
        p: round(victoires_par_ia[p] / total_par_ia[p] * 100, 2) if total_par_ia[p] > 0 else 0
        for p in profondeurs
    }

    # Génération du CSV
    with open(nom_fichier, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        
        # Section détaillée par paire d'IA
        writer.writerow([
            "Profondeur Blanc", "Profondeur Noir",
            "Victoires Blanc", "Victoires Noir", "Matchs Nuls",
            "Durée Moyenne (coups)", "Temps Moyen (s)"
        ])

        for (p1, p2), valeurs in resultats.items():
            moy_coups = round(sum(stats_coups[(p1, p2)]) / len(stats_coups[(p1, p2)]) if stats_coups[(p1, p2)] else 0, 1)
            temps_moyen = round(sum(stats_temps[(p1, p2)]) / len(stats_temps[(p1, p2)]) if stats_temps[(p1, p2)] else 0, 2)
            writer.writerow([
                p1, p2,
                valeurs["blanc"], valeurs["noir"], valeurs["match nul"],
                moy_coups, temps_moyen
            ])

        # Statistiques globales
        writer.writerow([])
        writer.writerow(["Statistiques Globales"])
        writer.writerow(["Profondeur", "Victoires", "Total", "% Victoire", "Temps Total (s)"])
        for p in profondeurs:
            writer.writerow([p, victoires_par_ia[p], total_par_ia[p], winrate[p], round(sum(stats_temps[(p, p2)] for p2 in profondeurs), 2)])

    print(f"\n✅ Résultats sauvegardés dans '{nom_fichier}'")
    print(f"Temps total : {fin - debut:.2f} secondes")
    print(f"Moyenne de coups par partie : {total_coups // len(taches)}")
    print(f"Moyenne de temps par partie : {total_temps / len(taches):.2f}s")

    return nom_fichier

def analyser_resultats(nom_fichier="resultats_tournoi.csv"):
    """Génère des graphiques à partir du CSV"""
    df = pd.read_csv(nom_fichier)
    
    # Filtrage des données
    details = df[~df["Statistiques Globales"].astype(str).str.contains("nan")]
    stats_globales = df[df["Statistiques Globales"].astype(str).str.contains("Statistiques Globales")].iloc[0]
    
    # 1. Heatmap des victoires
    heatmap_data = details.pivot(index="Profondeur Blanc", columns="Profondeur Noir", values="Victoires Blanc")
    plt.figure(figsize=(6, 5))
    sns.heatmap(heatmap_data, annot=True, fmt="d", cmap="viridis")
    plt.title("Victoires du Blanc par profondeur IA")
    plt.xlabel("Profondeur Noir")
    plt.ylabel("Profondeur Blanc")
    plt.tight_layout()
    plt.savefig("victoires_heatmap.png")
    plt.close()

    # 2. Bar chart des winrates
    df_stats = df[df["Statistiques Globales"].astype(str).str.contains("Statistiques Globales", na=False)]
    df_stats = df_stats.iloc[1:].copy()
    df_stats["Profondeur"] = df_stats["Profondeur"].astype(int)
    
    plt.figure(figsize=(8, 5))
    plt.bar(df_stats["Profondeur"], df_stats["% Victoire"])
    plt.title("Taux de victoire par profondeur")
    plt.xlabel("Profondeur")
    plt.ylabel("% Victoire")
    plt.xticks(df_stats["Profondeur"])
    plt.tight_layout()
    plt.savefig("winrate_bar_chart.png")
    plt.close()

    # 3. Boxplot des durées de parties
    durations = []
    for (p1, p2), coups in stats_coups.items():
        durations.extend([{"Profondeur Blanc": p1, "Profondeur Noir": p2, "Durée": d} for d in stats_temps[(p1, p2)]])
    
    df_durations = pd.DataFrame(durations)
    plt.figure(figsize=(10, 6))
    sns.boxplot(x="Profondeur Blanc", y="Durée", hue="Profondeur Noir", data=df_durations)
    plt.title("Distribution des durées des parties par profondeur")
    plt.xlabel("Profondeur Blanc")
    plt.ylabel("Durée (s)")
    plt.legend(title="Profondeur Noir")
    plt.tight_layout()
    plt.savefig("durees_boxplot.png")
    plt.close()

if __name__ == "__main__":
    fichier_resultats = generer_resultats()
    analyser_resultats(fichier_resultats)
    print("Graphiques générés : victoires_heatmap.png, winrate_bar_chart.png, durees_boxplot.png")