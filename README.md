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
 -------------------------------------------------

## TP2: utiliser une API 

### Partie 1 : Régulation de la luminosité

### Objectif
Ici, je devais réguler automatiquement une ampoule en fonction de la luminosité ambiante (en utilisant une API REST). D'ailleurs, le programme cherche à maintenir une luminosité de 200 lux.

### Le fonctionnement
Mon programme:
 1. récupère la luminosité du capteur avec GET
 2. Calcule l'intensité de l'ampoule en fonction de la luminosité mesurée
 3. Envoie la nouvelle intensité à l'ampoule avec PUT
 4. Enregistre la date + luminosité + l'intensité ds un fichier JSON
 5. Répète ces opérations 10 fois avec intervalle de 30 secondes

Juste, si la luminosité >= 200 lux, l'ampoule reçoit la val 0. Sinon, son intensité est calculée avec la formule : round(((200 - luminosite) / 200) * 99) (donnée en cours)

### Technologies utilisées 
- Python
- Bibliothèque requests + json + datetime + time

J'ai utilisé ces biblio pour pouvoir communiquer avec l'API REST, enregistrer les mesures, save les dates et les heures et enfin pour attendre (par ex pour écrire time.sleep(30)) 

### Exécution
Le programme se trouve dans TP2/Partie1/Part1.py. Par contre, faut avoir une connexion au VPN de l'UNIGE pour accéder à l'API privée.
Pour installer la biblio, il faut faire (pip install requests), et ensuite depuis la racine du dépots, faut lancer python3 TP2/Partie1/Part1.py

### Résultats
Enfait, à chaque fois qu'on execute, ça va créer un fichier JSON dans le dossier TP2/Partie1. Et j'ai fais en sorte que le nom du fichier a la date et l'heure de la session (pour garder les results des diff executions). De plus, les mesures sont à chaque fois sauvegardées progressivement pour ne pas avoir une perte de données (si ça s'interrompt). J'aimerai rajouter aussi que mon programme crée automatiquement un nouveau fichier json dans le dossier TP2/Partie1/my_measures. 
J'ai aussi effectué plusieurs sessions à diff moments de la journée (entre le 16 et 17.11.2026). Et ils montrent que l'intensité de l'ampoule varie avec la luminosité ambiante. 

### Gestion des erreurs
J'ai utilisé try et except pour détecter les erreurs de comm avec l'API. Et si y'a une erreur réseau, il y aura un message qui s'affiche et le programme va continuer avec la tentative d'après. 

--- 

## Partie 2: Analyse des arrêts TPG 

### 1. objectif
Pour cette deuxième partie, il fallait choisir une API existante et créer un programme Python qui permet à l'utilisateur d'entrer quelque chose et de récupérer des résultats à partir de cette entrée. Les résultats devaient aussi être enregistrés dans des fichiers JSON ou XML. Du coup j'ai choisi de travailler avec les données des TPG, parce que c'est quelque chose qu'on utilise à Genève et je trouvais ça intéressant de pouvoir récupérer des informations sur les arrêts. J'ai décidé de faire deux scénarios différents. Le premier permet de connaître la fréquentation d'un arrêt, et le deuxième permet de rechercher tous les arrêts qui commencent par une certaine lettre.

### 2. API utilisée
J'ai utilisé l'API TPG Open Data, qui est disponible sur le site opendata.tpg.ch. Elle donne accès à plusieurs jeux de données sur les transports publics genevois. Pour mon premier scénario, j'ai utilisé deux jeux de données de cette même API. Le premier s'appelle `arrets` et il permet de retrouver les codes associés aux noms des arrêts. Le deuxième, `montees-par-arret-par-ligne`, contient les données sur les montées et les descentes. Pour mon deuxième scénario, j'ai seulement utilisé le jeu de données `arrets`, puisque je voulais récupérer les noms des arrêts. J'ai utilisé la bibliothèque `requests` pour envoyer les requêtes GET, `json` pour sauvegarder mes résultats et `os` pour créer les dossiers automatiquement.

### 3. Fonctionnement du programme
J'ai commencé par créer un menu principal pour que l'utilisateur puisse choisir entre mes deux scénarios. Pour ça, j'ai utilisé une fonction `main()` avec une boucle `while`. Tant que l'utilisateur ne choisit pas 0, il peut continuer à faire des recherches. J'ai ensuite séparé mes deux scénarios dans deux fonctions : `analyser_frequentation()` et `rechercher_par_lettre()`. Pour le premier scénario, l'utilisateur entre le nom d'un arrêt TPG, par exemple Gare Cornavin. Le programme commence par rechercher son nom dans l'API pour récupérer ses codes. En fait, j'ai remarqué qu'un même arrêt pouvait avoir plusieurs codes, donc je devais tous les récupérer pour avoir les données qui lui correspondent. Ensuite, j'utilise ces codes pour envoyer une deuxième requête et récupérer les montées et les descentes du 7 février 2026. Je fais la somme des valeurs et je calcule aussi les pourcentages. Puis je compare les montées et les descentes avec `if`, `elif` et `else` pour afficher si l'arrêt est plutôt un lieu de départ ou d'arrivée. Pour le deuxième scénario, l'utilisateur entre juste une lettre, par exemple B. Le programme recherche les noms des arrêts qui commencent par cette lettre. J'ai utilisé une boucle `while` avec `offset` parce que l'API peut renvoyer au maximum 100 résultats par requête. Donc si j'ai plus de 100 résultats, le programme continue à récupérer les suivants. J'ai aussi fait en sorte de ne pas afficher plusieurs fois le même nom d'arrêt et de classer les résultats par ordre alphabétique.


### 4. l'execution
Pour exécuter mon programme, il faut avoir installé la bibliothèque `requests` avec `pip install requests`. Contrairement à la première partie, je n'ai pas besoin de me connecter au réseau UNIGE ou au VPN, puisque l'API TPG Open Data est accessible publiquement. Depuis la racine de mon dépôt GitHub, je peux donc lancer `python3 TP2/Partie2/Part2.py`. Le programme affiche ensuite le menu. Je peux choisir 1 pour analyser un arrêt, 2 pour faire une recherche alphabétique, ou 0 pour quitter.

### 5. Résultats + observation
J'ai choisi d'enregistrer les résultats de mes deux scénarios dans deux dossiers différents pour ne pas tout mélanger. Pour le premier scénario, les fichiers sont enregistrés dans `TP2/Partie2/my_results`. Chaque fichier contient le nom de l'arrêt, ses codes, la date des données, le total des montées et descentes et leurs pourcentages. J'ai fait six tests différents : Battelle, Carouge-Rondeau, Gare Cornavin, Guye, Plainpalais et Uni-mail. Ce que j'ai trouvé intéressant, c'est qu'il y a vraiment de grandes différences entre les arrêts. Par exemple, pour Gare Cornavin j'ai obtenu 50 792,18 montées et 49 001,53 descentes. Donc dans les données récupérées, cet arrêt est plutôt un lieu de départ, mais la différence reste assez faible. Par contre pour Battelle, j'ai obtenu seulement 2,73 montées contre 32,76 descentes. Ça correspond à environ 92 % de descentes. Je trouvais ça assez surprenant, surtout par rapport aux résultats des autres arrêts. Il faut quand même préciser que mes données concernent le samedi 7 février 2026, donc je ne peux pas dire que les arrêts se comportent toujours comme ça les autres jours.

Pour mon deuxième scénario, les résultats sont enregistrés dans le dossier `TP2/Partie2/results_letter`. J'ai fait sept tests avec les lettres B, F, H, L, Q, X et Z. Par exemple, pour la lettre B, j'ai trouvé 131 noms d'arrêts différents, et pour L j'en ai trouvé 172. Par contre, pour la lettre Q, il y avait seulement 3 arrêts et pour X, aucun résultat. J'ai trouvé ce dernier test intéressant parce que même quand aucun arrêt n'est trouvé, le programme fonctionne et crée quand même un fichier JSON avec une liste vide.

### 6. Difficultés rencontrées et gestion des erreurs

J'ai rencontré quelques difficultés pendant cette deuxième partie. Déjà, au début, je pensais pouvoir récupérer directement les montées et les descentes avec le nom d'un arrêt. Mais en fait, j'ai dû comprendre qu'il fallait d'abord récupérer ses codes dans un premier jeu de données, puis les utiliser dans le deuxième. J'ai aussi eu quelques erreurs Python, notamment quand j'ai commencé à organiser mon code avec des fonctions `def`. Par exemple, j'avais utilisé `response` à un endroit et `reponse` à un autre, donc Python ne reconnaissait pas la variable. J'ai également eu des problèmes d'indentation quand j'ai ajouté la sauvegarde des résultats dans mes fonctions. Pour les résultats, j'ai utilisé `os.makedirs()` afin que les dossiers soient créés automatiquement s'ils n'existent pas. J'ai aussi séparé les résultats dans deux dossiers différents. Enfin, j'ai ajouté des blocs `try/except` autour des requêtes HTTP, comme dans la première partie, pour éviter que le programme s'arrête complètement si l'API TPG ne répond pas. Avec `raise_for_status()`, je peux aussi détecter les erreurs renvoyées par le serveur. Au final, cette deuxième partie m'a permis de mieux comprendre comment récupérer des données avec une API, mais surtout comment les utiliser ensemble pour obtenir un résultat qui dépend de ce que l'utilisateur entre.
