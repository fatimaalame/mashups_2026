#import les fichiers json
import json 
from pathlib import Path

#importer le fichier xml
import xml.etree.ElementTree as ET

#to locate json file then read the data et les afficher 
#here im using the frequentation.json
fichier = Path (__file__).parent / "data" / "frequentation.json"

with open (fichier,"r", encoding="utf-8") as f:
    frequentation = json.load(f)

# Pour lire le fichier xml pr lire les arrets s
fichier_xml = Path(__file__).parent / "data" / "arrets.xml"

arbre = ET.parse(fichier_xml)
racine = arbre.getroot()

#Scénario 1 to read the km produits 
#here im using the third json 
fichier_km = Path(__file__).parent / "data" / "kilometres.json"

with open(fichier_km, "r", encoding="utf-8") as f:
    kilometres = json.load(f)


## Début de l'application
print ("Bienvenue dans TPG open data")
print ("Nombre d'enregistrements : ", len(frequentation))


def fiche_ligne():
    print("\n--- Recherche d'une ligne TPG ---")

    ligne_recherchee = input("Entrez un numéro de ligne: ").strip()
    resultats = []

    # Pour le nombre d'enregistrements trouvés
    for enregistrement in frequentation:
        if (enregistrement["ligne"] == ligne_recherchee
                and enregistrement["annee"] == "2025"):
            resultats.append(enregistrement)

    print("Nombre d'enregistrements trouvés:", len(resultats))

    # Pour le total des montées
    total_montees = 0

    for enregistrement in resultats:
        total_montees += enregistrement["nb_de_montees"]

    print("Total des montées:", round(total_montees, 2))

    # Pour le total des descentes
    total_descentes = 0

    for enregistrement in resultats:
        total_descentes += enregistrement["nb_de_descentes"]

    print("Total des descentes:", round(total_descentes, 2))

    # Recherche des arrets desservis par la ligne
    #here im using the xml file 
    ligne_xml = ligne_recherchee.zfill(2)

    arrets_ligne = []

    for arret in racine.findall("arret"):
        lignes = arret.findall("lignes/ligne")

        for ligne in lignes:
            if ligne.text == ligne_xml:
                arrets_ligne.append(arret.findtext("nom"))
                break
  

    print("Nombre d'entrées d'arrêts :", len(arrets_ligne))

    #to remove les doublons
    arrets_uniques = set(arrets_ligne)

    print("\nNombre d'arrêts distincts :", len(arrets_uniques))

    print("\nListe des arrêts distincts :")
    for nom in sorted(arrets_uniques):
        print("-", nom)
    print("\n")

    #here im only looking for the km produits back in 2025
    resultats_km = []

    for enregistrement in kilometres:
        if (enregistrement["ligne"] == ligne_recherchee
                and enregistrement["date"].startswith("2025-")):
            resultats_km.append(enregistrement)

    print("\nNombre d'enregistrements kilométriques trouvés :", len(resultats_km))

    #Calcul du total des km produits
    total_km = 0

    for enregistrement in resultats_km:
        total_km += enregistrement["km_prod"]

    print("Total des kilomètres produits en 2025 :", round(total_km, 2))

fiche_ligne()