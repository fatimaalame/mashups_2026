![Logo TPG](other/logo_tpg.png)

# Mashups 2026
Practical assignments for the Mashups and Contextualisation  

J'aimerai créer un programme python utilisable dans le terminal qui combine des données sur les arrêts, la fréquentation et les kilomètres parcourus du réseau TPG etc...

## TP1 -> TPG Open Data

### Présentation du projet
L'objectif du TP1 est de développer un programme Python qui utilise au moins 3 fichiers de données distincts (dont au moins un JSON et un XML). J'ai pour ceci choisi d'aller chercher dans les bases de données OpenData des Transports publics genevois (TPG). Mon objectif est de pouvoir analyser les lignes du réseaux à partir des arrêts desservis, de la fréquentation des voyageurs et des km produits. Nous sommes aussi censé présenter 5 scénarios différents et une interface minimale qui s'affiche dans le terminal de l'IDE actuel. 

- Le scénario 1: fiche d'une ligne TPG 
- Le scénario 2: Top 5 arrêts montés par ligne
- Le scénario 3: Quelle ligne desservent le + d'arrets ? 
- Le scénario 4: Vacances vs horaires normaux 
- Le scénario 5: Recherche d'un arrêt TPG

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

Pour lancer mon programme, il faut juste avoir Python 3 installé. J'ai utilisé uniquement des bibliothèques déjà incluses dans Python, donc normalement il n'y a rien d'autre à installer :)

D'abord, récupérer mon projet sur GitHub : git clone https://github.com/fatimaalame/mashups_2026.git

Puis aller dans le dossier TP1 : cd mashups_2026/TP1

Et enfin lancer : python3 main.py

Là, le menu apparaîtra et il suffira de choisir entre le chiffre 1 et 5 pour tester les différents scénarios. 
(P.s: Les trois fichiers de données sont déjà dans le sous-dossier data, donc pas besoin de télécharger quoi que ce soit d’autre.) 


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

Le programme affiche également les noms des arrêts distincts par ordre alphabétique :)

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
| A | 37 | 1 116 000,14 |
| 83 | 35 | 242 246,12 |
| 60 | 35 | 3 180 404,82 |
| 07 | 33 | 5 296 553,26 |
| 09 | 33 | 7 162 498,39 |

Le programme a trouvé 91 lignes différentes dans le XML, mais j'ai décidé d'afficher uniquement les 10 premières pour que le résultat soit plus lisible dans le terminal

**Particularités des données :** Comme dans le scénario 1, les numéros de ligne ne sont pas toujours écrits de la même manière dans les deux fichiers. J'ai donc utilisé zfill(2) pour pouvoir comparer les numéros du JSON avec ceux du XML. J'ai aussi remarqué que certaines lignes présentes dans le XML n'ont pas forcément de données de fréquentation correspondantes dans le JSON. Par exemple, la ligne A possède 37 noms d'arrêts distincts et 1 116 000,14 montées en 2025. Au début, le programme ne retrouvait pas cette fréquentation à cause de la différence d'écriture des numéros de ligne entre les fichiers. J'ai donc corrigé ce problème avec ma fonction normaliser_ligne(). Finally, les arrêts sont comptés à partir de leurs noms distincts. Cela ne correspond donc pas forcément au nombre exact d'arrêts physiques du réseau.

### Scénario 4: Comparaison des horaires VACANCES et NORMAL

Pour ce 4eme scénario, je voulais voir s'il y avait une vraie différence entre les kilomètres produits pendant les jours avec un horaire normal et ceux avec un horaire vacances. Parce qu'en soit, on pourrait imaginer que les TPG font moins de kilomètres pendant les vacances, mais est-ce que c'est vraiment le cas ? Et surtout, de combien ?

J'ai donc utilisé 2 fichiers (kilometres.json et frequentation.json) pour pouvoir comparer tout ça. En gros, le programme permet à l'utilisateur de choisir une ligne, puis il va chercher les kilomètres produits en 2025. Ensuite, j'ai séparé les données en deux catégories, VACANCES et NORMAL, pour calculer la moyenne des kilomètres produits pour chacune. Au début, je pensais simplement comparer le total des kilomètres, mais enfait ça n'aurait pas été très représentatif, parce qu'il n'y a pas le même nombre de jours dans les deux catégories. Donc j'ai plutôt décidé de calculer une moyenne par jour et ensuite de regarder la différence en pourcentage.

**Par exemple avec la ligne 12 :**

| Indicateur | Ligne 12 |
|---|---:|
| Jours VACANCES | 63 |
| Jours NORMAL | 190 |
| Moyenne VACANCES | 3 717,38 km |
| Moyenne NORMAL | 3 783,96 km |
| Différence | 66,58 km |
| Diminution | 1,76 % |
| Montées en 2025 | 21 018 435,15 |

Ce que je trouve intéressant, c'est que pour la ligne 12, on voit une diminution des kilomètres produits pendant les jours VACANCES, même si elle est assez faible : seulement 1,76 %. Et puisque la ligne 12 passe par Battelle, où se trouve notre cher CUI, je me suis dit que cette petite diminution était peut-être due aux étudiants qui ne viennent plus en cours pendant les vacances. Comme quoi, nos vacances font peut-être aussi du bien aux TPG :) Bon, évidemment, ce n'est qu'une hypothèse. Les chiffres concernent les kilomètres produits, pas directement le nb de voyageurs. 

De plus, j'ai remarqué que le fichier kilometres.json ne contient pas uniquement les catégories VACANCES et NORMAL. J'ai donc choisi de garder seulement ces deux types d'horaires pour ma comparaison. J'ai aussi fait attention à calculer une moyenne par jour, plutôt que par enregistrement, pour éviter de fausser les résultats si une même date apparaît plusieurs fois. Enfin, j'ai utilisé la ligne 12 comme exemple, pour pouvoir comparer les deux horaires et voir si la différence était vraiment importante.


### Scénario 5 : Recherche d'un arrêt TPG
Pour ce dernier scénario, j'ai voulu faire un peu l'inverse du scénario 1. Au lieu de chercher une ligne TPG et de voir quels arrêts elle dessert, je voulais permettre à l'utilisateur de rechercher directement un arrêt par son nom et d'obtenir des informations dessus. J'ai donc combiné 2 fichiers (arrets.xml et frequentation.json). Le programme cherche d'abord le nom de l'arrêt dans le XML, puis affiche les différents quais, leurs coordonnées GPS et les lignes qui les desservent. Ensuite, il utilise les codes des quais pour retrouver dans le JSON le total des montées en 2025, toutes lignes confondues.

**Exemple avec l'arrêt Battelle :**

| Indicateur | Résultat |
|---|---|
| Arrêt trouvé | Carouge GE, Battelle |
| Nombre de quais | 1 |
| Code du quai | BALE00 |
| Ligne desservant l'arrêt | 41 |
| Total des montées en 2025 | 1 184,97 |

Pour cet exemple, j'ai choisi l'arrêt Battelle, histoire de rester dans le thème du CUI ! Mon programme a retrouvé un seul quai (BALE00), desservi par la ligne 41, avec un total de 1 184,97 montées en 2025. Le programme affiche également les coordonnées GPS du quai. Et comme il suffit d'écrire « Battelle » pour retrouver « Carouge GE, Battelle », l'utilisateur n'a pas forcément besoin de connaître le nom complet de l'arrêt.

**Particularités des données :**

J'ai remarqué que les noms des arrêts ne sont pas forcément écrits de la même manière dans le JSON et dans le XML. Du coup, pour faire la correspondance entre les deux fichiers, j'ai utilisé les codes des quais plutôt que les noms. J'ai aussi prévu le cas où l'utilisateur recherche un arrêt qui n'existe pas, ou ne saisit aucun nom. Dans ce cas, le programme affiche un message et revient au menu principal au lieu de continuer avec des résultats vides. Enfin, la recherche fonctionne même si l'utilisateur n'écrit pas exactement le nom complet de l'arrêt. Par exemple, écrire « Battelle » permet de retrouver « Carouge GE, Battelle ». Par contre, si la recherche est trop générale, le programme peut retrouver plusieurs arrêts différents et additionner leurs montées.




### Conclusion
Ce TP m’a permis de comprendre que la diﬃculté ne réside pas uniquement dans la
programmation, mais aussi dans la manière dont on exploite et interprète les données. En
travaillant avec trois sources diﬀérentes, j’ai été confrontée à plusieurs problèmes de
correspondance, de cohérence et de traitement des données. J’ai notamment appris qu’obtenir
un résultat ne suﬃt pas. Encore faut-il comprendre ce qu’il représente et s’assurer qu’il est
pertinent. Au-delà des cinq scénarios réalisés, ce projet m’a surtout appris à questionner mes
résultats, à identifier mes erreurs et à améliorer progressivement mon programme. Finalement, ce
que je retiens de ce TP, c’est qu’un programme qui fonctionne n’est pas nécessairement un
programme qui donne du sens aux données. Et c’est justement cette distinction qui m’a le plus
appris.

### Utilisation d'un LLM
J'ai utilisé les LLMs pour m'aider à comprendre et combiner mes fichiers JSON et XML, corriger mes
erreurs Python (et il y en a eu pas mal !), vérifier mes résultats et m'assurer que mes solutions
correspondaient au niveau attendu pour ce TP. Elle m'a aussi beaucoup aidée à structurer et
reformuler ma documentation, notamment le README et certaines parties de ce rapport, tout en
gardant mes propres explications et observations. J'ai tenu à eﬀectuer les corrections moi-même,
étape par étape pour comprendre ce que je faisais plutôt que de simplement reprendre du code
généré. Les outils que j’ai utilisé sont GPT-5.5 Thinking (OpenAI) et Claude Sonnet 5.5 (Anthropic).

### Sources utilisées pour le main.py
- Documentation du module JSON: https://docs.python.org/fr/3/library/json.html [consulté le
24.10.26]
- Documentation du module ElementTree: https://docs.python.org/fr/3/library/
xml.etree.elementtree.html [consulté le 24.10.26]
- Pour la structure de données: https://docs.python.org/fr/3/tutorial/datastructures.html [consulté
[24.10.26]
- Pour le path: https://docs.python.org/fr/3/library/pathlib.html [consulté le 24.10.26]
- Pour les fonctions pour mes chaines de caractères: https://docs.python.org/fr/3/library/
stdtypes.html#text-sequence-type-str [consulté le 24.10.26]
- Pour les fichiers XML: https://docs.python.org/fr/3/library/xml.etree.elementtree.html [consulté
le 25.10.26]
- Pour la normalisation: https://www.geeksforgeeks.org/python/python-string-zfill/ [consulté le
27.10.26]
- Pour le set ( ) : https://www.geeksforgeeks.org/python/python-set-function/ [consulté le
27.10.26]