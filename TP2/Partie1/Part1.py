import requests
import json 
from datetime import datetime

url = "http://10.194.69.214:3671/api/v1/sensors/5/luminance"
url_ampoule = "http://10.194.69.214:3671/api/v1/dimmers/7" 

reponse = requests.get(url) #à l'adresse du capteur 
donnees = reponse.json()
luminosite = donnees["value"]

print("luminosité: ", luminosite, "lux")
reponse = requests.get(url, timeout=10)

## luminosite = 100 #test temporaire 
if luminosite >= 200:
    ampoule = 0
else:
    ampoule = round(((200-luminosite)/200)*99)
print("Intensité de l'ampoule: ", ampoule)

#to send la val de la formule
commande = {"value": ampoule} 

reponse_ampoule = requests.put(url_ampoule, json=commande, timeout=10)
print("Statut de la commande:", reponse_ampoule.status_code)

mesures = []
mesure = {
    "date_heure": datetime.now().isoformat(timespec="seconds"),
    "luminosite": luminosite,
    "ampoule": ampoule
}
mesures.append(mesure)

with open("TP2/Partie1/measures.json", "w", encoding="utf-8") as fichier:
    json.dump(mesures, fichier, indent=4, ensure_ascii=False)