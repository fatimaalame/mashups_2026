import requests 

url_catalogue_tpg = "https://opendata.tpg.ch/api/explore/v2.1/catalog/datasets/arrets/records"
url_montees = "https://opendata.tpg.ch/api/explore/v2.1/catalog/datasets/montees-par-arret-par-ligne/records"
url_osm = "https://nominatim.openstreetmap.org/search"


print() #debut interface
print (" -- TPG OPEN API  -- ")
print()

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
    exit ()

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

reponse_osm = requests.get(
    url_osm,
    params = {"q":f"{nom_arret} Genève, Suisse", "format": "json", "limit":1},
    headers={"User-Agent":"MashupUNIGEStudentProject/1.0(education)"},timeout=10
)

reponse_osm.raise_for_status()
donnees_osm = reponse_osm.json()

if donnees_osm:
    latitude = donnees_osm[0]["lat"]
    longitude = donnees_osm[0]["lon"]

    print("Latitude :", latitude)
    print("Longitude :", longitude)
else:
    print("Aucun résultat OpenStreetMap")


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