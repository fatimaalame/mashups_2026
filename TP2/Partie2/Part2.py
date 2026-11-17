import requests 
import json 
import os 

url_catalogue_tpg = "https://opendata.tpg.ch/api/explore/v2.1/catalog/datasets/arrets/records"
url_montees = "https://opendata.tpg.ch/api/explore/v2.1/catalog/datasets/montees-par-arret-par-ligne/records"

def analyser_frequentation():
    print() #debut interface1

    ##nom_arret = "arretinexistant" ## test pour protection
    nom_arret = input("Entrez le nom d'un arrêt TPG : ")
    print()
    reponse = requests.get(
        url_catalogue_tpg,
        params={"where": f"search(nomarret, '{nom_arret}')", "limit":100},
        timeout=10
    )

    reponse.raise_for_status()

    donnees = reponse.json()
    codes_arrets = []
    for arret in donnees ["results"]:
        if arret["nomarret"].casefold() == nom_arret.casefold():
            codes_arrets.append(arret["arretcodelong"])

    print("Nb de résultats:", donnees["total_count"])
    print("Code de", nom_arret, ":",codes_arrets)
    print("Nb de codes:", len(codes_arrets))

    if not codes_arrets:
        print("Aucun code trouvé pour", nom_arret)
        return

    liste_codes = ", ".join("'" + code + "'" for code in codes_arrets)

    reponse_montees = requests.get(
        url_montees,
        params={"where": f"arret_code_long IN ({liste_codes}) AND date = date'2026-02-07'","limit": 100},
        timeout=10
    )

    reponse_montees.raise_for_status()
    donnees_montees = reponse_montees.json()
    print("Nb de mesures trouvées:", donnees_montees["total_count"])

    total_montees = 0 
    total_descentes = 0 

    for mesure in donnees_montees["results"]:
        total_montees += mesure ["nb_de_montees"]
        total_descentes += mesure ["nb_de_descentes"]

    print ()
    print(" -- Résultats pour " , nom_arret, " -- ")
    print("Total montées:", round(total_montees, 2))
    print("Total descentes:", round(total_descentes, 2))
    print ()
    if total_montees > total_descentes:
        print(nom_arret, " -> plutot départ")
    elif total_descentes > total_montees:
        print(nom_arret, " -> plutot arrivée")
    else:
        print(nom_arret, " -> autant de départs que d'arrivées")        
    print()

    total_movement= total_montees + total_descentes 
    if total_movement > 0:
        pourcentage_montees = (total_montees / total_movement) * 100
        pourcentage_descentes = (total_descentes / total_movement) * 100
    else:
        pourcentage_montees = 0
        pourcentage_descentes = 0 

    print("pourcentage de montées: ", round(pourcentage_montees,2),"%")
    print("pourcentage de descentes:", round(pourcentage_descentes,2),"%")
    print ()


    dossier_resultats = os.path.join(os.path.dirname(__file__), "my_results")
    os.makedirs(dossier_resultats, exist_ok=True)

    resultat = {
        "arret": nom_arret,
        "date_donnees": "2026-02-07",
        "codes_arrets": codes_arrets,
        "total_montees": round(total_montees, 2),
        "total_descentes": round(total_descentes, 2),
        "pourcentage_montees": round(pourcentage_montees, 2),
        "pourcentage_descentes": round(pourcentage_descentes, 2)
    }

    nom_fichier = nom_arret.replace(" ", "_").replace("/", "_") + ".json"
    chemin_fichier = os.path.join(dossier_resultats, nom_fichier)

    with open(chemin_fichier, "w", encoding="utf-8") as fichier:
        json.dump(resultat, fichier, indent=4, ensure_ascii=False)

def main ():
    choix = "" 
    while choix != "0":
        print()
        print(" -- TPG OPEN API -- ")
        print(" 1.Fréquentation d'un arrêt")
        print("2. Rechercher les arrêts par lettre")
        print("0. Quitter")
        print()

        choix = input ("Votre input ? ")
        if choix == "1":
            analyser_frequentation()
        elif choix == "2":
            print("scénario 2 par encore fait")
        elif choix == "0":
            print("Au revoir")
            print ()
        else:
            print("Choix inconnu, réessayez svp")

if __name__ == "__main__"    :
    main()                        