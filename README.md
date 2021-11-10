# Dokumentation League Prediction

Hausarbeit im Wahlpflichtmodul Applications in Data Science

# 1 Beschreibung der Skripte
Im Folgenden werden die in Python geschriebenen Skripte des League Prediction Projekts beschrieben. 

# 1.1 Klassen 

# 1.2 API-Anfrage

# 1.3 Datenverarbeitung
Im Python-Skript „data_processing“ befindet sich die Funktion „process_data“. Diese Funktion verarbeitet die Daten, die von der Web API des Herausgebers Riot Games angefragt und in das vorher beschriebene Datenschema verarbeitet wurden. Die übergebenen Daten werden hier im Wesentlichen für die Erstellung der Features vorbereitet. Hierfür wird die Spielhistorie aller Spieler eingelesen. Für die ausgewählten Feature-Kandidaten werden dann Durchschnittswerte pro Spieler über ihre Spielhistorie berechnet. Die Berechnung der Durchschnittswerte erfolgt jedoch präziser ausgedrückt in der ausgelagerten Funktion „create_avg_features“. Mithilfe einer übergebenen Liste können dann beliebig viele In-Game-Durchschnittsstatistiken berechnet werden.

Das Zielschema mit nur einem Feature-Kandidat „assists“ würde wie folgt aussehen: 

* result_data_model: matchId | game_result | Summoner_1_assists_avg | … | Summoner_n_assists_avg 

# 1.4 Erstellung der Features
Im Python-Skript „features“ befinden sich die Funktionen zur Erstellung der Features. Es werden an dieser Stelle Features berechnet, die die Performanz der einzelnen Spieler auf eine Teamperformanz zusammenfassen. Das Ziel ist hierbei am Ende eine Kennzahl zu erhalten, die die Performanz beider gegeneinander antretenden Teams berücksichtigt.

Das Zielschema der Daten sieht wie folgt aus: 

* features_x: matchId | game_result | feature_1 | … | feature_n

Berechnung der Features:

* Prozentualer Zuschlag / Abschlag der zusammengefassten Teamperformanz aus der Perspektive von Team 1 (blue). Ist Team 1 z.B. in Bezug auf die Kennzahl Assists besser, so wird der prozentuale Unterschied mit 1 addiert. Ist Team 2 z.B. in Bezug auf die Kennzahl Assists schlechter, so wird nur der prozentuale Anteil verwendet.

* Prozentualer Zuschlag / Abschlag der zusammengefassten Teamperformanz aus der Perspektive von Team 1 (blue). Ähnlich wie Beispiel 1 nur ausgehend von der Zahl 0. Eine positive Zahl spricht dann bspw. für eine bessere Performanz von Team 1. Das gleiche andersherum bei einer negativen Zahl.

# 1.5 Training der Modelle zur Vorhersage
Im Python-Skript „model_training“ werden verschiedene Klassifizierungsalgorithmen trainiert. Als Eingabe werden für die Funktionen die zuvor berechneten Features und Spielergebnisse übergeben.


