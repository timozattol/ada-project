from flask import Flask, send_file, request, render_template

import pandas as pd
import pickle
import os

from functions import search_df
from functions import generate_folium
from functions import filter_df
from functions import count_df
from functions import random_tweets

with open("../datasets/parsed_filtered_df.pkl", "rb") as handle:
       main_df = pickle.load(handle)
opinion_df = main_df[main_df['sentiment'] != 0]

# Set up map directory
if not os.path.exists('maps'):
    os.makedirs('maps')

app = Flask("opinion-map")

#def serve_map(search_query):
@app.route('/')
@app.route('/search/<search_query>')
@app.route('/search', methods=['GET', 'POST'])
def serve_map(search_query=None):
    print("REQUEST FORM IS")
    print(request.form)
    if request.form:
        search_query = request.form.get("search")
        langs = request.form.getlist("langs")
        matching_method = request.form.get("matching_method")
        metric_type = request.form.get("metric_type")
    else:
        # Default values
        langs = []
        matching_method = 'match_any'
        metric_type = 'metric_mean'

    file_path = "%s-%s-%s-%s" % (search_query, ":".join(langs), matching_method, metric_type)


    if metric_type == 'metric_count':
        df = main_df
    else:
        df = opinion_df

    if search_query:
        df = search_df(df, search_query.split(" "), search_exclusive=(matching_method == 'match_all'))

    if len(langs) > 0:
        df = filter_df(df, langs)

    selected_tweets = random_tweets(df)

    if metric_type == 'metric_count':
        df = count_df(df, main_df)

    folium_map = generate_folium(df, method=metric_type)

    folium_map.save("maps/map-test-%s.html" % file_path)


    return render_template('show_map.html',
        search_query=search_query,
        langs=langs,
        matching_method=matching_method,
        metric_type=metric_type,
        file_path=file_path,
        selected_tweets=selected_tweets
    )

@app.route('/map-test-<file_path>.html')
@app.route('/map-test-.html')
def show_map(file_path=None):
    # Get the folium map generated for this query
    return send_file('maps/map-test-%s.html' % file_path)

if __name__ == '__main__':
    app.run()
