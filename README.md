# Topogram 

[![Build Status](https://travis-ci.org/topogram/topogram.svg?branch=master)](https://travis-ci.org/topogram/topogram)  [![Coverage Status](https://coveralls.io/repos/topogram/topogram/badge.svg?branch=master)](https://coveralls.io/r/topogram/topogram?branch=master) [![Documentation Status](https://readthedocs.org/projects/topogram/badge/?version=latest)](https://readthedocs.org/projects/topogram/?badge=latest)
<!-- [ ![Codeship Status for topogram/topogram](https://codeship.com/projects/2255a810-f8c9-0132-7d84-76682d16c2d4/status?branch=master)](https://codeship.com/projects/86696) -->


Topogram is a data mining library to produce time-based networks and maps from text data. 


## About

With tools for validation and parsing, Topogram provides a pipeline to create visualizations of relationships between multiple entities like people, words, time and places. Based on [networkx](http://netwokx.readthedocs.org), [NLTK](http://www.nltk.org) and [d3js](http://d3js.org), it provides a complete toolkit to create advanced social network analysis from raw datasets. 

Read the complete documentation at [topogram.readthedocs.org](http://topogram.readthedocs.org)


## Usage

Topogram relies on three core components : corpus, extractors  and visualizers.

#### 1. Corpus : describe your dataset

```python

from topogram.corpus.csv_file import CSVCorpus 

# import corpus
csv_corpus = CSVCorpus('data.csv',
    source_column="user_id",
    text_column="text",
    timestamp_column="created_at",
    time_pattern="%Y-%m-%d %H:%M:%S",
    additional_columns=["permission_denied", "deleted_last_seen"])

# validate corpus formatting
try :
    csv_corpus.validate()
except ValueError, e:
    print e.message, 422

```

#### 2. Processor : extract your information

```python

from topogram import Topogram
from topogram.processors.nlp import NLP
from topogram.processors.regexp import Regexp

# init processors
chinese_nlp = NLP("zh")
url = Regexp(r"\b(([\w-]+://?|www[.])[^\s()<>]+(?:\([\w\d]+\)|([^\p{P}\s]|/)))")

# init 
topogram = Topogram(corpus=csv_corpus, processors=[("zh", chinese_nlp), ("urls", url)])
```

#### 3. Visualizer : get your viz data

```python

from topogram.vizparsers.network import Network

# create viz model
words_network = Network( directed=False )

for row in topogram.process():
    words_network.add_edges_from_nodes_list(row["zh"])

# get processed graph as d3js json
print words_network.get(nodes_count=1000, min_edge_weight=3, json=True)
```

#### More options

```python
# timeseries
timeseries = topogram.get_timeseries(time_scale="minute")

# select only the time frame between 2001 Jan 1 and Dec 31
topogram.setTimeFrame(start=datetime(2000, 1, 1) , end=datetime(2001, 31, 12))

# export map coordinates
map = topogram.get_map(networks=["words"], projection="orthographic")
```

## Install

    pip install topogram

or 

    pip install git://github.com/topogram/topogram.git#egg=topogram

## Troubleshooting

Topogram is still in beta. 

If you have any trouble or questions, please [open an issue](https://github.com/topogram/topogram/issues). We'll do our best to help you solve it. 

## Development

Topogram is under development. Code and pull requests are very welcome.

#### Tests

    pip install -r dev_requirements.txt 
    make test

#### Documentation

Build the documentation (with sphinx)

    make documentation 
    make upload-docs # publish online 
