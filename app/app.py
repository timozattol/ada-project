from flask import Flask
import pandas as pd
import pickle

#with open("datasets/parsed_filtered_df.pkl", "rb") as handle:
#       main_df = pickle.load(handle)

app = Flask("opinion-map")

@app.route('/<search_query>')
def serve_map(search_query):
    # TODO steps
    # create base search box, map
    # stuff with pandas
    return search_query

if __name__ == '__main__':
    app.run()
