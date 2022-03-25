import datetime
import json
import pickle
import pandas as pd


def station_name_to_coordinates(df):
    train_stations = pd.read_csv("website/analysis/train_stations.csv")
    df = pd.merge(df, train_stations, left_on='start_loc', right_on='Name Haltestelle')
    df = df.drop(columns=['abk_bahnhof', "Name Haltestelle"]).rename(columns={"lat": "lat_from", "lon": "lon_from"})
    df = pd.merge(df, train_stations, left_on='end_loc', right_on='Name Haltestelle')
    df = df.drop(columns=["abk_bahnhof", "Name Haltestelle", "start_loc", "end_loc"]).rename(columns={"lat": "lat_to", "lon": "lon_to"})
    return df


def estimate_capacity(df):
    model = pickle.load(open("website/model/capacity_model.pkl", "rb"))
    df_X = df[["day_of_week", "week", "start_hour", "line_category"]]
    return model.predict(df_X).astype(int)
    


def pre_process_data(df):
    df["start"] = pd.to_datetime(df["start"])
    df["end"] = pd.to_datetime(df["end"])
    df_with_coordinates = station_name_to_coordinates(df)
    df_with_coordinates["day_of_week"] = df_with_coordinates["start"].dt.day_of_week
    df_with_coordinates["week"] = df_with_coordinates["start"].dt.isocalendar().week.astype(int)
    print(df_with_coordinates["week"])
    with open("website/line_categories.json", "r") as json_file:
        json_categories = json.load(json_file)
        df_with_coordinates["line_category"] = df_with_coordinates["line"].replace(json_categories)
        print(df_with_coordinates["line_category"])
    df_data = df_with_coordinates.dropna()
    df_data["start_hour"] = df_data["start"].dt.hour
    df_data["travel_duration"] = (df_data["end"] - df_data["start"]).dt.total_seconds()//60
    df_data["capacity"] = estimate_capacity(df_data)
    df_data.drop(df_data[df_data["travel_duration"] < 0].index, inplace=True)
    df_data_feat_eng = df_data.drop(["start", "end", "line"], axis=1)
    return df_data_feat_eng
