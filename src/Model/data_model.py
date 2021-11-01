class Match: # 1 call
    summoner1: None
    summoner2: None
    summoner3: None
    summoner4: None
    summoner5: None
    summoner6: None
    summoner7: None
    summoner8: None
    summoner9: None
    summoner10: None # 10 x summoner callen
    blue_win: None
    red_win: None # not blue_win
    t1_highest_winrate: None
    t2_highest_winrate: None
    t1_avg_winrate: None
    t2_avg_winrate: None

class Summoner:
    # feature related attributes
    matches: [] # match ids -->     50 matches + 1 calls
    champion: None
    winrate_overall: None # winrate last 100 games
    damage_done_avg: None

class MatchDto:
    # feature related attributes
    # from participants[participantDto] mit summoner puuid
    total_damage: None
    total_healing: None