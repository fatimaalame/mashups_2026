import requests
url = "http://10.194.69.214:3671/api/v1/sensors/5/luminance"

reponse = requests.get(url) #à l'adresse du capteur 
donnees = reponse.json()
luminosite = donnees["value"]

print("luminosité: ", luminosite, "lux")
reponse = requests.get(url, timeout=10)

luminosite = 100 #test temporaire 
if luminosite >= 200:
    ampoule = 0
else:
    ampoule = round(((200-luminosite)/200)*99)
print("Intensité de l'ampoule: ", ampoule)
