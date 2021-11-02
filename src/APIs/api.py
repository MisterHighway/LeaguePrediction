import json
import requests
import time
import pandas as pd
import Model.data_model as data

url_europe = "https://europe.api.riotgames.com"
url_euw1 = "https://euw1.api.riotgames.com"
key = "RGAPI-e91be27c-c547-4f3e-ab2a-3d602e845ef7"  # private key
# key = "RGAPI-0d9039f8-ef59-415b-9162-72bbcec454f7"
file_src = "../Model/matches.csv"  # training data
amount_matches = 5


def wait_exceeded():
    for i in range(120):
        time.sleep(1)
        i = i + 1
        print(i)


def http_call(url, api):
    if "?" in api:
        apikey = "&api_key=" + key
    else:
        apikey = "?api_key=" + key
    r = requests.get(url + api + apikey)
    if r.status_code == 429:
        print("rate limit exceeded.")
        wait_exceeded()
        http_call(url, api)
    elif r.status_code == 200:
        return r
    else:
        print("something went wrong" + str(r.status_code))


def match_to_csv(new_data):
    old_data = None
    try:
        old_data = pd.read_csv(file_src)
        print(old_data)
    except:
        print("no old data")
    finally:
        if old_data is not None:
            pd.DataFrame(old_data.append(pd.json_normalize(json.loads(new_data)))).to_csv(file_src, index=False)
        else:
            pd.DataFrame(pd.json_normalize(json.loads(new_data))).to_csv(file_src, index=False)


def load_match(match_id, puu_id):
    summoner = []
    win = None
    m = http_call(url_europe, "/lol/match/v5/matches/" + match_id)
    if m is None:
        print("retry load match: " + match_id + "; " + puu_id)
        return load_match(match_id, puu_id)
    else:
        for p in m.json()["info"]["participants"]:
            print(p["summonerName"])
            summoner.append(data.Summoner(get_summoner(p["puuid"]), p["championId"]))
            if p["puuid"] == puu_id:
                win = str(p["win"])
    match_to_csv(data.Match(match_id, summoner[0], summoner[1], summoner[2], summoner[3], summoner[4],
                            summoner[5], summoner[6], summoner[7], summoner[8], summoner[9], win).to_string())


def get_summoner(puu_id):
    r = http_call(url_europe, "/lol/match/v5/matches/by-puuid/" + puu_id + "/ids?start=0&count=" + str(amount_matches))
    if r is not None:
        r = http_call(url_europe, "/lol/match/v5/matches/by-puuid/" + puu_id + "/ids?start=0&count=" + str(amount_matches))
        match_ids = r.json()
        summoner_matches = []
        for ma in match_ids:
            r = http_call(url_europe, "/lol/match/v5/matches/" + str(ma))
            stats = None
            if r is not None:
                for p in r.json()["info"]["participants"]:
                    if p["puuid"] == puu_id:
                        stats = p
                summoner_matches.append(data.SummonerMatch(puu_id, r.json()["info"]["gameDuration"], stats))
                return summoner_matches
            else:
                print("retry loading summoner_match : " + str(ma) + "; " + puu_id)
                return get_summoner(puu_id)
    else:
        print("retry loading match_history : " + puu_id)
        return get_summoner(puu_id)


matches = [
    "EUW1_5527687562",
    "EUW1_5527670892",
    "EUW1_5527458633",
    "EUW1_5527441595",
    "EUW1_5527365898",
    "EUW1_5527251116",
    "EUW1_5527236386",
    "EUW1_5527213185",
    "EUW1_5527138215",
    "EUW1_5527133667",
    "EUW1_5527010190",
    "EUW1_5521475473",
    "EUW1_5521461318",
    "EUW1_5521386656",
    "EUW1_5521411496",
    "EUW1_5517037425",
    "EUW1_5516980009",
    "EUW1_5516904767",
    "EUW1_5516810272",
    "EUW1_5516852432"
]

for m in matches:
    load_match(m, "R0OlrY75z-x0-Mff-kteKSn_JnS0KXDC1SzweYXDjU55F1S4lW_YdmMBPPMfyYYZS3rOAd6yeOOWPA")
