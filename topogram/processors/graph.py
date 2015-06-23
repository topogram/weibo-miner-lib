#!/usr/bin/env python
# -*- coding: utf-8 -*-

from topogram.processor import Processor

import networkx as nx
from  itertools import permutations

import logging
logger = logging.getLogger('topogram.processors.graph')

class Graph(Processor):

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

    def __call__(self, nodes):
        if type(nodes) is list : 
            self.add_edges_from_nodes_list(nodes)
        elif type(nodes) is tuple : 
            self.add_edge(*nodes)
        return self.g.edges()
