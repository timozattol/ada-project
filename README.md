Repository for the EPFL Applied Data Analysis Autumn 2016 course project

# Team
- Brandon Le Sann
- Timothée Lottaz
- Seth Vanderwilt

# Abstract
The goal of the project is to analyze a set of geolocated tweets in Switzerland and construct a map of Switzerland similar to that of [Happy Maps](http://goodcitylife.org/happymaps/). We will focus on characterizing the sentiment of the tweets as positive or negative towards a certain entity, i.e. "is this tweet positive or negative about company X?". We will create an interactive map that takes a keyword as input, such as "CFF" (Swiss national railway). The map will aggregate the geotagged tweets containing this keyword and show the local average "positivity" of these tweets on a heamap.

# Data description
Geolocalized tweets from January-August 2016, located in Switzerland, gathered by ADA course staff. TODO ask for more details/license?

# Feasibility and Risks
The main challenges of the project are:
* Big data: the dataset is huge and we might need to use a cluster to process all of the data.
* Sparsity: Swiss people are not known to be active on Twitter, and the regions outside of the big cities may only contain limited information.
* Multiple languages: given its cultural diversity and international touristic appeal, Swiss Twitter contains tweets in English, French, Swiss-German, Swiss-Italian and many other languages! This complicates our sentiment analysis pipeline - potential solutions could be to only consider only consider tweets in English or to translate all tweets to English before extracting sentiment.
* Other?

# Deliverables
The deliverables are:
* The interactive visualization (map!)
* The source code of the project
* An iPython notebook or PDF presenting the main results, such as maps, tables and statistical analysis

# Timeplan
?
