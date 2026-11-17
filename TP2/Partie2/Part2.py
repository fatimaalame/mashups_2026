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

reponse_montees = requests.get(
    url_montees,
    params={"where": "arret_code_long = 'CVIN03' AND date = date'2026-02-07'","limit": 100},
    timeout=10
)

reponse_montees.raise_for_status()
donnees_montees = reponse_montees.json()

for mesure in donnees_montees["results"]:
    print(mesure["date"], mesure["ligne"], mesure["nb_de_montees"], mesure["nb_de_descentes"])
