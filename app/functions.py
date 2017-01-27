import numpy as np
import folium

def search_df(df, search_terms, search_exclusive=False):
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

def generate_folium(df):
    df_to_map = df.groupby("geo_state").mean()
    append_state_code(df_to_map)

    print(df_to_map)

    geo_path = '../utils/ch-cantons.topojson.json'

    folium_map = folium.Map(location=[46.57, 8], zoom_start=8)
    folium_map.choropleth(geo_path=geo_path,
                         data=df_to_map,
                         columns=['state_code', 'sentiment'],
                         key_on='feature.id',
                         topojson='objects.cantons',
                         fill_color='YlGn'
                        )
    return folium_map

def append_state_code(df):
    '''Adds state code in a new column, in place'''

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
