import pandas as pd
from src.Model.data_processing import process_data
from src.Model.features import create_features_1, create_features_2
from src.Model.file_writer import write, read_log
from src.Model.model_training import train_model

# select in game statistics features
features = ['kills', 'deaths', 'assists', 'damageDealtToObjectives', 'dragonKills', 'goldEarned',
                    'totalDamageDealt', 'turretKills', 'visionScore', 'win']

# read and process csv data generated by api script
matches_2 = pd.read_csv('../Data/matches2.csv')
matches_3 = pd.read_csv('../Data/matches3.csv')
matches_4 = pd.read_csv('../Data/matches4.csv')
matches_5 = pd.read_csv('../Data/matches5.csv')
result_matches = pd.concat([matches_2, matches_3, matches_4, matches_5], ignore_index=True)
result_matches.to_csv('../Data/match.csv')
result_data_model = process_data(result_matches, features)

# check result data model
write('\ndescription:')
write(result_data_model[['matchId', 'game_result', 'summoner_1_win_avg']].describe())
write(result_data_model.shape[0])

# create features with result_data_model
create_features_1(result_data_model, features)
create_features_2(result_data_model, features)

# train prediction model
model_1 = train_model(pd.read_csv('../Data/features_1.csv'), 1)
model_2 = train_model(pd.read_csv('../Data/features_2.csv'), 2)
# model_2 = train_model(pd.read_csv('../Data/features_2.csv'), 3)

print(read_log())


