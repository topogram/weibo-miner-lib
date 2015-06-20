# Topogram -- text networks analysis in Python  

[![Build Status](https://travis-ci.org/topogram/topogram.svg?branch=master)](https://travis-ci.org/topogram/topogram)  [![Coverage Status](https://coveralls.io/repos/topogram/topogram/badge.svg?branch=master)](https://coveralls.io/r/topogram/topogram?branch=master) [![Documentation Status](https://readthedocs.org/projects/topogram/badge/?version=latest)](https://readthedocs.org/projects/topogram/?badge=latest)
<!-- [ ![Codeship Status for topogram/topogram](https://codeship.com/projects/2255a810-f8c9-0132-7d84-76682d16c2d4/status?branch=master)](https://codeship.com/projects/86696) -->

Topogram is a  Python library for extracting and visualizing *networks of words and citations* from raw data (Twitter, Weibo, news, etc...) Target audience is developers, researchers, journalists interested in an easy way to analyze texts.

Documentation available at [topogram.readthedocs.org](http://topogram.readthedocs.org)

### Features

* Support for large corpora
* Citations graph
* Word co-occurence graph
* Time-based anlaysis (hour, day, month, year... )
* Community detection (Louvain algorithm)

### Tests & Docs

    pip install -r dev_requirements.txt 
    
    make test

    make documentation # build documentation (with sphinx)
    make upload-docs # publish online 
