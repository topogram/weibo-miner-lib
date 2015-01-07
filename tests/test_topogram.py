#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import  unittest
from datetime import datetime
from topogram.topogram import Topogram
from topogram.languages.zh import ChineseNLP 
from topogram.corpora.csv_corpus import CSVCorpus
from topogram.topograms.basic import BasicTopogram

class TestTopogram(unittest.TestCase):

    def setUp(self):
        # get a csv corpus
        csv_path = os.path.join(os.getcwd(), "tests/sampleweibo.csv")
        self.corpus = CSVCorpus(csv_path, source_column="uid", time_pattern="%Y-%m-%d %H:%M:%S")

        # get Chinese NLP
        self.nlp = ChineseNLP()

        # create topogram
        self.topogram = Topogram(self.corpus, self.nlp)

    def add_nx_data(self):
        # random data to test  
        self.topogram.add_words_edge( "a","b")
        self.topogram.add_words_edge( "a","b")
        self.topogram.add_words_edge( "c","b")

        self.topogram.add_citations_edge( "a","b")
        self.topogram.add_citations_edge( "a","b")
        self.topogram.add_citations_edge( "c","b")

    def test_init(self):
        """ should accept only lib built-in types """
        self.assertRaises(TypeError, lambda : Topogram(1, self.nlp))
        self.assertRaises(TypeError, lambda : Topogram(self.corpus, 1))
        self.assertRaises(TypeError, lambda : Topogram(self.corpus, self.nlp, {}))

    def test_extract_citations(self):
        # add a citation pattern
        urlPattern=r"\b(([\w-]+://?|www[.])[^\s()<>]+(?:\([\w\d]+\)|([^\p{P}\s]|/)))"
        self.topogram.add_citation_regexp(urlPattern)
        # extract citation
        citations = self.topogram.extract_citations("bonjour http://topogram.io http://topogram.io")
        self.assertTrue(len(citations) == 2)

    def test_ignore_citations(self):
        # add a citation pattern
        urlPattern=r"\b(([\w-]+://?|www[.])[^\s()<>]+(?:\([\w\d]+\)|([^\p{P}\s]|/)))"
        self.topogram.add_citation_regexp(urlPattern)
        
        # extract citation
        self.topogram.add_citation_to_ignore("http://google.com")
        citations = self.topogram.extract_citations("bonjour http://topogram.io http://topogram.io http://google.com")
        self.assertTrue(len(citations) == 2)

    def test_has_networks(self):
        self.add_nx_data() 
        self.assertTrue(self.topogram.words.size() == 2) # nodes
        self.assertTrue(self.topogram.words.order() == 3) # edges

    def test_is_weighted_network(self):
        self.add_nx_data()
        print self.topogram.words.edges(data=True)
        self.assertTrue(self.topogram.words["a"]["b"]["weight"] == 2)
        self.assertTrue(self.topogram.citations["a"]["b"]["weight"] == 2)

    def test_export_to_d3_js(self):
        self.add_nx_data()
        d3_json = self.topogram.export_words_to_d3_js()
        print d3_json
        self.assertTrue( type(d3_json["nodes"]) is list)
        self.assertTrue( type(d3_json["links"]) is list)

    def test_specific_timeframes(self):
        start = datetime.now()
        stop = datetime.now()

        self.assertRaises(TypeError, lambda : self.topogram.set_time_limit(0, stop))
        self.assertRaises(TypeError, lambda : self.topogram.set_time_limit(start, 0))

class TestBasicTopogram(unittest.TestCase):

    def setUp(self):
        # get a csv corpus
        csv_path = os.path.join(os.getcwd(), "tests/sampleweibo.csv")
        self.corpus = CSVCorpus(csv_path, source_column="uid", time_pattern="%Y-%m-%d %H:%M:%S")

        # get Chinese NLP
        self.nlp = ChineseNLP()

        # create topogram
        self.topogram = BasicTopogram(self.corpus, self.nlp)

    def test_process(self):
        self.topogram.process()
        self.assertTrue(self.topogram.citations.order() != 0)



if __name__ == '__main__':
    unittest.main()
