import json

import pandas as pd


def process_data(source_file):
    pd.set_option('display.max_columns', None)

    # read local csv data
    print('\n')
    matches_source_df = pd.read_csv(source_file)

    # matches
    matches_df = matches_source_df[['matchId', 'wins']]

    # create summoner dataframes
    print('\n')
    summoner_1 = matches_source_df[['matchId', 'Summoner1.match_history']]
    summoner_2 = matches_source_df[['matchId', 'Summoner2.match_history']]
    summoner_3 = matches_source_df[['matchId', 'Summoner3.match_history']]
    # summoner_4 = matches_source_df[['matchId', 'Summoner4.match_history']]
    summoner_5 = matches_source_df[['matchId', 'Summoner5.match_history']]
    summoner_6 = matches_source_df[['matchId', 'Summoner6.match_history']]
    # summoner_7 = matches_source_df[['matchId', 'Summoner7.match_history']]
    # summoner_8 = matches_source_df[['matchId', 'Summoner8.match_history']]
    # summoner_9 = matches_source_df[['matchId', 'Summoner9.match_history']]
    summoner_10 = matches_source_df[['matchId', 'Summoner10.match_history']]

    # array with selected game stats
    avg_features = ['kills', 'deaths', 'assists']

    # create avg features for each summoner (player)
    summoner_1 = create_avg_features(summoner_1, '1', avg_features)
    summoner_2 = create_avg_features(summoner_2, '2', avg_features)
    summoner_3 = create_avg_features(summoner_3, '3', avg_features)
    # summoner_4 = create_avg_feature(summoner_4, '4', avg_features)
    summoner_5 = create_avg_features(summoner_5, '5', avg_features)
    summoner_6 = create_avg_features(summoner_6, '6', avg_features)
    # summoner_7 = create_avg_feature(summoner_7, '7', avg_features)
    # summoner_8 = create_avg_feature(summoner_8, '8', avg_features)
    # summoner_9 = create_avg_feature(summoner_9, '9', avg_features)
    summoner_10 = create_avg_features(summoner_10, '10', avg_features)

    print('\n-------------------- sommoner dataframes --------------------\n')
    print(summoner_1)
    print('\n')
    print(summoner_2)
    print('\n')
    print(summoner_3)
    print('\n')
    print(summoner_5)
    print('\n')
    print(summoner_6)
    print('\n')
    print(summoner_10)

    # join matches_df with summoner dataframes
    matches_df = pd.merge(matches_df, summoner_1, on='matchId', how='inner')
    matches_df = pd.merge(matches_df, summoner_2, on='matchId', how='inner')
    matches_df = pd.merge(matches_df, summoner_3, on='matchId', how='inner')
    # matches_df = pd.merge(matches_df, summoner_4, on='matchId', how='inner')
    matches_df = pd.merge(matches_df, summoner_5, on='matchId', how='inner')
    matches_df = pd.merge(matches_df, summoner_6, on='matchId', how='inner')
    #  matches_df = pd.merge(matches_df, summoner_7, on='matchId', how='inner')
    # matches_df = pd.merge(matches_df, summoner_8, on='matchId', how='inner')
    # matches_df = pd.merge(matches_df, summoner_9, on='matchId', how='inner')
    matches_df = pd.merge(matches_df, summoner_10, on='matchId', how='inner')

    # write csv file
    print('\n-------------------- result dataframe --------------------\n')
    print(matches_df.columns)
    matches_df.to_csv("../Data/result_data_model.csv")


def create_avg_features(summoner_dataframe, summoner_number, avg_features):
    # iterate over avg_features
    for avg_feature in avg_features:
        # create feature columns
        summoner_dataframe.insert(2, 'summoner_' + summoner_number + '_' + avg_feature + '_avg', '')
        # iterate over
        for index, row in summoner_dataframe.iterrows():
            # transform and load json
            match_history = '{"match_history":' + row['Summoner' + summoner_number + '.match_history']\
                .replace("'", '"').replace("True", "true").replace("False", "false") + '}'
            match_history_json = json.loads(match_history)['match_history']

            # set counters
            match_count = 0
            features_count = 0

            # iterate over in game stats
            for x in match_history_json:
                match_count += 1
                features_count += x['in_game_stats'][avg_feature]

            # calculate features
            row['summoner_' + summoner_number + '_' + avg_feature + '_avg'] = features_count / match_count

    return summoner_dataframe.drop('Summoner' + summoner_number + '.match_history', 1)


process_data("../Model/matches.csv")
