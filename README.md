# Dokumentation League Prediction

Hausarbeit im Wahlpflichtmodul Applications in Data Science

# 1 Installationsanweisung
Für die Applikation sollte Anaconda(für pandas, sklearn, joblib, seaborn & matplotlib), sowie dotenv (pip install python-dotenv) installiert sein. Die Datei „matches.rar“ im Ordner „data“ muss dazu entpackt werden. In der Datei „.env“ muss anschließend der API Key eingegeben werden. Damit sollte nun die Applikation im Skript „start“ ausführbar sein.

Zum Ausprobieren können folgende Summoner Namen verwendet werden:

* Don Noway

* noway2u

* Dzukill

Eine Liste von Spielern, die momentan live spielen: 

* https://www.trackingthepros.com/players/eu/in-game/

Hierfür muss auf den Namen des Spielers geklickt werden und dann kann der Name kopiert werden.


# 2 Ergebnisse
Mit den trainierten Algorithmen konnten keine hohe Accuracy erreicht werden. Die Accuracy bewegte sich im Laufe des Trainings zwischen 45 und 65 Prozent und konnte auch durch optionale Anpassungen nicht erhöht werden. Der Grund dafür liegt sehr wahrscheinlich darin, dass die ausgewählten Features keine hohe Aussagekraft besitzen. Dies lässt sich insbesondere in dem Bild „analyis_features_values“ in dem Ordner „data“ sehen. Die Abbildung zeigt pro Feature ein Koordinatensystem, in dem die Verteilung zwischen dem Feature-Ergebnis und dem Ausgang eines Matches zu sehen ist.

Als Vorschlag für die Verbesserung der Ergebnisse wäre es sinnvoll, Features mit Bezug auf die ausgewählten Charaktere der Spieler zu entwickeln. Hierfür wäre die Unterscheidung zwischen der allgemeinen Charakter-Performanz unter allen Spielern und die individuelle Performanz eines Spielers sinnvoll. Das Erstellen eines Features bzgl. der allgemeinen Performanz könnte sich jedoch als schwierig erweisen, da über die Web API keine zusammengefassten Statistiken erreichbar sind. 

Es ist zudem anzunehmen, dass eine gute Vorhersage Match-Ergebnisses bei öffentlichen Matches schwierig zu erreichen ist. Demnach wäre ein Fokus auf Matches auf einem hohen Niveau von Vorteil.

# 3 Beschreibung der Skripte
Im Folgenden werden die in Python geschriebenen Skripte des League Prediction Projekts beschrieben.

Hinweis: Mit dem Begriff Summoner ist in diesem Zusammenhang ein Spieler oder Spielteilnehmer gemeint.

# 3.1 Datenmodell
Im Skript „data_model“ befinden sich die Klassen der von der API angefragten Objekte.

Das Datenmodell sieht wie folgt aus:

* Match (enthält Summoner 1 bis 10), das vorhergesagt werden soll

* Summoner (enthält Liste vergangener Matches eines Summoner als SummonerMatches), ein Teilnehmer eines Matches

* SummonerMatch, die Details zu einem vergangenem Match eines Summoners 

# 3.2 API-Anfrage
Im Skript „apis“ werden über die Funktionen alle Daten aus Web API angefragt und in eine CSV-Datei geschrieben. Hierfür gibt es verschiedene Möglichkeiten:

* Laden eines Live-Matches

* Laden des zuletzt gespielten Matches

* Laden eines Matches per matchId

Beim Laden wird als Ergebnis ein Match aus dem definierten Datenmodell geliefert. Dementsprechend werden Bestandteile wie Summoner und SummonerMatches abgefragt.

# 3.3 Datenverarbeitung
Im Python-Skript „data_processing“ befindet sich die Funktion „process_data“. Diese Funktion verarbeitet die Daten, die von der Web API des Herausgebers Riot Games angefragt und in das vorher beschriebene Datenschema verarbeitet wurden. Die übergebenen Daten werden hier im Wesentlichen für die Erstellung der Features vorbereitet. Hierfür wird die Match-Historie aller Spieler eingelesen. Für die ausgewählten Feature-Kandidaten werden dann Durchschnittswerte pro Spieler über ihre Match-Historie berechnet. Die Berechnung der Durchschnittswerte erfolgt jedoch präziser ausgedrückt in der ausgelagerten Funktion „create_avg_features“. Mithilfe einer übergebenen Liste können dann beliebig viele In-Game-Durchschnittsstatistiken berechnet werden.

Das Zielschema mit nur einem Feature-Kandidat „assists“ würde wie folgt aussehen: 

* result_data_model: matchId | game_result | Summoner_1_assists_avg | … | Summoner_n_assists_avg 

# 3.4 Erstellung der Features
Im Python-Skript „features“ befinden sich die Funktionen zur Erstellung der Features. Es werden an dieser Stelle Features berechnet, die die Performanz der einzelnen Spieler auf eine Teamperformanz zusammenfassen. Das Ziel ist hierbei am Ende eine Kennzahl zu erhalten, die die Performanz beider gegeneinander antretenden Teams berücksichtigt.

Das Zielschema der Daten sieht wie folgt aus: 

* features_x: matchId | game_result | feature_1 | … | feature_n

Berechnung der Features:

* Prozentualer Zuschlag / Abschlag der zusammengefassten Teamperformanz aus der Perspektive von Team 1 (blue). Ist Team 1 z.B. in Bezug auf die Kennzahl Assists besser, so wird der prozentuale Unterschied mit 1 addiert. Ist Team 2 z.B. in Bezug auf die Kennzahl Assists schlechter, so wird nur der prozentuale Anteil verwendet.

* Prozentualer Zuschlag / Abschlag der zusammengefassten Teamperformanz aus der Perspektive von Team 1 (blue). Ähnlich wie Beispiel 1 nur ausgehend von der Zahl 0. Eine positive Zahl spricht dann bspw. für eine bessere Performanz von Team 1. Das gleiche andersherum bei einer negativen Zahl.

# 3.5 Training der Modelle zur Vorhersage
Im Python-Skript „model_training“ werden verschiedene Klassifizierungsalgorithmen trainiert. Als Eingabe werden für die Funktionen die zuvor berechneten Features und Match-Ergebnisse übergeben.

Es werden folgende Classifier verwendet:

* RandomForestClassifier

* DecisionTreeClassifier

* MLPClassifier 

* KNeighborsClassifier

# 3.6 Applikation
Um die Applikation zu starten, muss das Python-Skript „start“ ausgeführt werden. Es wird ein Dialog gestartet, in dem abgefragt wird, wie ein Match geladen werden soll und wie viele Matches für die Ermittlung der Performanz betrachtet werden sollen. Für das Starten der Bestimmung der Vorhersage muss ein Spieler Name eingegeben werden.


