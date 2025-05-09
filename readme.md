# Projet IA – Jeu d’échecs inversé avec intelligence artificielle

## Objectif

Ce projet, réalisé dans le cadre de l’UE d’Intelligence Artificielle, consiste à développer un jeu d’échecs inversé où le but est de **perdre** la partie. Le jeu intègre une intelligence artificielle (IA) avec plusieurs niveaux de difficulté, permettant à l’utilisateur de s’entraîner contre différents types d’adversaires.

## Fonctionnalités principales

- **Mode de jeu inversé** : l’objectif est de se débarrasser de toutes ses pièces ou de ne plus avoir de coups à jouer.
- **IA adaptative** : plusieurs niveaux de difficulté sont disponibles, ajustant la stratégie de l’IA.
- **Simulation de parties** : possibilité de lancer des tournois entre différentes IA.
- **Rapport de tournoi** : génération d’un rapport détaillant les performances de l’IA sur plusieurs parties.

## Structure du projet

- `echec.py` : définition des règles du jeu et gestion de l’échiquier.
- `ia.py` : implémentation de l’IA avec différents niveaux de difficulté.
- `jeu.py` : boucle principale du jeu, gestion des tours et des interactions.
- `joueur.py` : gestion des actions du joueur humain.
- `simulation.py` : module permettant de réaliser les tournois.
- `rapport_tournoi.txt` : exemple de rapport généré après une série de parties.

## Lancement du jeu

### Prérequis

- Python 3.x installé sur votre machine.

### Installation

1. Clonez le dépôt :
   ```bash
   git clone https://github.com/Foolish111/Projet-IA.git
   cd Projet-IA

2. Lancez le jeu :

    ```bash
    python jeu.py

## Utilisation 

Suivez les indications à l'écran, vous aurez 3 choix, le premier pour faire une partie Homme contre Homme, 
le deuxième pour faire une partie Homme contre machine et enfin pour faire une partie machine contre machine. Si vous séléctionnez un mode avec au moins une machine, il vous faudra donner le niveau de la machine.


## Simulation

1. Pour lancer le tournoi des IA, attention le tournoi devrait prendre environ une heure, en fonction de votre materiel, si vous voulez diminuez ce temps
rendez-vous dans le fichier `ia.py`, et modifiez l'attribut **limite_temps** de la classe **IA**, c'est une valeur en secondes, à noter que plus elle sera basse, plus le temps de recherche des coups sera court certes, mais moins bons seront les coups :

   ```bash
    python simulation.py

## Auteurs

https://github.com/Foolish111

https://github.com/Shrek1515