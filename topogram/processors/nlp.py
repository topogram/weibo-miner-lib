#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
from topogram.utils import any2utf8
from topogram.processor import Processor
import importlib

import os
here = os.path.dirname(os.path.abspath(__file__))
stopwords_dir = os.path.join(here , os.path.join("languages", "stopwords"))

import logging
logger = logging.getLogger('topogram.nlp')

class NLP(Processor):
    """
    Interface (abstract base class) for NLP and text cleaning.
    This class should be instantiated to describe a specific language.

    """

    def __init__(self, language): 
        logger.info("init NLP class for %s"%language)

        if language not in ["zh", "en", "fr"]:
            raise NotImplementedError('%s : language not supported yet.'%language)
        else :
            self.parser = importlib.import_module( "topogram.processors.languages.%s"%language)
            self.parser.add_support() # some language-specific tasks

        # stopwords
        self.stopwords = []

        # parse generic stopwords
        stopwords_file=os.path.join(stopwords_dir, "all.txt")
        self.stopwords+=[i.strip() for i in open(stopwords_file,"r")]

        # parse language-specific  stopwords
        stopwords_file=os.path.join(stopwords_dir, language+".txt")
        self.stopwords+=[i.strip() for i in open(stopwords_file,"r")]

        logger.info("Parsed %s stopwords"%len(self.stopwords))

    def extract_keywords(self,txt):
        """ Method to extract keywords from a string"""
        return self.parser.extract_keywords(txt)


    def extract_dictionary(self,txt):
        """ Method to extract dictionary from a string"""
        return self.parser.extract_dictionary(txt)

    def get_words(self, txt):
        """ Get words w/o stopwords. Returns a list of words"""
        dico=self.extract_dictionary(txt)
        if dico is not None : 
            words=[any2utf8(w) for w in dico if any2utf8(w) not in self.stopwords]
        else :
            words = []
        return words

    def add_stopword(self, word): 
        """ Add a stopword to the list of stopwords"""
        self.stopwords.append(word)

    def filter_out_stopwords(self,txt):
        """ Remove stopwords from text"""
        txt_wo_stopwords=[w for w in txt if w not in self.stopwords]
        print len(txt), len(txt_wo_stopwords)
        return txt_wo_stopwords

    def __call__(self, content):
        """ Main action to execute. Will extract keywords from the 'content' attribute"""
        # clean = self.filter_out_regexps(content)
        keywords = self.get_words(content)
        return keywords

    # def add_stop_regexp(self, regexp):
    #     """ Add a regexp pattern to ignore while processing text  """ 
    #     self.stop_regexps.append(re.compile(regexp, re.UNICODE))

    # def filter_out_regexps(self, txt):
    #     """ Remove all elements following defined regexp patterns"""
    #     clean=txt
    #     for regexp in self.stop_regexps:
    #         for junks in regexp.findall(txt):
    #             if type(junks) is str:
    #                 clean=clean.replace(junks,"")
    #             else :
    #                 for junk in junks:
    #                     clean=clean.replace(junk,"")
    #     return clean
