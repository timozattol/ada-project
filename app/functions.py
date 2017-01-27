import pandas as pd
import numpy as np
import folium

from random import random

# ========== Tweet Selection ==========

def get_happy_sad_tweet(df, happy):
    """ Randomly selects a tweet from the happiest (`happy` = True) or saddest (`happy` = False) canton and returns it as a Serie"""
    # If df is empty return empty string
    if len(df) < 1:
        return ''
    if happy:
        selected_state = main_df_opinion.groupby("geo_state").mean().sort_values(by='sentiment', ascending=False).index[0]
    else:
        selected_state = main_df_opinion.groupby("geo_state").mean().sort_values(by='sentiment', ascending=False).index[-1]
    # getting indexes of tweets in the happiest/saddest state
    indexes = main_df_opinion[main_df_opinion['geo_state'] == selected_state]['main'].index
    # randomly selecting one of them
    indexes_list = list(indexes)
    random_index = int(random()*len(list(indexes)))
    tweet_selected_index = indexes_list[random_index]
    return main_df_opinion.loc[tweet_selected_index]

def random_tweets(df, number=10):
    number = min(len(df), number)

    if number > 0:
        return df.sample(number)
    else:
        return pd.DataFrame()

# ========== Sub-functions to filter data ==========

def filter_langs(df, langs):
    """ filter the df with one or several languages """
    return df[df['lang'].isin(langs)]

def filter_relevant_states(df, threshold):
    """ keep states that have more than `threshold` tweets """
    return df.groupby("geo_state").filter(lambda x: x.count()["main"] > threshold)

def append_weekday(df):
    df["weekday"] = df["published"].apply(lambda x: x.weekday())

def filter_weekday(df, days): #drop weekday after?
    return df[df['weekday'].isin(days)]

def filter_df(df, langs = ['en'], days = [0, 1, 2, 3, 4, 5, 6], threshold=0):
    """Filters the DataFrame according to language, weekdays, and threshold"""
    # Language filter
    df = filter_langs(df, langs)
    # Threshold filter if necessary
    if threshold > 0:
        df = filter_relevant_states(df, threshold)
    # Weekday filter
    append_weekday(df)
    df = filter_weekday(df, days)
    df = df.drop('weekday', 1)
    return df


# ========== Search & Count ==========


def search_df(df, search_terms, search_exclusive=False):
    """ Searches the df for either one of the terms. If `search_exclusive` is True, then searches the df for entries that have all terms """
    # Lowercase search terms
    search_terms = [t.lower() for t in search_terms]

    # Create a boolean array to subset the dataframe with search matching terms
    if search_exclusive:
        search_filter_bool = np.ones(len(df), dtype=bool)

        for term in search_terms:
            search_filter_bool = search_filter_bool & df['main'].str.lower().str.contains(term)
    else:
        search_filter_bool = np.zeros(len(df), dtype=bool)

        for term in search_terms:
            search_filter_bool = search_filter_bool | df['main'].str.lower().str.contains(term)

    return df[search_filter_bool]


def count_df(searched_df, main_df):
    """Propotion of tweets talking about a certain topic. Computation may be long.
    `searched_df` must have been done using the whole dataset! (not only neutral)
    Returns a dataframe"""
    topic_tweets = searched_df.groupby("geo_state")["sentiment"].count()
    total_tweets = main_df.groupby("geo_state")["sentiment"].count()
    return pd.DataFrame(topic_tweets/total_tweets)



# ========== Map Generation ==========

def generate_folium(df, method='metric_mean'):
    if method == 'metric_mean':
        df = df.groupby("geo_state").mean()
        thresh = [-0.66, -0.33, 0, 0.33, 0.66]
        colors = 'RdYlGn'
        legend = 'Happineess level 2016 per state'
    elif method == 'metric_count':
        thresh = [] #try different stuff
        colors = 'BuPu'
        legend = 'Proportion of tweets mentioning topic per canton'
    else:
        raise ValueError

    df = append_state_code(df)

    geo_path = '../utils/ch-cantons.topojson.json'

    folium_map = folium.Map(location=[46.8, 8.2], zoom_start=8)


    folium_map.choropleth(geo_path=geo_path,
                         data=df,
                         columns=['state_code', 'sentiment'],
                         key_on='feature.id',
                         topojson='objects.cantons',
                         threshold_scale=thresh,
                         fill_color=colors,
                         legend_name=legend
                        )
    return folium_map

def append_state_code(df):
    '''Adds state code in a new column, (semi-)in place'''

    state_to_code = {
        'Zurich': 'ZH',
        'Solothurn': 'SO',
        'Geneva': 'GE',
        'Lucerne': 'LU',
        'Thurgau': 'TG',
        'Jura': 'JU',
        'Grisons': 'GR',
        'Valais': 'VS',
        'Fribourg': 'FR',
        'Bern': 'BE',
        'Schaffhausen': 'SH',
        'Schwyz': 'SZ',
        'Vaud': 'VD',
        'Saint Gallen': 'SG',
        'Neuchâtel': 'NE',
        'Aargau': 'AG',
        'Ticino': 'TI',
        'Basel-City': 'BS',
        'Basel-Landschaft': 'BL',
        'Obwalden': 'OW',
        'Zug': 'ZG',
        'Uri': 'UR',
        'Glarus': 'GL',
        'Nidwalden': 'NW',
        'Appenzell Innerrhoden': 'AI',
        'Appenzell Ausserrhoden': 'AR'
    }

    df['state_code'] = [state_to_code[index] for index in df.index.values]

    # Create missing rows to match the json
    for state, state_code in state_to_code.items():
        if state_code not in df['state_code'].tolist():
            df = df.append(pd.Series({"state_code": state_code, "sentiment": 0}), ignore_index=True)

    return df
