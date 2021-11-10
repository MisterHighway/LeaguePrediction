import json
import pandas as pd
from src.model.file_writer import write


def process_data(df, features):
    pd.set_option('display.max_columns', None)

    # create matches_df, game_result = 1 => blue team wins
    matches_df = df[['matchId', 'wins']]
    matches_df.insert(2, 'game_result', 'null')
    # print(matches_df)
    for index, row in matches_df.iterrows():
        # print(row['wins'])
        if row.wins == True:
            matches_df.at[index, 'game_result'] = '1'
        else:
            matches_df.at[index, 'game_result'] = '0'
    #print(matches_df.head())
    matches_df = matches_df.drop('wins', 1)

    # create summoner dataframes
    summoner_1 = df[['matchId', 'Summoner1.match_history']]
    summoner_2 = df[['matchId', 'Summoner2.match_history']]
    summoner_3 = df[['matchId', 'Summoner3.match_history']]
    summoner_4 = df[['matchId', 'Summoner4.match_history']]
    summoner_5 = df[['matchId', 'Summoner5.match_history']]
    summoner_6 = df[['matchId', 'Summoner6.match_history']]
    summoner_7 = df[['matchId', 'Summoner7.match_history']]
    summoner_8 = df[['matchId', 'Summoner8.match_history']]
    summoner_9 = df[['matchId', 'Summoner9.match_history']]
    summoner_10 = df[['matchId', 'Summoner10.match_history']]

    # array with selected game stats
    avg_features = features

    # create avg features for each summoner (player)
    summoner_1 = create_avg_features(summoner_1, '1', avg_features)
    summoner_2 = create_avg_features(summoner_2, '2', avg_features)
    summoner_3 = create_avg_features(summoner_3, '3', avg_features)
    summoner_4 = create_avg_features(summoner_4, '4', avg_features)
    summoner_5 = create_avg_features(summoner_5, '5', avg_features)
    summoner_6 = create_avg_features(summoner_6, '6', avg_features)
    summoner_7 = create_avg_features(summoner_7, '7', avg_features)
    summoner_8 = create_avg_features(summoner_8, '8', avg_features)
    summoner_9 = create_avg_features(summoner_9, '9', avg_features)
    summoner_10 = create_avg_features(summoner_10, '10', avg_features)

    # join matches_df with summoner dataframes
    matches_df = pd.merge(matches_df, summoner_1, on='matchId', how='inner')
    matches_df = pd.merge(matches_df, summoner_2, on='matchId', how='inner')
    matches_df = pd.merge(matches_df, summoner_3, on='matchId', how='inner')
    matches_df = pd.merge(matches_df, summoner_4, on='matchId', how='inner')
    matches_df = pd.merge(matches_df, summoner_5, on='matchId', how='inner')
    matches_df = pd.merge(matches_df, summoner_6, on='matchId', how='inner')
    matches_df = pd.merge(matches_df, summoner_7, on='matchId', how='inner')
    matches_df = pd.merge(matches_df, summoner_8, on='matchId', how='inner')
    matches_df = pd.merge(matches_df, summoner_9, on='matchId', how='inner')
    matches_df = pd.merge(matches_df, summoner_10, on='matchId', how='inner')

    # write csv file
    write('-------------------- result dataframe --------------------\n')
    matches_df.to_csv('../data/result_data_model.csv')
    write(matches_df.columns)
    # write(matches_df.head())
    return matches_df


def create_avg_features(summoner_dataframe, summoner_number, avg_features):
    # iterate over avg_features
    for avg_feature in avg_features:

        # create feature columns
        summoner_dataframe.insert(2, 'summoner_' + summoner_number + '_' + avg_feature + '_avg', '')

        # iterate over
        for index, row in summoner_dataframe.iterrows():

            # transform and load json
            match_history = '{"match_history":' + row['Summoner' + summoner_number + '.match_history'] \
                .replace("'", '"').replace("True", "true").replace("False", "false") + '}'
            match_history_json = json.loads(match_history)['match_history']

            # set counters
            match_count = 0
            features_count = 0
            none_count = 0

            # iterate over in game stats
            for x in match_history_json:
                if x['in_game_stats'] == 'None':
                    none_count += 1
                else:
                    match_count += 1
                    features_count += x['in_game_stats'][str(avg_feature)]
                    # if avg_feature == 'win': print('features_count: '+str(x['in_game_stats'][str(avg_feature)]))

            # calculate avg
            row['summoner_' + summoner_number + '_' + avg_feature + '_avg'] = features_count / (
                        match_count - none_count)
            # if avg_feature == 'win': print('AVG : ' + str(features_count / (match_count - none_count)))
    return summoner_dataframe.drop('Summoner' + summoner_number + '.match_history', 1)
