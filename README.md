![Logo TPG](other/logo_tpg.png)

# Mashups 2026
Practical assignments for the Mashups and Contextualisation  

J'aimerai créer un programme python utilisable dans le terminal qui combine des données sur les arrêts, la fréquentation et les kilomètres parcourus du réseau TPG etc...

## TP1 -> TPG Open Data

### Présentation du projet
L'objectif du TP1 est de développer un programme Python qui utilise au moins 3 fichiers de données distincts (dont au moins un JSON et un XML). J'ai pour ceci choisi d'aller chercher dans les bases de données OpenData des Transports publics genevois (TPG). Mon objectif est de pouvoir analyser les lignes du réseaux à partir des arrêts desservis, de la fréquentation des voyageurs et des km produits. Nous sommes aussi censé présenter 5 scénarios différents et une interface minimale qui s'affiche dans le terminal de l'IDE actuel. 

- Le scénario 1: Fiche d'une ligne TPG qui annoncera plusieurs choses 
- Le scénario 2: 
- Le scénario 3: Quelle ligne desservent le + d'arrets ? 
- Le scénario 4: 
- Le scénario 5: 

### Sources de données

| Fichier | Format | Contenu |
|---|---|---|
| frequentation.json | JSON | Montées et descentes mensuelles par ligne et par arrêt |
| arrets.xml | XML | Arrêts, quais et lignes desservies |
| kilometres.json | JSON | Kilomètres produits on a daily basis par ligne |

Pour faciliter et limiter les données, j'ai décidé que les calculs de fréquentation et de kilomètres sont effectués sur les données uniquement sur l'année 2025.

Sources de mes données: 
1. Pour les arrêts en XML/KML: https://opendata.swiss/fr/dataset/reseau-tpg-arrets1?sort=title-asc
2. Pour les fréquentations en 2025 en JSON: https://opendata.tpg.ch/explore/dataset/montees-mensuelles-par-arret-par-ligne/table/?disjunctive.ligne&disjunctive.ligne_type_act&disjunctive.arret&disjunctive.arret_code_long
3. Pour les km produits journaliers par ligne en 2025: https://opendata.tpg.ch/explore/dataset/kilometres-produits-journaliers-par-ligne/export/?disjunctive.ligne&disjunctive.ligne_type_act&disjunctive.horaire_type&disjunctive.jour_semaine&sort=date&refine.date=2025

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

**Toujours un exemple avec la ligne 5 :**

| Rang | Arrêt | Montées en 2025 |
|---|---|---:|
| 1 | Gare Cornavin | 1 136 811,64 |
| 2 | Genève-Aéroport-Terminal | 563 675,37 |
| 3 | Hôpital | 461 987,32 |
| 4 | Bel-Air | 456 896,02 |
| 5 | Coutance | 339 810,30 |

Le programme affiche aussi les codes des quais et leurs coordonnées GPS quand il arrive à les retrouver dans le XML : )

**Attention :** Enfait, les noms des arrêts ne sont pas toujours écrits de la même manière dans le JSON et le XML. Donc au lieu de les comparer directement par leur nom, j'ai utilisé les codes des quais pour faire la correspondance entre les deux fichiers. Par ex, pour Gare Cornavin, le JSON contient 3 codes : CVIN00, CVIN01 et CVIN03. Mais le programme ne retrouve que CVIN01 et CVIN03 dans le XML. J'ai donc ajouté une vérification pour afficher les codes absents. Et aussi, comme certains arrêts ont plusieurs quais, ils peuvent avoir plusieurs coordonnées GPS.
Enfin, j'ai testé avec la ligne 9999, qui ne possède aucune donnée de fréquentation en 2025 dans mon fichier. Dans ce cas, le programme affiche simplement un message pour prévenir l'utilisateur au lieu de continuer avec un classement vide.

### Scénario 3: Top 10 des lignes TPG avec le plus d'arrêts

Pour ce troisième scénario, j'ai voulu savoir quelles sont les lignes TPG qui desservent le plus d'arrêts. Le programme analyse donc toutes les lignes présentes dans le XML et affiche les 10 premières avec leur fréquentation en 2025.

J'ai combiné 2 fichiers (arrets.xml et frequentation.json) pour :

- Récupérer toutes les lignes présentes dans le XML et les arrêts qu'elles desservent
- Enlever les noms d'arrêts en double avec set(), car un même arrêt peut avoir plusieurs quais
- Compter le nombre de noms d'arrêts distincts pour chaque ligne
- Classer les lignes de celle qui a le plus d'arrêts à celle qui en a le moins
- Afficher uniquement les 10 premières
- Calculer le total des montées en 2025 pour chaque ligne à partir du JSON

**Exemple avec les données TPG :**

| Ligne | Arrêts distincts | Montées en 2025 |
|---|---:|---:|
| 01 | 44 | 6 892 915,82 |
| 20 | 43 | 3 559 197,45 |
| 54 | 43 | 252 972,95 |
| 38 | 43 | 720 297,71 |
| 05 | 39 | 6 375 036,69 |
| A | 37 | Données indisponibles |
| 83 | 35 | 242 246,12 |
| 60 | 35 | 3 180 404,82 |
| 07 | 33 | 5 296 553,26 |
| 09 | 33 | 7 162 498,39 |

Le programme a trouvé 91 lignes différentes dans le XML, mais j'ai décidé d'afficher uniquement les 10 premières pour que le résultat soit plus lisible dans le terminal

**Particularités des données :** Comme dans le scénario 1, les numéros de ligne ne sont pas toujours écrits de la même manière dans les deux fichiers. J'ai donc utilisé zfill(2) pour pouvoir comparer les numéros du JSON avec ceux du XML. J'ai aussi remarqué que certaines lignes présentes dans le XML n'ont pas forcément de données de fréquentation correspondantes dans le JSON. Par exemple, la ligne A possède 37 noms d'arrêts distincts, mais aucune donnée de montées n'a été retrouvée pour 2025. Au lieu d'afficher 0, ce qui pourrait laisser penser que personne n'a utilisé cette ligne, j'ai préféré afficher "Données de fréquentation indisponibles". Finally, les arrêts sont comptés à partir de leurs noms distincts. Cela ne correspond donc pas forcément au nombre exact d'arrêts physiques du réseau.