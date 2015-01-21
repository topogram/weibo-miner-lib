#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import json
import  unittest
from datetime import datetime
from topogram.topogram import Topogram
from topogram.languages.zh import ChineseNLP 
from topogram.corpora.csv_file import CSVCorpus
from topogram.topograms.basic import BasicTopogram

# get a csv corpus
csv_path = os.path.join(os.getcwd(), "tests/sampleweibo.csv")
corpus = CSVCorpus(csv_path, source_column="uid", time_pattern="%Y-%m-%d %H:%M:%S")

# get Chinese NLP
nlp = ChineseNLP()
nlp.add_stopword("ukn")

class TestTopogram(unittest.TestCase):

    def setUp(self):

        # create topogram
        self.topogram = Topogram(corpus, nlp)
        self.nlp = nlp
        self.corpus = corpus

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
        hashtagPattern=r"#([^#\s]+)#"
        self.topogram.add_citation_regexp(hashtagPattern)

        # extract citation
        citations = self.topogram.extract_citations("bonjour #yoyo# #yoyo# #yaya#")
        self.assertTrue(len(citations) == 3)

    def test_ignore_citations(self):
        # add a citation pattern
        hashtagPattern=r"#([^#\s]+)#"
        self.topogram.add_citation_regexp(hashtagPattern)
        
        # extract citation
        self.topogram.add_citation_to_ignore("yaya")
        citations = self.topogram.extract_citations("bonjour #yoyo# #yoyo# #yaya#")
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

    # def test_specific_timeframes(self):
    #     self.topogram.set_timeframe('2012-01-03', '2012-04-02')
    #     self.assertTrue(len(self.topogram.corpus) == 58)
    #     self.topogram.reset_timeframe()
    #     self.assertTrue(len(self.topogram.corpus) == 121)

class TestBasicTopogram(unittest.TestCase):

    def setUp(self):

        # create topogram
        corpus = CSVCorpus(csv_path, source_column="uid", time_pattern="%Y-%m-%d %H:%M:%S")
        corpus.validate()
        self.topogram = BasicTopogram(corpus, nlp)

        self.topogram.add_citation_to_ignore("ukn")
        self.topogram.add_citation_to_ignore("uid")

        urlPattern=r"\b(([\w-]+://?|www[.])[^\s()<>]+(?:\([\w\d]+\)|([^\p{P}\s]|/)))"
        hashtagPattern=r"#([^#\s]+)#"
        self.topogram.nlp.add_stop_regexp(urlPattern)

        # self.topogram.nlp.add_stopword(u' ')

    def test_process(self):
        self.topogram.process()
        self.assertTrue(self.topogram.citations.order() != 0)

    def test_list_of_top_words(self):
        self.topogram.process()
        top_words = self.topogram.get_top_words(150)
        self.assertTrue(len(top_words) == 2)
        top_citations = self .topogram.get_top_citations(20)
        
        print top_citations
        self.assertTrue(len(top_citations) == 1)

    def test_densities(self):
        self.topogram.process()
        self.assertTrue(self.topogram.get_words_density() < 1)
        self.assertTrue(self.topogram.get_citations_density() < 1)

    # def test_top_graphs(self):
    #     self.topogram.process()
    #     self.topogram.get_words_network(200)
    #     self.assertTrue(False)

if __name__ == '__main__':
    unittest.main()
