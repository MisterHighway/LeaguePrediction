class SummonerMatch:

    def __init__(self, puuid, game_time, in_game_stats):
        self.puuid = puuid  # identifier of the summoner playing the match
        self.game_time = game_time  # the time until one team won
        self.in_game_stats = in_game_stats  # the summoners in game stats, such as damage done, etc

    def to_string(self):
        return '{ "puuid": "' + self.puuid + '", "game_time": ' + str(self.game_time) \
               + ', "in_game_stats": ' + \
               str(self.in_game_stats) + "}"


class Summoner:

    def __init__(self, match_history, champion):
        self.match_history = match_history  # array of last matches
        self.champion = champion  # champion in active game

    def to_string(self):
        match_history = "["
        for m in self.match_history:
            match_history += m.to_string() + ","
        match_history = match_history[0:len(match_history) - 1]
        match_history += "]"
        return '{ "match_history": ' + match_history + ', "champion": ' + str(self.champion) + "}"


class Match:

    def __init__(self, summoner1, summoner2, summoner3, summoner4,
                 summoner5, summoner6, summoner7, summoner8, summoner9, summoner10, win):
        self.summoner1 = summoner1  # game participants
        self.summoner2 = summoner2
        self.summoner3 = summoner3
        self.summoner4 = summoner4
        self.summoner5 = summoner5
        self.summoner6 = summoner6
        self.summoner7 = summoner7
        self.summoner8 = summoner8
        self.summoner9 = summoner9
        self.summoner10 = summoner10
        self.win = win  # summoner 1-5 game won?

    def to_string(self):
        res = '{ "Summoner1":' + self.summoner1.to_string() + ', "Summoner2":' + self.summoner2.to_string() \
               + ', "Summoner3":' + self.summoner3.to_string() + ', "Summoner4":' + self.summoner4.to_string() \
               + ', "Summoner5":' + self.summoner5.to_string() + ', "Summoner6":' + self.summoner6.to_string() \
               + ', "Summoner7":' + self.summoner7.to_string() + ', "Summoner8":' + self.summoner8.to_string() \
               + ', "Summoner9":' + self.summoner9.to_string() + ', "Summoner10":' + self.summoner10.to_string() \
               + ', "wins":' + str(self.win) + "}"
        return res.replace("'", '"').replace("True", "true").replace("False", "false")
