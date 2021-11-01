import requests

url = "https://euw1.api.riotgames.com"
key = "" # private key
# key = "RGAPI-0d9039f8-ef59-415b-9162-72bbcec454f7"


def getSummoner():
    r = requests.get(url + 'lol/platform/')
    return r.json()


# rate limits beachten



r = requests.get("https://euw1.api.riotgames.com/lol/platform/v3/champion-rotations?api_key=RGAPI-0d9039f8-ef59-415b-9162-72bbcec454f7")
print(r.json())