import requests 

url = "https://opendata.tpg.ch/api/explore/v2.1/catalog/datasets/arrets/records"
url_montees = "https://opendata.tpg.ch/api/explore/v2.1/catalog/datasets/montees-par-arret-par-ligne/records"
reponse = requests.get(
    url,
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