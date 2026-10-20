import json 
from pathlib import Path

#to locate json file then read the data et les afficher 
fichier = Path (__file__).parent / "data" / "frequentation.json"

with open (fichier,"r", encoding="utf-8") as f:
    frequentation = json.load(f)

print ("Bienvenue dans TPG open data")
print ("Nombre d'enregistrements : ", len(frequentation))

print("\n--- Recherche d'une ligne TPG ---")

ligne_recherchee = input("Entrez un numéro de ligne : ")

resultats = []

for enregistrement in frequentation:
    if enregistrement["ligne"] == ligne_recherchee:
        resultats.append(enregistrement)

print("Nombre d'enregistrements trouvés :", len(resultats))