import pandas as pd

def process_data():
    de_videos_df = pd.read_csv("/Users/Izana Bizuneh/PycharmProjects/LeaguePrediction/src/Data/DEvideos.csv")
    de_videos_df.to_csv("/Users/Izana Bizuneh/PycharmProjects/LeaguePrediction/src/Data/result.csv")
