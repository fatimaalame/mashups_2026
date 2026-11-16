import requests
url = "http://10.194.69.214:3671/api/v1/sensors/5/luminance"

reponse = requests.get(url) #à l'adresse du capteur 
donnees = reponse.json()
luminosite = donnees["value"]