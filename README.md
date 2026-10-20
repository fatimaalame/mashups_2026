![Logo TPG](other/logo_tpg.png)

# Mashups 2026
Practical assignments for the Mashups and Contextualisation  

J'aimerai créer un programme python utilisable dans le terminal qui combine des données sur les arrêts, la fréquentation et les kilomètres parcourus du réseau TPG etc...

## TP1 -> TPG Open Data

### Présentation du projet
L'objectif du TP1 est de développer un programme Python qui utilise au moins 3 fichiers de données distincts (dont au moins un JSON et un XML). J'ai pour ceci choisi d'aller chercher dans les bases de données OpenData des Transports publics genevois (TPG). Mon objectif est de pouvoir analyser les lignes du réseaux à partir des arrêts desservis, de la fréquentation des voyageurs et des km produits. Nous sommes aussi censé présenter 5 scénarios différents et une interface minimale qui s'affiche dans le terminal de l'IDE actuel. 

- Le scénario 1: Fiche d'une ligne TPG qui annoncera plusieurs choses 
- Le scénario 2: 
- Le scénario 3:
- Le scénario 4: 
- Le scénario 5: 

### Sources de données

| Fichier | Format | Contenu |
|---|---|---|
| frequentation.json | JSON | Montées et descentes mensuelles par ligne et par arrêt |
| arrets.xml | XML | Arrêts, quais et lignes desservies |
| kilometres.json | JSON | Kilomètres produits on a daily basis par ligne |

Pour faciliter et limiter les données, j'ai décidé que les calculs de fréquentation et de kilomètres sont effectués sur les données uniquement sur l'année 2025.

### Comment executer ? 

Le programme utilise Python 3 et uniquement des bibliothèques standard (json, pathlib, xml.etree.ElementTree).

Depuis le dossier TP1, exécuter sur votre IDE :

->    python3 main.py

### Scénario 1: Fiche d'une ligne TPG

Ici, je permet à l'utilisateur de saisir un numéro de ligne et d'obtenir plusieurs informations à son sujet.

Donc en gros, j'ai combiné les 3 fichiers pour:

- Calculer le total des montées et descentes en 2025
- Identifier les arrêts desservis par la ligne
- Supprimer les noms d'arrêts en double
- Et enfin, calculer le total des kilomètres produits en 2025

**Exemple avec la ligne 5 :**

| Indicateur | Résultat |
|---|---:|
| Enregistrements de fréquentation | 789 |
| Montées en 2025 | 6 375 036,69 |
| Descentes en 2025 | 6 375 369,14 |
| Entrées XML correspondant à la ligne | 66 |
| Noms d'arrêts distincts | 39 |
| Enregistrements kilométriques | 365 |
| Kilomètres produits en 2025 | 845 670,80 km |

Le programme affiche également les noms des arrêts distincts par ordre alphabétique : )

**Particularités des données :** Enfait, les numéros de ligne ne sont pas toujours écrits de la même manière dans les fichiers ("5" en JSON et "05" en XML), ce qui est un problème. Donc j'ai utilisé  "zfill(2)" pour gérer tout ça. Et aussi, le nombre de noms distincts ne correspond pas nécessairement au nombre exact d'arrêts physiques, donc je les ai aussi enlevés (les doublons).

### Scénario 2: Top 5 des arrêts les plus fréquentés d'une ligne TPG

Pour ce deuxième scénario, j'ai décidé de permettre à l'utilisateur de saisir un numéro de ligne et de voir les 5 arrêts où il y a eu le + de montées en 2025.

J'ai du coup combiné 2 fichiers (frequentation.json et arrets.xml) pour :

- Récupérer tous les arrêts de la ligne choisie et additionner leurs montées sur l'année 2025
- Classer les arrêts du plus fréquenté au moins fréquenté
- Afficher uniquement les 5 premiers
- Récupérer les codes des quais de ces arrêts dans le JSON
- Chercher ces mêmes codes dans le XML pour retrouver leurs coordonnées GPS
- Signaler les codes qui n'ont pas été retrouvés dans le XML

**Exemple avec la ligne 5 :**

| Rang | Arrêt | Montées en 2025 |
|---|---|---:|
| 1 | Gare Cornavin | 1 136 811,64 |
| 2 | Genève-Aéroport-Terminal | 563 675,37 |
| 3 | Hôpital | 461 987,32 |
| 4 | Bel-Air | 456 896,02 |
| 5 | Coutance | 339 810,30 |

Le programme affiche aussi les codes des quais et leurs coordonnées GPS quand il arrive à les retrouver dans le XML : )

**Attention :** Enfait, les noms des arrêts ne sont pas toujours écrits de la même manière dans le JSON et le XML. Donc au lieu de les comparer directement par leur nom, j'ai utilisé les codes des quais pour faire la correspondance entre les deux fichiers.

Par ex, pour Gare Cornavin, le JSON contient 3 codes : CVIN00, CVIN01 et CVIN03. Mais le programme ne retrouve que CVIN01 et CVIN03 dans le XML. J'ai donc ajouté une vérification pour afficher les codes absents.

Et aussi, comme certains arrêts ont plusieurs quais, ils peuvent avoir plusieurs coordonnées GPS.

Enfin, j'ai testé avec la ligne 9999, qui ne possède aucune donnée de fréquentation en 2025 dans mon fichier. Dans ce cas, le programme affiche simplement un message pour prévenir l'utilisateur au lieu de continuer avec un classement vide.