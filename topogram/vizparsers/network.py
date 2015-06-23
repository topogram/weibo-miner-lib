#!/usr/bin/env python
# -*- coding: utf-8 -*-

from topogram.vizparser import Visualizer

import networkx as nx
from networkx.readwrite import json_graph, gpickle
from networkx.algorithms.approximation.dominating_set import min_weighted_dominating_set

from  itertools import permutations
from collections import Counter

import logging 
logger = logging.getLogger('topogram.visualizers.network')

class Network(Visualizer):

    def __init__(self, directed=False):
        logger.info("Init network graph visualization")
        if directed : 
            self.g = nx.DiGraph()
        else :
            self.g = nx.Graph()

    # compute graph
    def add_edges_from_nodes_list(self, nodelist):
        """ Compute and add relationships to graph from a list of nodes. 
            This assume that each node in this list is connected to each other in a similar fashion (weight=1)
        """ 
        for node in list(permutations(set(nodelist), 2)) : # pair the words
            self.add_edge(node[0], node[1])

    def add_edge(self, nodeA, nodeB):
        if self.g.has_edge(nodeA, nodeB):
            self.g[nodeA][nodeB]['weight'] += 1
        else:
            self.g.add_edge(nodeA, nodeB, weight= 1)

    def get(self, nodes_count=0, min_edge_weight=0, json=False):
        """ Get most important nodes in the networks
              
              nodes_count : maximum number of nodes in the final graph
              min_edge_weight : minimum weight for edges to be kept
              json : boolean

              return :
                if json==True : returns a d3js formatted json
                else  a networkx Graph object, subgraph of g
        """
        g = self.g
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

        if json : 
            return json_graph.node_link_data(g_ok)
        else : 
            return g_ok

    def get_nodes(self, g):
        return g.nodes()

    # METRICS

    def get_nodes_degree(self, graph):
        """ get most important nodes in a graph"""
        degrees =  graph.degree()
        return [ { "node" : word , "degree":  degrees[word]} for word in sorted(degrees, key=lambda x: degrees[x], reverse=True)]

    def calculate_eigenvector_centrality(self, graph):  
        ''' Calculate eigenvector centrality of a node, sets value on node as attribute; returns graph, and dict of the eigenvector centrality values.
        '''
        g = graph
        ec = nx.eigenvector_centrality(g)
        nx.set_node_attributes(g,'eigen_cent',ec)
        #ec_sorted = sorted(ec.items(), key=itemgetter(1), reverse=True)
        return ec

    # def get_average_graph(self, g):
    #     """Filter the graph with only nodes above the average connectivity"""
    #     avg_deg = nx.eigenvector_centrality(g)
    #     print "average degree connectivity %s"%avg_deg
    #     self.limit_node_network(g, avg_deg)


    def get_average_degree_connectivity(self):
        return nx.average_degree_connectivity(self.g)

    def get_density(self):
        """ Return the density of the words graph. (The density is 0 for a graph without edges and 1 for a complete graph.) """
        return nx.density(self.g)

    def __call__(self, nodes, edges , data={}):

        if data != {} and type(data) is not dict :
            raise ValueError("Data to init graph are required to be dict")

        for e in edges:
            self.add_edge(*(e))
        logger.info("Edges added")


    def to_d3_js(self):
        """ export to d3 with clean formatting """
        d =  json_graph.node_link_data(self.g)
        return d

    def to_JSON(self):
        d =  json_graph.node_link_data(self.g)
        return d

    def from_JSON(self, json_data):
        """ load from json"""
        self.g = json_graph.node_link_graph(json_data)
