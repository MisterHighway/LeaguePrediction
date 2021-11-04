import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import accuracy_score
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor

def test(df):
    pd.set_option('display.max_columns', None)

    # array with selected game stats
    # avg_features = ['kills']
    avg_features = ['kills', 'deaths', 'assists', 'damageDealtToObjectives', 'dragonKills', 'goldEarned',
                    'totalDamageDealt', 'turretKills', 'visionScore', 'win']

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
    result_df = pd.DataFrame()
    for avg_feature in avg_features:
        result_df[avg_feature] = feature_df[avg_feature]

    print('\n-------------------- features dataframe (1) --------------------\n')
    print(result_df.columns)
    print('\n'+feature_df.head())


test(pd.read_csv('../Data/result_data_model.csv'))