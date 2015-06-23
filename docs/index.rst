.. Topogram documentation master file, created by
   sphinx-quickstart on Sat Jun 20 08:23:25 2015.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.



Welcome to Topogram's documentation!
====================================

.. only:: html

    :Release: |version|
    :Date: |today|

Frustration is the most ignored part of data science work. Right now, you should be working on this amazing 3D visualization but you still have to parse the date correctly and to fix all UTF-8 bugs. To help you survive this difficult condition,  Topogram will provide you with an easy way to create data pipelines with only a few lines of Python code. 

::

    # Extract a network of words from a dataset
    corpus = CSVCorpus(your_data.csv ) 
    nlp = NLP("english")
    words_network = Network(directed=False)

    for row in corpus: 
        words = nlp(row["content"])
        words_network(words)

    print words_network.to_JSON() # return a dict with weighted edges and nodes 

Topogram won't take care of the visualization itself but it will clean and format your data sets, so you can directly plug the output into something like d3js or matplotlib to see nice colored things.

Topogram relies on three core components : 

* **corpora** : parse a corpus in CSV or stream directly from Mongo, Elastic Search, etc.  
* **processors** : basic tools to format dates, extract relationships, etc.
* **viz parsers** : data containers that will return clean and ready-to-use data  for a visualization (time series, network graph, map, etc.). 



Read  the documentation for other corpora, formats, processors or visualization parsers. 

.. toctree::
    :maxdepth: 2

    install
    quickstart

    tutorials


Topogram is still in beta version. Feel free to give us feedback 





Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
