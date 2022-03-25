import pickle

from numpy import argmin


def load_model(filename):
    model = pickle.load(open(filename, "rb"))
    return model

def get_latest_reservation_ts(model, df):
    y_pred = model.predict(df)
    return min(y_pred), argmin(y_pred)
    