#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import nltk
from textblob import TextBlob
import re
import sys
from textblob_fr import PatternTagger, PatternAnalyzer
from topogram.utils import any2utf8

here = os.path.dirname(os.path.abspath(__file__))

# Chinese methods
def add_support():
    # add better support for traditional character
    dico_file=os.path.join(here,'dict/dict.txt.big')
    jieba.set_dictionary(dico_file)

def extract_keywords(txt):
    """ Extract keywords from FR text""" 
    blob = TextBlob(any2utf8(txt), pos_tagger=PatternTagger(), analyzer=PatternAnalyzer())
    tags = blob.tags
    return [tag for tag in tags]

def normalise(word):
"""Normalises words to lowercase and stems and lemmatizes it."""
word = word.lower()
word = stemmer.stem_word(word)
word = lemmatizer.lemmatize(word)
return word


def extract_dictionary(txt):
    """ Extract from FR text"""
        blob = TextBlob(any2utf8(txt), pos_tagger=PatternTagger(), analyzer=PatternAnalyzer())
    seg_list = blob.words  
    return list(seg_list)
