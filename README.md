# SwissFeels

SwissFeels, an interactive sentiment map of Switzerland, built for the EPFL Applied Data Analysis Autumn 2016 course

## Team
* [Brandon Le Sann](https://github.com/BrandonLS)
* [Timothée Lottaz](https://github.com/timozattol)
* [Seth Vanderwilt](https://github.com/sethv1)

## Abstract
The goal of our project was to analyze a large dataset of geolocated tweets and construct an interactive sentiment map of Switzerland, similar to that of [Happy Maps](http://goodcitylife.org/happymaps/). We focused on characterizing the sentiment of the tweets as positive or negative towards a certain entity, i.e. "is this tweet positive or negative about company X?". The objective was to have an interactive visualization that takes a keyword as input, for example "CFF" (Swiss national railway) and displays the sentiment of each canton on the Swiss map. 

## Data aquisition
The ADA course staff collected tweets from January to November 2016 that were geolocated in Switzerland. Each tweet was annotated with estimates of its language and sentiment. We filtered the original 50GB dataset to a more manageable collection of approximately 3.7 million tweets.

## Repository Contents

Data wrangling and analysis notebooks:
* [First look at the data fields and format](01dataset_partial_overview.ipynb)
* [Fetch the data we want from Hadoop cluster and store it locally](02data_processing.py)
* [Exploratory analysis of the data with aggregate statistics and sentiment](03data_exploration.ipynb)
* [Searching the dataset with a few different subjects](04applied_statistics.ipynb)
* [Test code for the Flask app](05_app_testing.ipynb)
* [Generate plots for our beautiful poster](06_poster_graphs.ipynb)

Interactive visualization webapp using Flask, pandas and Folium:
* [Flask webapp main code](app/app.py)
* [Backend data searching, map creation and tweet selection functions](app/functions.py)
* [App package requirements](app/requirements.txt)
* [Static logos and CSS](app/static/)
* [Webapp HTML templates](app/templates/)
* [TopoJSON file for Swiss canton boundaries](utils/ch-cantons.topojson.json)
* Note: The interactive viz saves every query result in the local directory _app/maps_

## Data format
The following fields were necessary in order to process the tweets:
* `geo_state`: the tweet's source canton
* `sentiment`: the tweet's sentiment, either Positive, Neutral or Negative.

We also decided to keep other interesting fields:
* `author_gender`: which can be MALE, FEMALE, or UNKNOWN
* `lang`: the language of the tweet
* `main`: the raw text of the tweet
* `published`: the date and time the tweet was published

## Data Cleaning / Issues

* There was one major issue with the dataset. The **geolocation** of the tweets was not collected prior to July 2016. This made ~60% of the data unusable.
* The `geo_state` field was often valid, but we had to filter out some **outliers** that were not Swiss cantons. These represented 0.4% of the data.
* Another minor issue was the **language detection**. Somehow Spanish seems to be spoken a lot more frequently than Italian (a national language)! Looking further into this problem we found that many Italian-language tweets were mislabeled as Spanish.
* Twitter **bots** were a problem that we couldn't satisfactorily address. For example many local radio stations automatically tweet their playlists, which polluted the dataset.
* The **sentiment analysis** algorithm worked poorly on **non-English** tweets.

## Result graphs

### Number of tweets in each language
![Languages](http://i.imgur.com/4WZbxpQ.png)

### Happiness with swiss railways
![Trains](http://i.imgur.com/nkXQuNv.png)

### Can we see the "röschtigraben"?
![Röschti](http://i.imgur.com/IGnqHm2.png)

### How do the swiss feel about Hillary and Donald?
![Presidency](http://i.imgur.com/IGnqHm2.png)

### Where is the biggest portuguese community?
![Portuguese community](http://i.imgur.com/ECaUsB1.png)

## Website
We built an interactive map of Switzerland that displays the mean sentiment of each Swiss canton. Thanks to the search function, it is possible to view the mean of a subset of tweets containing search terms such as "SBB CFF FFS". See the screenshots section for an example of mean sentiment. There's also an option to display a map of the proportion of tweets containing the search terms, as you can see in the screenshots section. Some matching tweets are displayed so that the user can verify that his/her query works well.

## Website screenshots

### Per-canton sentiment mean for "Brexit"
![Brexit](http://i.imgur.com/r7UvsWj.jpg)

### Per-canton mentions for "Skiing" or "Snowboarding"
![Ski](http://i.imgur.com/iFvCprJ.jpg)

## Poster
[A poster](poster.pdf) was also presented to the [Applied ML Days](https://www.appliedmldays.org/).

## Conclusion

Overall, the SwissFeels project performs quite well. Some queries are polluted by bots or spurious matches, as our current implementation simply searches for string occurrences in the raw text. However, many queries are very clear ("skiing", etc.) and give interesting results. Labeling tweets with entity mentions would provide more reliable search results in the current implementation.
