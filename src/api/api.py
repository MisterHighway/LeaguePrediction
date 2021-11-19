import json
import requests
import time
import pandas as pd
import src.model.data_model as data
from dotenv import load_dotenv
import os

url_europe = "https://europe.api.riotgames.com"
url_euw1 = "https://euw1.api.riotgames.com"
load_dotenv()
key = os.getenv("API_Key")
if key is None:
    key = ""

file = "../tmp/temp_match.csv"  # for loading temporary matches


# file = "../data/matches6.csv"  # for storing matches


def wait_exceeded():
    for i in range(120):
        time.sleep(1)
        i = i + 1
        if i % 10 == 0:
            print('Noch ' + str(120 - i) + ' Sekunden')


def http_call(url, api):
    if "?" in api:
        apikey = "&api_key=" + key
    else:
        apikey = "?api_key=" + key
    r = requests.get(url + api + apikey, allow_redirects=False)
    if r.status_code == 429:
        print("Aufruf Limit erreicht. Bitte warten Sie 2 Minuten.")
        wait_exceeded()
        http_call(url, api)
    elif r.status_code == 200:
        return r
    else:
        print("something went wrong" + str(r.status_code))


def match_to_csv(new_data, file_src):
    old_data = None
    try:
        old_data = pd.read_csv(file_src)
    except:
        pass
    finally:
        if old_data is not None and "temp_match" not in file_src:
            pd.DataFrame(old_data.append(pd.json_normalize(json.loads(new_data)))).to_csv(file_src, index=False)
        else:
            pd.DataFrame(pd.json_normalize(json.loads(new_data))).to_csv(file_src, index=False)


def load_live_match(summoner_name, amount_matches=5):
    summoner = []
    s = http_call(url_euw1, "/lol/summoner/v4/summoners/by-name/" + str(summoner_name))
    if s is None:
        print("player might not be in game.")
    else:
        s_id = s.json()["id"]
        m = http_call(url_euw1, "/lol/spectator/v4/active-games/by-summoner/" + str(s_id))
        if m is None:
            print("this didnt work for summoner id: " + str(s_id))
        else:
            match_id = m.json()["gameId"]
            for p in m.json()["participants"]:
                print(p["summonerName"], str(p["teamId"])[0])
                player = http_call(url_euw1, "/lol/summoner/v4/summoners/" + p["summonerId"])
                if player.json() is None:
                    print("cant find the player")
                    summoner.append('"None"')
                else:
                    puuid = player.json()["puuid"]
                    summoner.append(data.Summoner(get_summoner(puuid, amount_matches), p["championId"]))
            match_to_csv(data.Match(match_id, summoner[0], summoner[1], summoner[2], summoner[3], summoner[4],
                                    summoner[5], summoner[6], summoner[7], summoner[8], summoner[9],
                                    '"None"').to_string(), file)


def load_one_match(summoner_name, amount_matches=5):
    summoner = []
    s = http_call(url_euw1, "/lol/summoner/v4/summoners/by-name/" + str(summoner_name))
    if s is None:
        print("cant find a game of this player.")
    else:
        s_id = s.json()["puuid"]
        m = http_call(url_europe, "/lol/match/v5/matches/by-puuid/" + s_id + "/ids?start=0&count=1")
        if m is None:
            print("this didnt work for summoner id: " + str(s_id))
        else:
            match_id = m.json()[0]
            match = http_call(url_europe, "/lol/match/v5/matches/" + str(match_id))
            for p in match.json()["info"]["participants"]:
                print(p["summonerName"], str(p["teamId"])[0])
                player = http_call(url_euw1, "/lol/summoner/v4/summoners/" + p["summonerId"])
                if player.json() is None:
                    print("cant find the player")
                    summoner.append('"None"')
                else:
                    puuid = player.json()["puuid"]
                    summoner.append(data.Summoner(get_summoner(puuid, amount_matches), p["championId"]))
            match_to_csv(data.Match(match_id, summoner[0], summoner[1], summoner[2], summoner[3], summoner[4],
                                    summoner[5], summoner[6], summoner[7], summoner[8], summoner[9],
                                    '"None"').to_string(), file)


def load_match(match_id, amount_matches=5):
    summoner = []
    m = http_call(url_europe, "/lol/match/v5/matches/" + match_id)
    if m is None:
        print("retry load match: " + match_id)
        return load_match(match_id, amount_matches)
    else:
        win = str(m.json()["info"]["participants"][0]["win"])
        for p in m.json()["info"]["participants"]:
            print(p["summonerName"], str(p["teamId"])[0])
            summoner.append(data.Summoner(get_summoner(p["puuid"], amount_matches), p["championId"]))

    match_to_csv(data.Match(match_id, summoner[0], summoner[1], summoner[2], summoner[3], summoner[4],
                            summoner[5], summoner[6], summoner[7], summoner[8], summoner[9], win).to_string(), file)


def get_summoner(puu_id, amount_matches):
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
        return get_summoner(puu_id, amount_matches)


def load_summoner_history(summoner_name, amount_matches):
    r = http_call(url_euw1, "/lol/summoner/v4/summoners/by-name/" + summoner_name)
    if r is not None:
        puuid = r.json()["puuid"]
        r = http_call(url_europe,
                      "/lol/match/v5/matches/by-puuid/" + puuid + "/ids?start=0&count=" + str(amount_matches))
        if r is not None:
            matches = r.json()
            return matches
        else:
            load_summoner_history(summoner_name, amount_matches)
    else:
        load_summoner_history(summoner_name, amount_matches)
