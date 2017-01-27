from flask import Flask, send_file, request, render_template

import pandas as pd
import pickle
import os

from functions import search_df
from functions import generate_folium
from functions import filter_df
from functions import count_df

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
        search_query = request.form.get("search")
        lang = request.form.getlist("lang")
        weekdays = request.form.getlist("weekdays")
        matching_method = request.form.get("matching_method")
        metric_type = request.form.get("metric_type")
    else:
        # Default values
        lang = []
        weekdays = []
        matching_method = 'match_any'
        metric_type = 'metric_mean'


    if search_query:
        ##df = search_df(opinion_df, search_query.split(" "), search_exclusive=False)
        df = search_df(main_df, search_query.split(" "), search_exclusive=False)
    else:
        df = opinion_df

    #df = filter_df(df, ['en'], [0, 1, 2])

    
    ## TODO count df should be done on main_df 
    df_count = count_df(df, main_df)
    #folium_map = generate_folium(df)
    folium_map = generate_folium(df_count, count=True)
    folium_map.save("maps/map-test-%s.html" % search_query)

    return render_template('show_map.html',
        search_query=search_query,
        lang=lang,
        matching_method=matching_method,
        metric_type=metric_type
    )

@app.route('/map-test-<search_query>.html')
@app.route('/map-test-.html')
def show_map(search_query=None):
    # Get the folium map generated for this query
    return send_file('maps/map-test-%s.html' % search_query)

if __name__ == '__main__':
    app.run()
