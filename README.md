# mashups_2026
Practical assignments for the Mashups and Contextualisation course at the University of Geneva (UNIGE)

J'aimerai créer un programme python utilisable dans le terminal qui combine des données sur les arrêts, la fréquentation et les kilomètres parcourus du réseau TPG etc...

## TP1 -> TPG Open Data

### Présentation du projet

L'objectif de ce TP est de développer un programme Python utilisable dans le terminal, qui combine plusieurs jeux de données ouvertes des Transports publics genevois (TPG).

Le programme permet d'analyser les lignes du réseau à partir des arrêts desservis, de la fréquentation des voyageurs et des kilomètres produits.

Il utilise trois fichiers de données, aux formats JSON et XML.

### Sources de données

| Fichier | Format | Contenu |
|---|---|---|
| `frequentation.json` | JSON | Montées et descentes mensuelles par ligne et par arrêt |
| `arrets.xml` | XML | Arrêts, quais et lignes desservies |
| `kilometres.json` | JSON | Kilomètres produits quotidiennement par ligne |

Les calculs de fréquentation et de kilomètres sont effectués sur les données de l'année **2025**.

### Exécution

Le programme utilise Python 3 et uniquement des bibliothèques standard (`json`, `pathlib`, `xml.etree.ElementTree`).

Depuis le dossier `TP1`, exécuter :

```bash
python3 main.py
```

### Scénario 1 — Fiche d'une ligne TPG

Ce premier scénario permet à l'utilisateur de saisir un numéro de ligne et d'obtenir plusieurs informations à son sujet.

Le programme combine les trois fichiers pour :

- Calculer le total des montées et descentes en 2025.
- Identifier les arrêts desservis par la ligne.
- Supprimer les noms d'arrêts en double.
- Calculer le total des kilomètres produits en 2025.

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

Le programme affiche également les noms des arrêts distincts par ordre alphabétique.

**Particularités des données :** les numéros de ligne ne sont pas toujours écrits de la même manière dans les fichiers (`5` en JSON et `05` en XML). Le programme utilise actuellement `zfill(2)` pour gérer ce cas. Le nombre de noms distincts ne correspond pas nécessairement au nombre exact d'arrêts physiques.

### Avancement

- [x] Chargement des trois sources JSON/XML
- [x] Première version fonctionnelle du scénario 1
- [ ] Scénario 2 — Top 5 des arrêts les plus fréquentés d'une ligne
- [ ] Scénario 3 — Nombre d'arrêts par ligne
- [ ] Scénario 4 — Vacances et horaires normaux
- [ ] Scénario 5 — Arrêts stratégiques du réseau
- [ ] Menu interactif
- [ ] Tests finaux et rapport
