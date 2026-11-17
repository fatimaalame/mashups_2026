import requests 

url = "https://opendata.tpg.ch/api/explore/v2.1/catalog/datasets/arrets/records"

reponse = requests.get(
    url,
    params={"where": "search(nomarret, 'Cornavin')", "limit":20},
    timeout=10
)

reponse.raise_for_status()

donnees = reponse.json()

for arret in donnees ["results"]:
    print(arret["nomarret"], ",", arret["arretcodelong"])

print("Nb de résultats:", donnees["total_count"])
