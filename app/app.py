from flask import Flask, send_file
import pandas as pd
import pickle
import os

from functions import search_df
from functions import generate_folium

with open("../datasets/parsed_filtered_df.pkl", "rb") as handle:
       main_df = pickle.load(handle)

opinion_df = main_df[main_df['sentiment'] != 0]

# Set up map directory
if not os.path.exists('maps'):
    os.makedirs('maps')

app = Flask("opinion-map")

@app.route('/search/<search_query>')
def serve_map(search_query):
    # TODO steps
    # create base search box, map
    # stuff with pandas

    if search_query:
        df = search_df(opinion_df, search_query.split(" "), search_exclusive=False)
    else:
        df = opinion_df

    folium_map = generate_folium(df)
    folium_map.save("maps/map-test-%s.html" % search_query)

    print(search_query)
    return """
    <iframe src="/map-test-%s.html" width="100%%" height="80%%">iframe debug text between tags</iframe>
    """ % search_query

@app.route('/map-test-<search_query>.html')
def show_map(search_query):
    # Get the folium map generated for this query
    return send_file('maps/map-test-%s.html' % search_query)

#TODO could serve some
#@app.route('/<mapname>.html')

if __name__ == '__main__':
    app.run()
