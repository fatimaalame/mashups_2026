import requests 

url = "https://opendata.tpg.ch/api/explore/v2.1/catalog/datasets/arrets/records"

reponse = requests.get(url, params={"limit": 3}, timeout = 10)
donnees = reponse.json() #answer is an json dico

print(donnees["results"])
