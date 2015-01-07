#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import networkx as nx
from networkx.readwrite import json_graph
from datetime import datetime
from nlp import NLP
from corpus import Corpus

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
            citations += [ citation for citation in regexp.findall(txt) if citation[0] not in self.ignored_citations ]
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

    def __init__(self, corpus, nlp, citation_regexp=r"@([^:：,，\)\(（）|\\\s]+)"):
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

    def set_time_limit(self, start, end):
        if not isinstance(start, datetime):
            raise TypeError("Topogram 'start' should be a datetime object")
        else :
            self.start = start

        if not isinstance(end, datetime):
            raise TypeError("Topogram 'end' should be a datetime object")
        else :
            self.end = end

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

