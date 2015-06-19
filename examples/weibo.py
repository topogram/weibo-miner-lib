#!/usr/bin/env python
# -*- coding: utf-8 -*-

from  itertools import permutations

from topogram.utils import any2utf8
from topogram.corpora.csv_file import CSVCorpus 
from topogram.languages.zh import ChineseNLP
from topogram.topograms.preprocess import NLPPreProcess

# import corpus
csv_corpus = CSVCorpus('sampleweibo.csv',
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


# init NLP
nlp = ChineseNLP()

# process  data
topogram = NLPPreProcess(corpus=csv_corpus, nlp=nlp)

for i, row in enumerate(topogram.process()):
    keywords = set(row["keywords"]) # set() to avoid repetitions

    # compute word graph 
    for word in list(permutations(keywords, 2)) : # pair the words
        topogram.add_words_edge(word[0], word[1])


# get processed graph
topogram.get_words_network(nodes_count=1000, min_edge_weight=3)

# output as  json
print topogram.export_words_to_json()
