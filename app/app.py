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
        lang = request.form.getlist("lang")
        wk = request.form.getlist("wk")
        match = request.form.get("match")
        result_type = request.form.get("result_type")
#       return redirect('/search/%s' % search_query)
        #DEBUG
        print(search_query)
        print(lang)
        print(wk)
        print(match)
        print(result_type)

    # TODO steps
    # create base search box, map
    # stuff with pandas

    #TODO hook up to form
    if search_query:
        #SLOW but keeps neutral sentiments
        #df = search_df(main_df, search_query.split(" "), search_exclusive=False)
        df = search_df(opinion_df, search_query.split(" "), search_exclusive=False)
    else:
        df = opinion_df

    folium_map = generate_folium(df)
    folium_map.save("maps/map-test-%s.html" % search_query)

    print(search_query)
    #old form stuff
    return """
    <form id="searchbox" action="/search" method="post">
        <input name="search" type="text" placeholder="Type here"/>
        <input type="submit" value="Search"/>
        <label> <input name="lang" value="lang1" type="checkbox" />lang1</label>
        <label> <input name="lang" value="lang2" type="checkbox" />lang2</label>
        <label> <input name="lang" value="lang3" type="checkbox" />lang3</label>
        <label> <input name="wk" value="weekday" type="checkbox" />weekday</label>
        <label> <input name="wk" value="weekend" type="checkbox" />weekend</label>
        <label> <input name="match" value="all" type="radio" />all</label>
        <label> <input name="match" value="any" type="radio" />any</label>
        <label> <input name="result_type" value="mean sentiment" type="radio" />mean sentiment</label>
        <label> <input name="result_type" value="count" type="radio" />count</label>

    </form>

    <iframe src="/map-test-%s.html" width="100%%" height="80%%">iframe debug text between tags</iframe>
    """ % search_query

@app.route('/map-test-<search_query>.html')
def show_map(search_query):
    # Get the folium map generated for this query
    return send_file('maps/map-test-%s.html' % search_query)

@app.route('/test')
def test():

    return render_template('show_map.html')

#TODO could serve some
#@app.route('/<mapname>.html')

if __name__ == '__main__':
    app.run()
