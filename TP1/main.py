#import les fichiers json
import json 
from pathlib import Path

#importer le fichier xml
import xml.etree.ElementTree as ET

#to locate json file then read the data et les afficher 
fichier = Path (__file__).parent / "data" / "frequentation.json"

with open (fichier,"r", encoding="utf-8") as f:
    frequentation = json.load(f)

print ("Bienvenue dans TPG open data")
print ("Nombre d'enregistrements : ", len(frequentation))

print("\n--- Recherche d'une ligne TPG ---")

ligne_recherchee = input("Entrez un numéro de ligne: ")
resultats = []

# Pour le nombre d'enregistrements trouvés
for enregistrement in frequentation:
    if enregistrement["ligne"] == ligne_recherchee:
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


# Pour lire le fichier xml pr lire les arrets s
fichier_xml = Path(__file__).parent / "data" / "arrets.xml"

arbre = ET.parse(fichier_xml)
racine = arbre.getroot()

print("\nNombre d'entrées d'arrêts dans le XML :", len(racine))

# Recherche des arrets desservis par la ligne
ligne_xml = ligne_recherchee.zfill(2)

arrets_ligne = []

for arret in racine.findall("arret"):
    lignes = arret.findall("lignes/ligne")

    for ligne in lignes:
        if ligne.text == ligne_xml:
            arrets_ligne.append(arret.findtext("nom"))
            break

print("\nArrêts desservis par la ligne", ligne_recherchee, ":")

for nom in arrets_ligne:
    print("-", nom)

print("Nombre d'entrées d'arrêts :", len(arrets_ligne))