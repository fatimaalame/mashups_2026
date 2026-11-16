import requests
import json 
from datetime import datetime
import time

url = "http://10.194.69.214:3671/api/v1/sensors/5/luminance"
url_ampoule = "http://10.194.69.214:3671/api/v1/dimmers/7" 

mesures = []

nom_fichier = "TP2/Partie1/mesures_" + datetime.now().strftime("%Y%m%d_%H%M%S") + ".json"

for i in range (10):
    try:    
        reponse = requests.get(url, timeout=10) #à l'adresse du capteur + récup nlle luminosité
        donnees = reponse.json()
        luminosite = donnees["value"]

        ## luminosite = 100 #test temporaire 
        if luminosite >= 200: # calcul lum
            ampoule = 0
        else:
            ampoule = round(((200-luminosite)/200)*99)

        #to send la val de la formule pr régler ampoule
        commande = {"value": ampoule} 
        reponse_ampoule = requests.put(url_ampoule, json=commande, timeout=10)
        reponse_ampoule.raise_for_status()
        
        mesure = { #save la mesure dans liste + dico 
            "date_heure": datetime.now().isoformat(timespec="seconds"),
            "luminosite": luminosite,
            "ampoule": ampoule
        }
        mesures.append(mesure)

        with open(nom_fichier, "w", encoding="utf-8") as fichier:
            json.dump(mesures, fichier, indent=4, ensure_ascii=False)

        print("Mesure", i + 1, ":", luminosite, "lux")
    
    except requests.RequestException as error:
                print("erreur de connexion:", error)
    if i < 9: 
            time.sleep(30)

