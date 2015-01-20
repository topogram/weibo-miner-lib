#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import networkx as nx
from networkx.readwrite import json_graph
from datetime import datetime
from nlp import NLP
from corpus import Corpus
from collections import Counter
from utils import any2utf8

try:
    import cPickle as _pickle
except ImportError:
    import pickle as _pickle

class Topogram:
    """
    base class to extract citations from text and generate networks of citations and words.
    This class should be instantiated to use a specific processing algorithms.
    """

    def compile_regexp(self, regexp):
        """ compile a regexp only once to gain time during processing """
        return re.compile(regexp, re.UNICODE)

    def extract_citations(self, txt):
        """ 
            Extract all citations from a given text. 
            Return a list of citations
        """
        citations=[]
        for regexp in self.citation_regexps :
            for x in regexp.findall(txt):
                if x not in self.ignored_citations : citations.append(x)
        return citations

    def add_citation_regexp(self, regexp):
        """ 
        Add a specific pattern to extract a citation from raw text.
        """ 
        if type(regexp) is str : 
            self.citation_regexps = [self.compile_regexp(regexp)] 
        elif type(regexp) is list :
            self.citation_regexps = [self.compile_regexp(reg) for reg in regexp]
        else : 
            raise TypeError("Topogram - regexp should be a str")  

    def add_citation_to_ignore(self, citation):
        """ Add a string to the list of citations to be ignored during processing. For instance, if you want to ignore a user (@justinbieber) while processing your tweets."""
        self.ignored_citations.append(citation)

    def add_words_edge(self, wordA, wordB):
        if self.words.has_edge(wordA, wordB):
            self.words[wordA][wordB]['weight'] += 1
        else:
            self.words.add_edge(wordA, wordB, weight= 1)

    def add_citations_edge(self, source, target):
        if self.citations.has_edge(source, target):
            self.citations[source][target]['weight'] += 1
        else:
            self.citations.add_edge(source, target, weight= 1)

    def __init__(self, corpus=Corpus, nlp=NLP, citation_regexp=r"@([^:：,，\)\(（）|\\\s]+)"):
        """
        Initialize a topogram from a corpus and a NLP processor.
        Optional : regexp parser  
        """

        if not isinstance(corpus, Corpus):
            raise TypeError("Topogram arg 1 should be a corpus")
        else :
            self.corpus = corpus

        if not isinstance(nlp, NLP):
            raise TypeError("Topogram arg 2 should be a NLP parser")
        else : 
            self.nlp = nlp

        self.add_citation_regexp(citation_regexp)
        self.ignored_citations=[]

        # main networks
        self.citations = nx.DiGraph()
        self.words = nx.Graph()
        self.words_to_citations = nx.Graph()

        # init 
        self.start = None
        self.end = None

    def set_timeframe(self, start, end):
        """ specific timeframe to process """
        self.corpus.set_timeframe(start, end)

    def reset_timeframe(self):
        """ Cancel specific timeframe to process"""
        self.corpus.reset_timeframe()

    def get_top_nodes(self, graph, min):
        """ get most important nodes in a graph"""
        degrees =  graph.degree()
        return [ { "node" : word , "degree":  degrees[word]} for word in sorted(degrees, key=lambda x: degrees[x], reverse=True) if degrees[word] > min]

    def get_top_words(self, min):
        """ Get most important words (based on network degree) """
        return self.get_top_nodes(self.words, min)

    def get_top_citations(self, min):
        """ Get most important words (based on network degree) """
        return self.get_top_nodes(self.citations, min)

    def get_node_network(self, graph, min):
        """ Get most important words (based on network degree) """
        nodes = self.get_top_nodes(graph, min)
        for node in nodes :
            nodes 

    def get_words_network(self, min):
        """ get a graph of words given a maximum number of nodes """
        self.get_node_network(self.words, min)

    def get_words_density(self):
        """ Return the density of the words graph. (The density is 0 for a graph without edges and 1 for a complete graph.) """
        return nx.density(self.words)

    def get_citations_density(self):
        """ Return the density of the words graph. (The density is 0 for a graph without edges and 1 for a complete graph.) """
        return nx.density(self.citations)

    def process(self):
        """ Method to extract all knowledge from corpus"""
        raise NotImplementedError('Not available for abstract base class. You should instantiate Topogram class with a specific algorithm')

    def export_words_to_d3_js(self):
        """ export to d3 with clean formatting """
        d =  json_graph.node_link_data(self.words)
        return d

    def export_citations_to_d3_js(self):
        """ export to d3 with clean formatting """
        d =  json_graph.node_link_data(self.citations)
        return d

    def export_to_json(self, fname):
        json_data = self.export_to_d3()
        json.dump(d, open(fname,"w"), sort_keys=True, indent=4)

