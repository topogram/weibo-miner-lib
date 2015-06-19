#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import networkx as nx
from networkx.readwrite import json_graph, gpickle
from networkx.algorithms.approximation.dominating_set import min_weighted_dominating_set

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

    def get_nodes(self, g):
        return g.nodes()

    def get_nodes_degree(self, graph):
        """ get most important nodes in a graph"""
        degrees =  graph.degree()
        return [ { "node" : word , "degree":  degrees[word]} for word in sorted(degrees, key=lambda x: degrees[x], reverse=True)]

    def get_top_words(self, min):
        """ Get most important words (based on network degree) """
        return self.get_top_nodes(self.words, min)

    def get_top_citations(self, min):
        """ Get most important words (based on network degree) """
        return self.get_top_nodes(self.citations, min)

    def get_words(self):
        return self.words

    def get_average_degree_connectivity(self, g):
        return nx.average_degree_connectivity(g)

    # def calculate_eigenvector_centrality(self, graph):  
    #     ''' Calculate eigenvector centrality of a node, sets value on node as attribute; returns graph, and dict of the eigenvector centrality values.
    #     Also has commented out code to sort by ec value
    #     '''
    #     g = graph
    #     ec = nx.eigenvector_centrality(g)
    #     nx.set_node_attributes(g,'eigen_cent',ec)
    #     #ec_sorted = sorted(ec.items(), key=itemgetter(1), reverse=True)
    #     return ec

    # def get_average_graph(self, g):
    #     """Filter the graph with only nodes above the average connectivity"""
    #     avg_deg = nx.eigenvector_centrality(g)
    #     print "average degree connectivity %s"%avg_deg
    #     self.limit_node_network(g, avg_deg)


    def get_node_network(self, g, nodes_count=0, min_edge_weight=0):
        """ Get most important nodes in the networks
              
              g : a networkx Graph object
              nodes_count : maximum number of nodes in the final graph
              min_edge_weight : minimum weight for edges to be kept

              return :a networkx Graph object, subgraph of g
        """

        print "%s nodes total"%len(g.nodes())
        nodes_ok= []

        # filter nodes
        if nodes_count != 0 :
            print "keep only  %s words"%nodes_count
            deg = g.degree() # calculate degrees
            nodes_sorted =  sorted(deg, key=lambda k:  deg[k] , reverse=True)
            nodes_ok = nodes_sorted[0:nodes_count]

        g_ok = g.subgraph(nodes_ok)
        print "%s nodes after filtering"%len(g_ok.nodes())

        # filter edges 
        if min_edge_weight != 0 :
            print "keep only the edges with a weight more than  %s"%min_edge_weight
            for u,v,d in g_ok.edges(data=True) :
                if d['weight'] < min_edge_weight : g_ok.remove_edge(u,v)

        print "%s edges after filtering"%len(g_ok.edges())

        return g_ok

    def get_words_network(self, nodes_count=0, min_edge_weight=0):
        """ 
            Get a graph of words given a maximum number of nodes 
        
        """
        words_network =  self.get_node_network(self.words, nodes_count=nodes_count, min_edge_weight=min_edge_weight)
        return words_network

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

    def export_to_json(self, g):
        d =  json_graph.node_link_data(g)
        return d

    def export_words_to_json(self):
        """ export to d3 with clean formatting """
        d =  json_graph.node_link_data(self.words)
        return d

    def load_words_from_json(self, json_data):
        """ load from json"""
        self.words = json_graph.node_link_graph(json_data)

    def export_citations_to_d3_js(self):
        """ export to d3 with clean formatting """
        d =  json_graph.node_link_data(self.citations)
        return d
