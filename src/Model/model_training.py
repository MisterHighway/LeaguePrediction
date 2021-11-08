from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, accuracy_score, classification_report
from sklearn.neural_network import MLPClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from src.Model.file_writer import write


def train_model(df, classifier):
    # select features
    X = df[['kills', 'deaths', 'assists', 'damageDealtToObjectives', 'dragonKills', 'goldEarned',
            'totalDamageDealt', 'turretKills', 'visionScore', 'win']]

    # select target object
    y = df.game_result

    # split into validation and training data
    train_X, val_X, train_y, val_y = train_test_split(X, y, test_size=0.35, random_state=4)

    # specify model
    prediction_model = None

    if classifier == 1:
        prediction_model = RandomForestClassifier(random_state=1)
        write('---------- Random Forest Classifier ----------\n')
    elif classifier == 2:
        prediction_model = DecisionTreeClassifier(random_state=1)
        write('---------- Decision Tree Classifier ----------\n')
    elif classifier == 3:
        prediction_model = MLPClassifier(random_state=1)
        write('---------- MLP Classifier ----------\n')
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