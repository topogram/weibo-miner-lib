#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from topogram.nlp import NLP 
from topogram.languages.zh import ChineseNLP 

class TestNLP(unittest.TestCase):

    def setUp(self):
        self.nlp = NLP()

    def test_regexp(self):
        urlPattern=r"\b(([\w-]+://?|www[.])[^\s()<>]+(?:\([\w\d]+\)|([^\p{P}\s]|/)))"
        self.nlp.add_stop_regexp(urlPattern)

        text = "test http://topogram.io/haha"
        filtered = self.nlp.filter_out_regexps(text)
        print len(filtered)
        self.assertTrue(filtered == "test ")

    def test_add_stopwords(self):
        self.assertTrue(len(self.nlp.stopwords) == 0)
        self.nlp.add_stopword("LOL")
        self.assertTrue(len(self.nlp.stopwords) == 1)

    def test_filter_out_stopwords(self):
        stopword = "LOL"
        self.nlp.add_stopword(stopword)
        filtered  = self.nlp.filter_out_stopwords(["kikoo", stopword, "haha"])
        self.assertTrue(stopword not in filtered)

class TestChineseNLP(unittest.TestCase):

    def setUp(self):
        self.nlp = ChineseNLP()

    def test_stopwords(self):
        self.assertTrue(len(self.nlp.stopwords) != 0)
        self.assertTrue("的" in self.nlp.stopwords)

    def test_extract_keywords(self):
        print self.nlp.extract_keywords("就是什么东西啦")
        self.assertTrue(False)
