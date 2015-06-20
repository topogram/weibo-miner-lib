#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from  itertools import permutations

from topogram.utils import any2utf8
from topogram.corpora.csv_file import CSVCorpus 
from topogram.processors.nlp import NLP
from topogram.processors.regexp import Regexp

from topogram import Topogram
from topogram.visualizers.network import Network

import logging
import sys
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

# import corpus
csv_corpus = CSVCorpus(os.path.join("examples", 'sampleweibo.csv'),
        source_column="uid",
        text_column="text",
        timestamp_column="created_at",
        time_pattern="%Y-%m-%d %H:%M:%S",
        additional_columns=["permission_denied", "deleted_last_seen"])

# validate corpus formatting
try :
    csv_corpus.validate()
except ValueError, e:
    print e.message, 422

# init processors
chinese_nlp = NLP("zh")
url = Regexp(r"\b(([\w-]+://?|www[.])[^\s()<>]+(?:\([\w\d]+\)|([^\p{P}\s]|/)))")

# process  data
topogram = Topogram(corpus=csv_corpus, processors=[("zh", chinese_nlp), ("urls", url)])

# create viz model
words_network = Network( directed=False )

for row in topogram.process():
    words_network.add_edges_from_nodes_list(row["zh"])

# get processed graph as d3js json
print words_network.get(nodes_count=1000, min_edge_weight=3, json=True)

