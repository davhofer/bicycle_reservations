import pandas as pd
parse_dates = ["start", "end", "travel_date", "latest_res_dt"]
df = pd.read_csv("website/model_data.csv", parse_dates=parse_dates)
df_book_in_advance = pd.to_timedelta(df["start"] - df["latest_res_dt"], unit="m").dt.total_seconds()//60
df_book_in_advance.drop(df_book_in_advance[df_book_in_advance < 0].index, inplace=True)
df["book_in_advance"] = df_book_in_advance
df["day_of_week"] = df["travel_date"].dt.day_of_week
df["week"] = df["travel_date"].dt.isocalendar().week
df["month"] = df["travel_date"].dt.month
df_data = df.drop(["count", "travel_date"], axis=1)
train_stations = pd.read_csv("data_preprocessed/dienststellen.csv")[["abk_bahnhof", "Name Haltestelle", "lat", "lon"]].dropna()
# full join for start train station 
df = pd.merge(df, train_stations, left_on='start_loc', right_on='abk_bahnhof')
df = df.drop(columns=['abk_bahnhof', "Name Haltestelle"]).rename(columns={"lat": "lat_from", "lon": "lon_from"})

# full join for destination
df = pd.merge(df, train_stations, left_on='end_loc', right_on='abk_bahnhof')
df = df.drop(columns=["abk_bahnhof", "Name Haltestelle"]).rename(columns={"lat": "lat_to", "lon": "lon_to"})
station_mapping = {}
for _, row in train_stations.iterrows():
    station_mapping[row["abk_bahnhof"]] = row["Name Haltestelle"]

df_book_in_advance = df[df["book_in_advance"] > 0]
booked_in_advance_grouped = df_book_in_advance.groupby(by=["start_loc", "end_loc"])["book_in_advance"].count().reset_index()
booked_in_advance_grouped = booked_in_advance_grouped.sort_values(["book_in_advance"], ascending=False)

grouped_by_month = df_book_in_advance.groupby(by=["month", "start_loc", "end_loc"])["book_in_advance"].count().reset_index()
grouped_by_month = grouped_by_month.sort_values("book_in_advance", ascending=False)
for month in range(3,11):
    #grouped_by_month[grouped_by_month["month"] == month].replace(station_mapping).to_csv(f"busiest_tracks/{month}-21.csv", index=False)
    display(grouped_by_month[grouped_by_month["month"] == month].replace(station_mapping))


all_stations = sorted(set(df["start_loc"].replace(station_mapping)))
df_book_in_advance = df[df["book_in_advance"] > 0]
booked_in_advance_grouped_coord = df_book_in_advance.groupby(by=["lat_from", "lon_from", "lat_to", "lon_to"])["book_in_advance"].count().reset_index()
booked_in_advance_grouped_coord = booked_in_advance_grouped_coord.sort_values(["book_in_advance"], ascending=False)

import numpy as np
IC_train_stations = train_stations[np.isin(train_stations["Name Haltestelle"], all_stations)]

import plotly.graph_objects as go

fig = go.Figure(
    layout=go.Layout(
        showlegend= False,
        height=800, 
        width=1200, 
        geo = {
            "center": {
                "lat": 46.818188,
                "lon": 8.227512
            },
            "lataxis": {"range": [44, 47]},
            "lonaxis": {"range": [5, 10]},
        }
    )
)

fig.add_trace(go.Scattergeo(
    lon = IC_train_stations['lon'],
    lat = IC_train_stations['lat'],
    text = IC_train_stations['Name Haltestelle'],
    mode = 'markers',
    hoverinfo = "text",
    marker = dict(
        size = 5,
        color = 'rgb(255, 0, 0)',
        line = dict(
            width = 3,
            color = 'rgba(68, 68, 68, 0)'
        )
    )))

for i in range(len(booked_in_advance_grouped_coord)):
    fig.add_trace(
        go.Scattergeo(
            lon = [booked_in_advance_grouped_coord['lon_from'][i], booked_in_advance_grouped_coord['lon_to'][i]],
            lat = [booked_in_advance_grouped_coord['lat_from'][i], booked_in_advance_grouped_coord['lat_to'][i]],
            mode = 'lines',
            hoverinfo = "skip",
            line = dict(width = 5,color = 'red'),
            opacity = float(booked_in_advance_grouped_coord['book_in_advance'][i]) / float(booked_in_advance_grouped_coord['book_in_advance'].max()),
        )
    )

fig.update_geos(
    visible=False, resolution=50,
    showcountries=True, countrycolor="Black",
    showsubunits=True, subunitcolor="Blue"
)

fig.show()

#import plotly.express as px

#fig = px.scatter(x=range(10), y=range(10))
#fig.write_html("path/to/file.html")
