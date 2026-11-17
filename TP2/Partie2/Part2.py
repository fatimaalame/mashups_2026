import requests 

url_catalogue_tpg = "https://opendata.tpg.ch/api/explore/v2.1/catalog/datasets/arrets/records"
url_montees = "https://opendata.tpg.ch/api/explore/v2.1/catalog/datasets/montees-par-arret-par-ligne/records"
url_osm = "https://nominatim.openstreetmap.org/search"
reponse = requests.get(
    url_catalogue_tpg,
    params={"where": "search(nomarret, 'Cornavin')", "limit":100},
    timeout=10
)

reponse.raise_for_status()

donnees = reponse.json()
codes_arrets = []
for arret in donnees ["results"]:
    if arret["nomarret"] == "Gare Cornavin":
        codes_arrets.append(arret["arretcodelong"])

print("Nb de résultats:", donnees["total_count"])
print("Code de Gare Cornavin:", codes_arrets)
print("Nb de codes:", len(codes_arrets))

liste_codes = ", ".join("'" + code + "'" for code in codes_arrets)

reponse_montees = requests.get(
    url_montees,
    params={"where": f"arret_code_long IN ({liste_codes}) AND date = date'2026-02-07'","limit": 100},
    timeout=10
)

reponse_montees.raise_for_status()
donnees_montees = reponse_montees.json()
print("Nombre de mesures:", donnees_montees["total_count"])

total_montees = 0 
total_descentes = 0 

for mesure in donnees_montees["results"]:
    total_montees += mesure ["nb_de_montees"]
    total_descentes += mesure ["nb_de_descentes"]

print("Total montées:", round(total_montees, 2))
print("Total descentes:", round(total_descentes, 2))

if total_montees > total_descentes:
    print("Cornavin:plutot départ")
elif total_descentes > total_montees:
    print("cornavin: plutot arrivée")
else:
    print("Cornavin: autant de départs que d'arrivées")        

reponse_osm = requests.get(
    url_osm,
    params = {"q":"Gare Cornavin, Genève, Suisse", "format": "json", "limit":1},
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

total_voyageurs = total_montees + total_descentes 
pourcentage_montees = (total_montees / total_voyageurs) * 100
pourcentage_descentes = (total_descentes / total_voyageurs) * 100


print("pourcentage de montées: ", round(pourcentage_montees,2),"%")
print("pourcentage de descentes:", round(pourcentage_descentes,2),"%")
