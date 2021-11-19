from src.api.api import load_live_match, load_one_match, load_match, load_summoner_history
from src.model.model_training import load_model, predict_with_model

model = load_model("random_forest")

loaders = [{'1': "live"}, {'2': "csv"}, {'3': "letztes"}, {'4': "match id"}]
loader_chosen = False
loader = None
matches = 5
while not loader_chosen:
    print("Wie soll das Match geladen werden? Bitte die Nummer eingeben.")
    print(loaders)
    try:
        input1 = int(input())
        if 0 < input1 <= len(loaders):
            loader = loaders[input1 - 1]
            loader = loader.get(str(input1))
            loader_chosen = True
        else:
            print("Bitte eine der angegebenen Nummern wählen")
    except:
        print("Bitte eine der angegebenen Nummern wählen")
print(loader)
matches_chosen = False
while not matches_chosen:
    print("Wie viele vergangene Spiele sollen für die Bewertung der Leistung beachtet werden? [1-100]")
    try:
        matches = int(input())
        if 101 > matches > 0:
            matches_chosen = True
        else:
            print("Bitte geben sie eine Zahl zwischen 1 und 100 ein.")
    except:
        print("Bitte geben sie eine Zahl zwischen 1 und 100 ein.")

if loader == "csv":
    print("Bitte den Namen einer Match Datei im Ordner tmp eingeben.")
    csv_src = input()
    print("Vorhersage für Sieg von Team "+str(2-predict_with_model(model, csv_src)[0]))
else:
    print("Bitte den Summoner Namen eingeben.")
    summoner_name = input()
    if loader == "letztes":
        print("lade letztes Spiel von " + summoner_name + ":")
        load_one_match(summoner_name, matches)
    elif loader == "live":
        print("lade live Spiel von " + summoner_name + ":")
        load_live_match(summoner_name, matches)
    elif loader == "match id":
        print("Lade die letzten 20 match ids:")
        print(load_summoner_history(summoner_name, 20))
        print("Bitte die match id eingeben.")
        match_id = input()
        print("lade Spiel " + match_id + " von " + summoner_name + ":")
        load_match(match_id, matches)
    print("Vorhersage für Sieg von Team "+str(2-predict_with_model(model, "../tmp/temp_match.csv")[0]))
