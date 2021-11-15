import pandas as pd
from joblib import dump, load
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, accuracy_score, classification_report
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier

from src.model.features import create_features_1
from src.model.file_writer import write
from src.model.data_processing import process_data


def train_model(df, classifier):
    # select features
    X = df[['kills', 'deaths', 'assists', 'damageDealtToObjectives', 'dragonKills', 'goldEarned',
            'totalDamageDealt', 'turretKills', 'visionScore', 'win']]

    # select target object
    y = df.game_result

    # split into validation and training data
    train_X, val_X, train_y, val_y = train_test_split(X, y, test_size=0.3, random_state=2)

    # specify model
    prediction_model = None

    if classifier == 1:
        prediction_model = RandomForestClassifier(random_state=3, max_depth=8)
        write('---------- Random Forest Classifier ----------\n')
    elif classifier == 2:
        prediction_model = DecisionTreeClassifier(random_state=3)
        write('---------- Decision Tree Classifier ----------\n')
    elif classifier == 3:
        prediction_model = MLPClassifier(random_state=3)
        write('---------- MLP Classifier ----------\n')
    elif classifier == 4:
        prediction_model = KNeighborsClassifier(n_neighbors=5)
        write('---------- K Neighbors Classifier ----------\n')
    else:
        print('\n---------- Select Classifier! ----------\n')

    # fit model with train_X and train_y
    if prediction_model is not None:
        prediction_model.fit(train_X, train_y)

        # predictions on val_X with model
        val_predictions = prediction_model.predict(val_X)

        # calculate accuracy

        write('\naccuracy:\n')
        write(accuracy_score(val_y, val_predictions))

        write('\nmean absolute error:\n')
        write(mean_absolute_error(val_y, val_predictions))

        write('\nclassification report:\n')
        write(classification_report(val_y, val_predictions))
        return prediction_model
    else:
        write('\n---------- prediction_model is none ----------\n')


def save_model(model, name):
    dump(model, '../model/trained_models/' + name + '.joblib')


def load_model(name):
    return load('../model/trained_models/' + name + '.joblib')


def predict_with_model(model, csv_path):

    # select features
    features = ['kills', 'deaths', 'assists', 'damageDealtToObjectives', 'dragonKills', 'goldEarned',
                'totalDamageDealt', 'turretKills', 'visionScore', 'win']

    # read and process data of match
    match_df = pd.read_csv(csv_path)
    processed_match_df = process_data(match_df, features)

    # create features (1)
    create_features_1(processed_match_df, features)
    features_1 = pd.read_csv('../tmp/features_1.csv')

    feature_result = features_1.drop(['Unnamed: 0', 'matchId', 'game_result'], axis=1)

    # return prediction on input features
    return model.predict(feature_result)
