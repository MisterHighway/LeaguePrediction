from src.api.api import load_live_match
from src.model.model_training import load_model, predict_with_model

model = load_model("random_forest")
# model = load_model("decision_tree")

load_live_match("Envy Carry")
predict_with_model(model, "../tmp/temp_match.csv")

loaders = [{'1': "live"}, {'2': "csv"}, {'3': "history"}]
loader_chosen = False
loader = None
while not loader_chosen:
    print("Wie soll das Match geladen werden? Bitte die Nummer eingeben.")
    print(loaders)
    input1 = input()
    if len(input1) < 2:
        loader = loaders[int(input1) - 1]
        loader = loader.get(input1)
        loader_chosen = True
    else:
        print("Bitte eine der angegebenen Möglichkeiten wählen")
print(loader)

if loader == "csv":
    print("Bitte den absoluten Pfad der csv eingeben.")
    csv_src = input()
    # csv zeile mit match Id suchen und starten
else:
    print("Bitte den Summoner Namen eingeben.")
    summoner_name = input()
    # mit summoner_name starten

