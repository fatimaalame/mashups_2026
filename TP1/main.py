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

############ INTERFACE -> Menu principal
def menu():
    print("\n  TPG OPEN DATA   ")
    print("\nQue souhaitez-vous faire ?")
    print("1. Fiche d'une ligne TPG")
    print("2. Top 5 des arrêts les plus fréquentés")
    print("3. Top 10 des lignes avec le plus d'arrêts")
    print("4. Comparaison des horaires VACANCES / NORMAL")
    print("5. Arrêts stratégiques du réseau")

    choix = input("\nVotre choix : ").strip()

    if choix == "1":
        fiche_ligne()

    elif choix == "2":
        top_5_arrets()

    elif choix == "3":
        classement_lignes()

    elif choix == "4":
        comparaison_horaires()

    elif choix == "5":
        print("Ce scénario n'est pas encore disponible.")

    else:
        print("Choix invalide. Veuillez réessayer.")

menu()

############# SCENARIO 1 -> fiche d'une ligne
def fiche_ligne():
    print("\n--- Recherche d'une ligne TPG ---")

    ligne_recherchee = input("Entrez un numéro de ligne: ").strip()
    resultats = []

    #pr le nombre d'enregistrements trouvés
    for enregistrement in frequentation:
        if (enregistrement["ligne"] == ligne_recherchee
                and enregistrement["annee"] == "2025"):
            resultats.append(enregistrement)

    print("Nombre d'enregistrements trouvés:", len(resultats))

    #pr le total des montées
    total_montees = 0

    for enregistrement in resultats:
        total_montees += enregistrement["nb_de_montees"]

    print("Total des montées:", round(total_montees, 2))

    #pr le total des descentes
    total_descentes = 0

    for enregistrement in resultats:
        total_descentes += enregistrement["nb_de_descentes"]

    print("Total des descentes:", round(total_descentes, 2))

    #recherche des arrets desservis par la ligne
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


############ SCENARIO 2-> Top 5 arrets montés par ligne  
def top_5_arrets():
    print("\n--- Top 5 des arrêts les plus fréquentés ---")

    ligne_recherchee = input("Entrez un numéro de ligne: ").strip()

    montees_par_arret = {}

    for enregistrement in frequentation:
        if (enregistrement["ligne"] == ligne_recherchee
                and enregistrement["annee"] == "2025"):

            nom = enregistrement["arret"]

            if nom not in montees_par_arret:
                montees_par_arret[nom] = 0

            montees_par_arret[nom] += enregistrement["nb_de_montees"]

    print("Nombre d'arrêts trouvés :", len(montees_par_arret))

    if not montees_par_arret:
        print("Aucune donnée de fréquentation trouvée pour cette ligne en 2025.")
        return 

    #to sort les arrêts selon le nombre de montées
    classement = sorted(
        montees_par_arret.items(), #.items = récupère les couples (nom, montées) du dico
        key=lambda element: element[1], #lamba = fct sans nom qui indique à sorted quelle val utiliser pr effectuer tri
        reverse=True #trie du + grd au + petit
    )

    #to show uniquement les 5 premiers
    print("\nTop 5 des arrêts de la ligne", ligne_recherchee)

    for nom, montees in classement[:5]: #conserve only first 5
        print("-", nom, ":", round(montees, 2), "montées")

    print("\nCodes des arrêts du top 5 :")
    #to verify les codes des arrets du top 5
    for nom, montees in classement[:5]:
        codes = set()
        codes_trouves = set()

        for enregistrement in frequentation:
            if (enregistrement["ligne"] == ligne_recherchee
                    and enregistrement["annee"] == "2025"
                    and enregistrement["arret"] == nom):
                codes.add(enregistrement["arret_code_long"])

        print(nom, ":", sorted(codes))
        
        #to search les coordonnées dans le XML
        for arret in racine.findall("arret"):
            code_xml = arret.findtext("code")

            if code_xml in codes:
                codes_trouves.add(code_xml)
                latitude = arret.findtext("coordonnees/latitude")
                longitude = arret.findtext("coordonnees/longitude")

                print("  Quai", code_xml, ":", latitude, longitude)

        #pr afficher les codes absents du XML
        codes_manquants = codes - codes_trouves
        if codes_manquants:
            print("  Codes absents du XML :", sorted(codes_manquants))               

############ SCENARIO 3 -> Classement des lignes par nombre d'arrêts
def classement_lignes():
    print("\n--- Classement des lignes TPG ---")

    arrets_par_ligne = {}

    for arret in racine.findall("arret"):
        nom = arret.findtext("nom")

        for ligne in arret.findall("lignes/ligne"):
            numero = ligne.text

            if numero not in arrets_par_ligne:
                arrets_par_ligne[numero] = set()

            arrets_par_ligne[numero].add(nom)

    print("Nombre de lignes trouvées :", len(arrets_par_ligne))
    nombre_arrets = {} #créé nv dico avec num de chaque ligne et son nb stops

    for numero, arrets in arrets_par_ligne.items(): #on parcourt le dico 
        nombre_arrets[numero] = len(arrets) #compte éléments de l'ens + enregistre résults

    classement = sorted(
    nombre_arrets.items(), #récupère couple num + nb d'arrets 
    key=lambda element: element[1], #el[1] = nb d'arret 
    reverse=True #classe du + grd au + ptt 
    )

    # Calculer les montées en 2025 pour chaque ligne
    montees_par_ligne = {} #create a new dico (num ligne à son total de montées 2025) 

    for enregistrement in frequentation: #parcourt ts les enre du json
        if enregistrement["annee"] == "2025":
            numero = enregistrement["ligne"].zfill(2) #we only keep yr 2025 

            if numero not in montees_par_ligne:
                montees_par_ligne[numero] = 0

            montees_par_ligne[numero] += enregistrement["nb_de_montees"]

    print("\nTop 10 des lignes avec le plus d'arrêts :")

    for numero, nombre in classement[:10]:
        if numero in montees_par_ligne:
            montees = round(montees_par_ligne[numero], 2)
            frequentation_texte = str(montees) + " montées en 2025"
        else:
            frequentation_texte = "Données de fréquentation indisponibles"

        print(
            "Ligne", numero, ":",
            nombre, "arrêts distincts -",
            frequentation_texte
        )

############ SCENARIO 4 -> Vacances vs horaires normaux
def comparaison_horaires():
    print("\n--- Comparaison des horaires TPG ---")

    ligne_recherchee = input("Entrez un numéro de ligne: ").strip()

    km_vacances = [] #2 list vides 
    km_normal = []

    for enregistrement in kilometres: #on parcourt mon fichier json km
        if (enregistrement["ligne"] == ligne_recherchee
                and enregistrement["date"].startswith("2025-")):

            if enregistrement["horaire_type"] == "VACANCES":
                km_vacances.append(enregistrement["km_prod"])

            elif enregistrement["horaire_type"] == "NORMAL":
                km_normal.append(enregistrement["km_prod"])

    print("Enregistrements VACANCES :", len(km_vacances))
    print("Enregistrements NORMAL :", len(km_normal)) #compte le nombre de val saved in every list

    if km_vacances and km_normal:
        moyenne_vacances = sum(km_vacances) / len(km_vacances)
        moyenne_normal = sum(km_normal) / len(km_normal)

        print("\nMoyenne VACANCES :", round(moyenne_vacances, 2), "km")
        print("Moyenne NORMAL :", round(moyenne_normal, 2), "km")
    else:
        print("Pas assez de données pour comparer les horaires.")