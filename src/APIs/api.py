import json
import requests
import time
import pandas as pd
import Model.data_model as data

url_europe = "https://europe.api.riotgames.com"
url_euw1 = "https://euw1.api.riotgames.com"
# key = "RGAPI-8babd049-cc39-420f-a612-5a04b527a8f6"  # private key
key = "RGAPI-0d9039f8-ef59-415b-9162-72bbcec454f7"
file_src = "../Data/matches4.csv"  # training data
amount_matches = 50


def wait_exceeded():
    for i in range(120):
        time.sleep(1)
        i = i + 1
        if i % 10 == 0:
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
    except:
        print("no old data")
    finally:
        if old_data is not None:
            pd.DataFrame(old_data.append(pd.json_normalize(json.loads(new_data)))).to_csv(file_src, index=False)
        else:
            pd.DataFrame(pd.json_normalize(json.loads(new_data))).to_csv(file_src, index=False)
    print(pd.read_csv(file_src))


def load_match(match_id, puu_id):
    summoner = []
    m = http_call(url_europe, "/lol/match/v5/matches/" + match_id)
    if m is None:
        print("retry load match: " + match_id + "; " + puu_id)
        return load_match(match_id, puu_id)
    else:
        win = str(m.json()["info"]["participants"][0]["win"])
        for p in m.json()["info"]["participants"]:
            print(p["summonerName"])
            summoner.append(data.Summoner(get_summoner(p["puuid"]), p["championId"]))

    match_to_csv(data.Match(match_id, summoner[0], summoner[1], summoner[2], summoner[3], summoner[4],
                            summoner[5], summoner[6], summoner[7], summoner[8], summoner[9], win).to_string())


def get_summoner(puu_id):
    r = http_call(url_europe, "/lol/match/v5/matches/by-puuid/" + puu_id + "/ids?start=0&count=" + str(amount_matches))
    if r is not None:
        match_ids = r.json()
        summoner_matches = []
        for ma in match_ids:
            r = http_call(url_europe, "/lol/match/v5/matches/" + str(ma))
            stats = None
            if r is not None:
                for p in r.json()["info"]["participants"]:
                    if p["puuid"] == puu_id:
                        stats = p
                if stats is None:
                    stats = '"None"'
                game_duration = r.json()["info"]["gameDuration"]
                if game_duration is None:
                    game_duration = '"None"'
                summoner_matches.append(data.SummonerMatch(puu_id, game_duration, stats))
            else:
                print("retry loading summoner_match : " + str(ma) + "; " + puu_id)
        if summoner_matches is None:
            summoner_matches = '"None"'
        return summoner_matches
    else:
        print("retry loading match_history : " + puu_id)
        return get_summoner(puu_id)


def load_summoner_history(summoner_name):
    r = http_call(url_euw1, "/lol/summoner/v4/summoners/by-name/" + summoner_name)
    if r is not None:
        puuid = r.json()["puuid"]
        r = http_call(url_europe, "/lol/match/v5/matches/by-puuid/"+puuid+"/ids?start=0&count="+str(amount_matches))
        if r is not None:
            matches = r.json()
            for m in matches:
                load_match(m, puuid)
        else:
            load_summoner_history(summoner_name)
    else:
        load_summoner_history(summoner_name)


load_summoner_history("Razørk Activoo")
file_src = "../Data/matches5.csv"  # training data
load_summoner_history("Raiden Shogun C2")
