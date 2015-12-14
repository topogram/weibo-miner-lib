# Topogram 

[![Build Status](https://travis-ci.org/topogram/topogram.svg?branch=master)](https://travis-ci.org/topogram/topogram)  [![Coverage Status](https://coveralls.io/repos/topogram/topogram/badge.svg?branch=master)](https://coveralls.io/r/topogram/topogram?branch=master) [![Documentation Status](https://readthedocs.org/projects/topogram/badge/?version=latest)](https://readthedocs.org/projects/topogram/?badge=latest)
<!-- [ ![Codeship Status for topogram/topogram](https://codeship.com/projects/2255a810-f8c9-0132-7d84-76682d16c2d4/status?branch=master)](https://codeship.com/projects/86696) -->


Topogram is a data mining library to produce time-based networks and maps from text data. 


## About

With tools for validation and parsing, Topogram provides a pipeline to create visualizations of relationships between multiple entities like people, words, time and places. Based on [networkx](http://netwokx.readthedocs.org), [NLTK](http://www.nltk.org) and [d3js](http://d3js.org), it provides a complete toolkit to create advanced social network analysis from raw datasets. 



## Usage

Read the documentation at [topogram.readthedocs.org](http://topogram.readthedocs.org)


## Install

    pip install topogram

or 

    pip install git+http://github.com/topogram/topogram.git#egg=topogram

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
