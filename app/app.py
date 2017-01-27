from flask import Flask
import pandas as pd
import pickle

from functions import search_df
from functions import generate_folium

with open("../datasets/parsed_filtered_df.pkl", "rb") as handle:
       main_df = pickle.load(handle)

opinion_df = main_df[main_df['sentiment'] != 0]

app = Flask("opinion-map")

@app.route('/search/<search_query>')
def serve_map(search_query):
    # TODO steps
    # create base search box, map
    # stuff with pandas

    if search_query:
        df = search_df(opinion_df, search_query.split(" "), search_exclusive=True)
    else:
        df = opinion_df

    folium_map = generate_folium(df)
    folium_map.save("map-test.html")

    return df.__repr__()

if __name__ == '__main__':
    app.run()
