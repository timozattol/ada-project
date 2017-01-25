#!/usr/bin/python3

from os import listdir
import subprocess
import pandas as pd
import numpy as np
import pickle

def sentiment_to_int(sentiment):
    '''Converts sentiment string to an integer'''
    if sentiment == "NEUTRAL":
        return 0
    elif sentiment == "POSITIVE":
        return 1
    elif sentiment == "NEGATIVE":
        return -1
    else:
        raise ValueError("Sentiment is invalid: {}".format(sentiment))

def json_to_df(path):
    '''Converts json from the harvester to a pandas DataFrame.
    Filters rows that contain all required_fields, and keep only
    the columns with useful fields'''
    fields = ["geo_state", "main", "sentiment",  "author_gender", "geo_country", "source_location", "published", "lang"]
    required_fields = ["geo_state", "sentiment"]

    with open(path) as file:
        json = pd.read_json(file)["_source"]

    filtered_json = []

    # Keep only relevant fields
    for j in json:
        filtered_json.append({field: j.get(field, None) for field in fields})

    # Filter out tweets witout state or sentiment
    dataframe = pd.DataFrame(filtered_json)

    dataframe.dropna(subset=required_fields, inplace=True)

    dataframe["sentiment_int"] = dataframe["sentiment"].apply(sentiment_to_int)

    return dataframe


if __name__ == "__main__":
    # To be launched from the entry node of the hdfs.
    # Copy a month of twitter data in a temporary folder, filter rows & columns.
    # Merge all days of a month and pickle the result.
    # Do this for every month.

    home = "/home/lottaz"
    harvest3r_path = "datasets/harvest3r_temp"
    twitter_data_path = "/datasets/goodcitylife/{}/harvest3r_twitter_data_*"
    pickle_path = "datasets/pickle"

    months = ['january',
              'february',
              'march',
              'april',
              'may',
              'june',
              'july',
              'august',
              'september',
              'october']

    # Empty the pickle folder
    subprocess.run("rm {}/{}/*".format(home, pickle_path), shell=True)

    # We know that geo_state does not occur before june
    for month in months[5:]:
        print("=={}==".format(month))

        # Empty the harvester folder
        subprocess.run("rm {}/{}/*".format(home, harvest3r_path), shell=True)

        # Copy a whole month from the hadoop file system to the harvester folder
        month_path = twitter_data_path.format(month)
        subprocess.run("hadoop fs -copyToLocal {} {}/{}/".format(month_path, home, harvest3r_path), shell=True)

        # Cumulative data frame for the month
        month_df = pd.DataFrame()

        for file_name in listdir("{}/{}/".format(home, harvest3r_path)):
            print("={}=".format(file_name))

            day_df = json_to_df("{}/{}/{}".format(home, harvest3r_path, file_name))
            month_df = month_df.append(day_df)

        # If the month contains tweets, pickle it for later use
        if len(month_df) > 0:
            df_path = "{}/{}/twitter_{}.pkl".format(home, pickle_path, month)

            with open(df_path, "wb") as handle:
                pickle.dump(month_df, handle)
