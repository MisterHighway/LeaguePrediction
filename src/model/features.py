import pandas as pd
from file_writer import write


def create_features_1(df, features):
    pd.set_option('display.max_columns', None)
    match_df = df[['matchId', "game_result"]]
    # array with selected game stats
    avg_features = features

    # calculate features in feature_df
    feature_df = pd.DataFrame()

    for avg_feature in avg_features:
        # team blue
        feature_df[avg_feature + '_avg_team_blue'] = (df['summoner_1_' + avg_feature + '_avg']
                                                      + df['summoner_2_' + avg_feature + '_avg']
                                                      + df['summoner_3_' + avg_feature + '_avg']
                                                      + df['summoner_4_' + avg_feature + '_avg']
                                                      + df['summoner_5_' + avg_feature + '_avg']) / 5

        # team red
        feature_df[avg_feature + '_avg_team_red'] = (df['summoner_6_' + avg_feature + '_avg']
                                                     + df['summoner_7_' + avg_feature + '_avg']
                                                     + df['summoner_8_' + avg_feature + '_avg']
                                                     + df['summoner_9_' + avg_feature + '_avg']
                                                     + df['summoner_10_' + avg_feature + '_avg']) / 5

        feature_df[avg_feature] = ''
        for index, row in feature_df.iterrows():
            if row[avg_feature + '_avg_team_blue'] == row[avg_feature + '_avg_team_red']:
                feature_df.at[index, avg_feature] = 1
            if row[avg_feature + '_avg_team_blue'] > row[avg_feature + '_avg_team_red']:
                feature_df.at[index, avg_feature] = 1 + (
                            row[avg_feature + '_avg_team_red'] / row[avg_feature + '_avg_team_blue'])
            else:
                feature_df.at[index, avg_feature] = (
                            row[avg_feature + '_avg_team_blue'] / row[avg_feature + '_avg_team_red'])

    # select features from feature_df
    feature_result_df = df[['matchId']]
    for avg_feature in avg_features:
        feature_result_df.insert(1, avg_feature, feature_df[avg_feature])
        #feature_result_df[avg_feature] = feature_df[avg_feature]


    write('\n-------------------- features dataframe (1) --------------------\n')
    result_df = match_df.merge(feature_result_df, on='matchId', how='inner')
    result_df.to_csv('../data/features_1.csv')
    write(result_df.columns)
    write(' \n')
    # write(result_df.head())
    # return result_df

def create_features_2(df, features):
    pd.set_option('display.max_columns', None)
    match_df = df[['matchId', "game_result"]]
    # array with selected game stats
    avg_features = features

    # calculate features in feature_df
    feature_df = pd.DataFrame()

    for avg_feature in avg_features:
        # team blue
        feature_df[avg_feature + '_avg_team_blue'] = (df['summoner_1_' + avg_feature + '_avg']
                                                      + df['summoner_2_' + avg_feature + '_avg']
                                                      + df['summoner_3_' + avg_feature + '_avg']
                                                      + df['summoner_4_' + avg_feature + '_avg']
                                                      + df['summoner_5_' + avg_feature + '_avg']) / 5

        # team red
        feature_df[avg_feature + '_avg_team_red'] = (df['summoner_6_' + avg_feature + '_avg']
                                                     + df['summoner_7_' + avg_feature + '_avg']
                                                     + df['summoner_8_' + avg_feature + '_avg']
                                                     + df['summoner_9_' + avg_feature + '_avg']
                                                     + df['summoner_10_' + avg_feature + '_avg']) / 5

        feature_df[avg_feature] = ''
        for index, row in feature_df.iterrows():
            if row[avg_feature + '_avg_team_blue'] == row[avg_feature + '_avg_team_red']:
                feature_df.at[index, avg_feature] = 0
            if row[avg_feature + '_avg_team_blue'] > row[avg_feature + '_avg_team_red']:
                feature_df.at[index, avg_feature] = \
                    row[avg_feature + '_avg_team_red'] / row[avg_feature + '_avg_team_blue']
            else:
                feature_df.at[index, avg_feature] = \
                    (row[avg_feature + '_avg_team_blue'] / row[avg_feature + '_avg_team_red']) * (-1)

    # select features from feature_df
    feature_result_df = df[['matchId']]
    for avg_feature in avg_features:
        feature_result_df.insert(1, avg_feature, feature_df[avg_feature])
        #feature_result_df[avg_feature] = feature_df[avg_feature]


    write('\n-------------------- features dataframe (2) --------------------\n')
    result_df = match_df.merge(feature_result_df, on='matchId', how='inner')
    result_df.to_csv('../data/features_2.csv')
    write(result_df.columns)
    write('\n')
    # write(result_df.head())
    # return result_df