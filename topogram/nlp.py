#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
from utils import any2utf8

import logging
logger = logging.getLogger('topogram.nlp')

class NLP:
    """
    Interface (abstract base class) for NLP and text cleaning.
    This class should be instantiated to describe a specific language.

    """

    def __init__(self): 
        logger.info("init NLP class")
        self.stopwords = []
        self.stop_regexps = []

    def extract_keywords(self,txt):
        """ Method to extract keywords from a string"""
        raise NotImplementedError('Not available for abstract base class. You should instantiate this class for a specific language')

    def extract_dictionary(self,txt):
        """ Method to extract dictionary from a string"""
        raise NotImplementedError('Not available for abstract base class. You should instantiate this class for a specific language')

    def get_words(self, txt):
        """ Get words w/o stopwords. Returns a list of words"""
        dico=self.extract_dictionary(txt) 
        words=[any2utf8(w) for w in dico if any2utf8(w) not in self.stopwords]
        return words

    def add_stopword(self, word): 
        """ Add a stopword to the list of stopwords"""
        self.stopwords.append(word)

    def filter_out_stopwords(self,txt):
        """ Remove stopwords from text"""
        print len(txt)
        txt_wo_stopwords=[w for w in txt if w not in self.stopwords]
        print len(txt), len(txt_wo_stopwords)
        return txt_wo_stopwords

    def add_stop_regexp(self, regexp):
        """ Add a regexp pattern to ignore while processing text  """ 
        self.stop_regexps.append(re.compile(regexp, re.UNICODE))

    def filter_out_regexps(self, txt):
        """ Remove all elements following defined regexp patterns"""
        clean=txt
        for regexp in self.stop_regexps:
            for junks in regexp.findall(txt):
                if type(junks) is str:
                    clean=clean.replace(junks,"")
                else :
                    for junk in junks:
                        clean=clean.replace(junk,"")
        return clean
