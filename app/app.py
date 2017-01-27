from flask import Flask, send_file, request, render_template

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

#def serve_map(search_query):
@app.route('/search/<search_query>')
@app.route('/search', methods=['GET', 'POST'])
def serve_map(search_query=None):
    print("REQUEST FORM IS")
    print(request.form)
    if request.form:
        print(request.form["search"])
        search_query = request.form.get("search")
        lang = request.form.get("lang")
        wk = request.form.get("wk")
        match = request.form.get("match")
        result_type = request.form.get("result_type")


    #TODO hook up to form
    if search_query:
        df = search_df(opinion_df, search_query.split(" "), search_exclusive=False)
    else:
        df = opinion_df

    folium_map = generate_folium(df)
    folium_map.save("maps/map-test-%s.html" % search_query)

    print(search_query)

    return render_template('show_map.html', search_query=search_query)

@app.route('/map-test-<search_query>.html')
def show_map(search_query):
    # Get the folium map generated for this query
    return send_file('maps/map-test-%s.html' % search_query)

if __name__ == '__main__':
    app.run()
