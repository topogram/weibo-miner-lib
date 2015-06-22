#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest 
from topogram.processors.nlp import NLP 
from topogram.processors.regexp import Regexp


class TestRegexp(unittest.TestCase):

    def setUp(self):
        self.regexp_url = Regexp(r"\b(([\w-]+://?|www[.])[^\s()<>]+(?:\([\w\d]+\)|([^\p{P}\s]|/)))")

    def test_regexp(self):
        text = "test http://topogram.io/haha"
        urls = self.regexp_url(text)
        print urls
        self.assertTrue(len(urls) == 1)
        self.assertTrue(urls[0] == "http://topogram.io/haha")


class TestNLP(unittest.TestCase):

    def setUp(self):
        self.nlp = NLP("zh") #chinese

    def test_add_stopwords(self):
        count_stopwords = len(self.nlp.stopwords)
        self.assertTrue( count_stopwords != 0)
        self.nlp.add_stopword("LOL")
        self.assertTrue(len(self.nlp.stopwords) == count_stopwords+1)

    def test_filter_out_stopwords(self):
        stopword = "LOL"
        self.nlp.add_stopword(stopword)
        filtered  = self.nlp.filter_out_stopwords(["kikoo", stopword, "haha"])
        self.assertTrue(stopword not in filtered)

    def test_extract_keywords(self):
        keywords = self.nlp.extract_keywords("我去中国旅游")
        print keywords
        self.assertTrue(len(keywords) == 2)
        self.assertTrue("旅游" in keywords)


    def test_extract_dictionary(self):
        dico = self.nlp.extract_dictionary("我去中国旅游")
        self.assertTrue(len(dico), 4)

class TestChineseNLP(unittest.TestCase):

    def setUp(self):
        self.nlp = NLP("zh")

    def test_stopwords(self):
        self.assertTrue(len(self.nlp.stopwords) != 0)
        self.assertTrue("的" in self.nlp.stopwords)

    def test_extract_keywords(self):
        keywords = self.nlp.extract_keywords("就是什么东西啦")
        self.assertTrue( type(keywords[0]) is str)
        self.assertTrue( len(keywords) == 3)
        self.assertTrue( "东西" in keywords)

