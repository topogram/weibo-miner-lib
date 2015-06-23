#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import json
import  unittest
from datetime import datetime
from topogram.topogram import Topogram
from topogram.processors.nlp import NLP 
from topogram.corpora.csv_file import CSVCorpus

# get a csv corpus
csv_path = os.path.join(os.getcwd(), "tests/sampleweibo.csv")
corpus = CSVCorpus(csv_path, origin="uid", time_pattern="%Y-%m-%d %H:%M:%S")

# get Chinese NLP
nlp = NLP("zh")
nlp.add_stopword("ukn")

class TestTopogram(unittest.TestCase):

    def setUp(self):
        """Create a topogram """ 
        self.topogram = Topogram(corpus=corpus, processors=[nlp])
        self.nlp = nlp
        self.corpus = corpus

    def test_init_instances_raise_errors(self):
        """ should only accept a Corpus instance and a list of processors"""
        self.assertRaises(TypeError, lambda : Topogram(1, [self.nlp]))
        self.assertRaises(TypeError, lambda : Topogram(self.corpus, 1))
        self.assertRaises(TypeError, lambda : Topogram(self.corpus, [1]))

    def test_init_store_values(self):
        """ should store corpus and processors"""
        self.assertEquals(self.topogram.corpus, self.corpus)
        self.assertEquals(self.topogram.processors[0], self.nlp)


    # def test_add_multiple_regexps(self):
    #     hashtagPattern=r"#([^#\s]+)#"
    #     self.topogram.add_citation_regexp([hashtagPattern, hashtagPattern])
    #     self.assertEquals(len(self.topogram.citation_regexps), 2)

    # def test_extract_citations(self):
    #     # add a citation pattern
    #     hashtagPattern=r"#([^#\s]+)#"
    #     self.topogram.add_citation_regexp(hashtagPattern)

    #     # extract citation
    #     citations = self.topogram.extract_citations("bonjour #yoyo# #yoyo# #yaya#")
    #     self.assertTrue(len(citations) == 3)

    # def test_ignore_citations(self):
    #     # add a citation pattern
    #     hashtagPattern=r"#([^#\s]+)#"
    #     self.topogram.add_citation_regexp(hashtagPattern)
        
    #     # extract citation
    #     self.topogram.add_citation_to_ignore("yaya")
    #     citations = self.topogram.extract_citations("bonjour #yoyo# #yoyo# #yaya#")
    #     self.assertTrue(len(citations) == 2)

    # def test_is_weighted_network(self):
    #     self.add_nx_data()
    #     print self.topogram.words.edges(data=True)
    #     self.assertTrue(self.topogram.words["a"]["b"]["weight"] == 2)
    #     self.assertTrue(self.topogram.citations["a"]["b"]["weight"] == 2)

    # def test_get_nodes_degree(self):
    #     self.add_nx_data() 
    #     deg = self.topogram.get_nodes_degree(self.topogram.words)
    #     print len(deg)
    #     self.assertEquals(len(deg), 3)

    # def test_get_words(self):
    #     self.add_nx_data() 
    #     w = self.topogram.get_words()
    #     self.assertEquals(w, self.topogram.words)

    # def test_get_average_degree_connectivity(self):
    #     self.add_nx_data() 
    #     d = self.topogram.get_average_degree_connectivity(self.topogram.words)
    #     print d, type(d)
    #     self.assertTrue(type(d) is dict)
    #     self.assertTrue(type(d[1]) is float)

    # def test_export_to_d3_js(self):
    #     self.add_nx_data()
    #     d3_json = self.topogram.export_words_to_d3_js()
    #     print d3_json
    #     self.assertTrue( type(d3_json["nodes"]) is list)
    #     self.assertTrue( type(d3_json["links"]) is list)

    # def test_export_words_to_json(self):
    #     self.add_nx_data()
    #     words_json = self.topogram.export_words_to_json()
    #     print words_json
    #     self.assertTrue( type(words_json["nodes"]) is list)
    #     self.assertTrue( type(words_json["links"]) is list)

    # def test_load_words_from_json(self):
    #     self.add_nx_data()
    #     words_json = self.topogram.export_words_to_d3_js()

    #     topogram = Topogram(corpus, nlp)
    #     topogram.load_words_from_json(words_json)
    #     self.assertEquals(topogram.words.nodes(), self.topogram.words.nodes())
    #     self.assertEquals(topogram.words.edges(), self.topogram.words.edges())

    # def test_get_nodes(self):
    #     self.add_nx_data()
    #     self.assertEquals(self.topogram.get_nodes(self.topogram.words), self.topogram.words.nodes())

    # def test_get_node_network(self):
    #     self.add_nx_data()
    #     g = self.topogram.get_node_network(self.topogram.words)
    #     self.assertTrue(g.nodes() < self.topogram.words.nodes())

# class TestBasicTopogram(unittest.TestCase):

#     def setUp(self):

#         # create topogram
#         corpus = CSVCorpus(csv_path, source_column="uid", time_pattern="%Y-%m-%d %H:%M:%S")
#         corpus.validateCSV()
#         self.topogram = BasicTopogram(corpus, nlp)

#         self.topogram.add_citation_to_ignore("ukn")
#         self.topogram.add_citation_to_ignore("uid")

#         urlPattern=r"\b(([\w-]+://?|www[.])[^\s()<>]+(?:\([\w\d]+\)|([^\p{P}\s]|/)))"
#         hashtagPattern=r"#([^#\s]+)#"
#         self.topogram.nlp.add_stop_regexp(urlPattern)

#         # self.topogram.nlp.add_stopword(u' ')

#     def test_process(self):
#         self.topogram.process()
#         self.assertTrue(self.topogram.citations.order() != 0)

#     # def test_list_of_top_words(self):
#     #     self.topogram.process()
#     #     top_words = self.topogram.get_top_words(150)
#     #     self.assertTrue(len(top_words) == 2)
#     #     top_citations = self .topogram.get_top_citations(20)
        
#     #     print top_citations
#     #     self.assertTrue(len(top_citations) == 1)

#     def test_densities(self):
#         self.topogram.process()
#         self.assertTrue(self.topogram.get_words_density() < 1)
#         self.assertTrue(self.topogram.get_citations_density() < 1)

# # class TestPreProcess(unittest.TestCase):
# #     def setUp(self):

# #         # create topogram
# #         corpus = CSVCorpus(csv_path, source_column="uid", time_pattern="%Y-%m-%d %H:%M:%S")
# #         corpus.validate()
# #         # self.topogram = BasicTopogram(corpus, nlp)
# #         self.preproc = NLPPreProcess(corpus=corpus, nlp=nlp)

# #     def test_process(self):
# #         rows = []
# #         for row in  self.preproc.process() : 
# #             print len(row["text_column"] )
# #             self.assertTrue(len(row["text_column"]) !=  0)
# #             self.assertTrue(type(row["text_column"]) is str)

# #     def test_preprocess_return_rows(self):
# #         rows = [row for row in  self.preproc.process() ]
# #         self.assertEquals(len(rows), 120)


if __name__ == '__main__':
    unittest.main()
