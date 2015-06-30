#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest 
from datetime import datetime

from topogram.processor import Processor 
from topogram.processors.nlp import NLP 
from topogram.processors.regexp import Regexp
from topogram.processors.time_rounder import TimeRounder
from topogram.processors.graph import Graph

import networkx as nx

class TestDefaultProcessor(unittest.TestCase):
    def setUp(self):
        self.processor =  Processor()

    def test_save_raises_NotImplementedError(self):
        self.assertRaises(NotImplementedError, lambda : self.processor.save())

    def test_load_raises_NotImplementedError(self):
        self.assertRaises(NotImplementedError, lambda : self.processor.load())

class TestRegexp(unittest.TestCase):

    def setUp(self):
        self.regexp_url = Regexp(r"\b(([\w-]+://?|www[.])[^\s()<>]+(?:\([\w\d]+\)|([^\p{P}\s]|/)))")

    def test_init(self):
        """ should accept only str as an init arg"""
        self.assertRaises(ValueError, lambda : Regexp([1]))

    def test_regexp(self):
        text = "test http://topogram.io/haha"
        urls = self.regexp_url(text)
        print urls
        self.assertTrue(len(urls) == 1)
        self.assertTrue(urls[0][0] == "http://topogram.io/haha")

class TestTimeRounder(unittest.TestCase):

    def setUp(self):
        self.date = datetime(2015,6, 23, 20,00,11)

    def test_authorized_time_scales(self):
        """should only authorized specific time scales"""
        self.assertRaises(ValueError, lambda :  TimeRounder("century") )

    def test_init(self):
        """ should store timescale"""
        second_rounder = TimeRounder("second")
        self.assertEquals(second_rounder.timescale, "second")

    def test_accept_only_datetime_object(self):
        """ should store timescale"""
        second_rounder = TimeRounder("second")
        self.assertRaises(ValueError, lambda : second_rounder("12 June 2014"))

    def test_round_date(self):
        """should round time properly """
        second_rounder = TimeRounder("second")
        self.assertEquals( datetime(2015,6, 23, 20,00,11), second_rounder(self.date))
        minute_rounder = TimeRounder("minute")
        self.assertEquals( datetime(2015,6, 23, 20,00), minute_rounder(self.date))
        hour_rounder = TimeRounder("hour")
        self.assertEquals( datetime(2015,6, 23, 20), hour_rounder(self.date))
        day_rounder = TimeRounder("day")
        self.assertEquals( datetime(2015,6, 23), day_rounder(self.date))
        month_rounder = TimeRounder("month")
        self.assertEquals( datetime(2015,6, 1), month_rounder(self.date))
        year_rounder = TimeRounder("year")
        self.assertEquals( datetime(2015,1, 1), year_rounder(self.date))

class TestGraph(unittest.TestCase):

    def setUp(self):
        self.g = Graph()

    def test_init(self):
        """ should accept both directed and undirected graph on setup"""
        g = Graph(directed=False)
        self.assertTrue(isinstance(g.g, nx.Graph))
        g = Graph(directed=True)
        self.assertTrue(isinstance(g.g, nx.DiGraph))

    def test_add_edge(self):
        """ should add edge with weight"""
        self.g.add_edge("a","b")
        self.assertEquals(len(self.g.g.edges()), 1)

        # add weight
        self.g.add_edge("a","b")
        self.assertEquals(len(self.g.g.edges()), 1)
        w= self.g.g.edges(data=True)[0][2]["weight"]
        self.assertEquals(w, 2)

    def  test_add_edges_from_nodes_list(self):
        """should add all unique permutations from a list"""
        self.g.add_edges_from_nodes_list(["a","b","c"])
        self.assertEquals(len(self.g.g.edges()), 3)

    def test__call__add_edge(self):
        """should add list or single edge"""
        self.g(["a","b","c"])
        self.assertEquals(len(self.g.g.edges()), 3)
        self.g( ("c","d") )
        self.assertEquals(len(self.g.g.edges()), 4)

class TestNLP(unittest.TestCase):

    def setUp(self):
        self.nlp = NLP("zh") #chinese

    def test_available_languages(self):
        self.assertRaises(NotImplementedError, lambda : NLP("martien"))

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

    def test_get_words(self):
        keywords = self.nlp.get_words("我去中国旅游")
        self.assertTrue(len(keywords) == 2)
        self.assertTrue("旅游" in keywords)
        self.assertTrue("我" not in keywords)

    def test_extract_dictionary(self):
        dico = self.nlp.extract_dictionary("我去中国旅游")
        self.assertTrue(len(dico), 4)

    def test__call__(self):
        keywords = self.nlp("我去中国旅游")
        self.assertTrue(len(keywords) == 2)
        self.assertTrue("旅游" in keywords)
        self.assertTrue("我" not in keywords)

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

