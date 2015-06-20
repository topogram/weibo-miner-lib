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

    from topogram.corpora.csv_file import CSVCorpus 
    
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

#### 2. Extractor : process your information

    from topogram.topograms.basic import BasicTopogram

    # init Chinese NLP
    nlp = ChineseNLP()

    # init with NLP analysis
    topogram = BasicTopogram(corpus=csv_corpus, processors=[nlp])

    # process  data
    topogram.process() 

#### 3. Visualizer : get your viz data

    # words network 
    words = topogram.words_to_d3js(max_nodes=200)

    # timeseries
    timeseries = topogram.get_timeseries(time_scale="minute")

    # select only the time frame between 2001 Jan 1 and Dec 31
    topogram.setTimeFrame(start=datetime(2000, 1, 1) , end=datetime(2001, 31, 12))

    # export map coordinates
    map = topogram.get_map(networks=["words"], projection="orthographic")


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
