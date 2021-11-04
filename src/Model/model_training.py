from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, accuracy_score, classification_report
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestClassifier


def train_model_1(df):
    # select features
    X = df[['kills', 'deaths', 'assists', 'damageDealtToObjectives', 'dragonKills', 'goldEarned',
                    'totalDamageDealt', 'turretKills', 'visionScore', 'win']]

    # select target object
    y = df.game_result

    # split into validation and training data
    train_X, val_X, train_y, val_y = train_test_split(X, y, test_size=0.33, random_state=1)

    # specify model
    prediction_model = DecisionTreeRegressor(random_state=1)

    # fit model with train_X and train_y
    prediction_model.fit(train_X, train_y)

    # predictions on val_X with model
    val_predictions = prediction_model.predict(val_X)
    print('\n---------- Decision Tree Regressor ----------\n')

    # calculate accuracy
    print('\naccuracy:')
    print(accuracy_score(val_y, val_predictions))

    print('\nmean absolute error:')
    print(mean_absolute_error(val_y, val_predictions))

    print('\nclassification report:')
    print(classification_report(val_y, val_predictions))
    return prediction_model

def train_model_2(df):
    # select features
    X = df[['kills', 'deaths', 'assists', 'damageDealtToObjectives', 'dragonKills', 'goldEarned',
                    'totalDamageDealt', 'turretKills', 'visionScore', 'win']]

    # select target object
    y = df.game_result

    # split into validation and training data
    train_X, val_X, train_y, val_y = train_test_split(X, y, test_size=0.33, random_state=1)

    # specify model
    prediction_model = RandomForestClassifier(random_state=1)

    # fit model with train_X and train_y
    prediction_model.fit(train_X, train_y)

    # predictions on val_X with model
    val_predictions = prediction_model.predict(val_X)
    print('\n---------- Random Forest Regressor ----------\n')

    # calculate accuracy
    print('\naccuracy:')
    print(accuracy_score(val_y, val_predictions))

    print('\nmean absolute error:')
    print(mean_absolute_error(val_y, val_predictions))

    print('\nclassification report:')
    print(classification_report(val_y, val_predictions))
    return prediction_model
