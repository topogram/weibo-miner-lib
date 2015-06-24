#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import  unittest
from datetime import datetime

from topogram.vizparser import Visualizer
from topogram.vizparsers.time_series import TimeSeries
from topogram.vizparsers.network import Network

import networkx as nx

class TestDefaultVisualizer(unittest.TestCase):

    def test_init(self):
        """should init"""
        v = Visualizer()
        self.assertTrue(isinstance(v, Visualizer) )
        self.assertEquals(v.test, "test" )


class TestTimeSeries(unittest.TestCase):

    def setUp(self):
        self.ts = TimeSeries()
        self.date = datetime(2015,6, 23, 20,00,11)


    def test_init(self):
        """should init with proper values""" 
        self.assertTrue(isinstance(self.ts, TimeSeries))
        # default values
        self.assertEquals(self.ts.timescale, "minute")
        self.assertEquals(self.ts.data, [])

    def test_authorized_time_scales(self):
        """should only authorized specific time scales"""
        self.assertRaises(ValueError, lambda :  TimeSeries("century") )

    def test_add_time_point(self):
        """should accept only datetime objects and store it correctly"""
        self.assertRaises(ValueError, lambda : self.ts.add_time_point("12 June 2013"))
        self.ts.add_time_point(self.date)
        self.assertEquals(len(self.ts.data), 1)

    def test_set_timescale(self):
        """should  recalculate values when the  timescale changes"""
        self.ts.add_time_point(self.date)
        self.ts.set_timescale("day")
        self.assertEquals(self.ts.data, [datetime(2015,6, 23)])

    def test_compute_series(self):
        """should compute series and output a count for all similar dates"""
        self.ts.add_time_point(self.date)
        self.ts.add_time_point(self.date)
        series = self.ts.compute_series()
        self.assertEquals(series[0]["count"], 2)

    def test_to_JSON(self):
        self.ts.add_time_point(self.date)
        self.ts.add_time_point(self.date)
        series = self.ts.to_JSON()
        self.assertTrue(isinstance(series, list))
        self.assertTrue(isinstance(series[0], dict))
        self.assertEquals(series[0]["count"], 2)

    def test__len__(self):
        self.ts(self.date)
        self.assertEquals(len(self.ts), 1)
        self.ts(self.date)
        self.assertEquals(len(self.ts), 2)

    def test__call__(self):
        self.assertRaises(ValueError, lambda : self.ts("12 june"))
        self.ts(self.date)
        self.assertEquals(len(self.ts), 1)
        self.ts([self.date, self.date])
        self.assertEquals(len(self.ts), 3)

class TestNetwork(unittest.TestCase):

    def setUp(self):
        self.g = Network()

    def add_nx_data(self):
        # random data to test  
        self.g.add_edge( "a","b")
        self.g.add_edge( "a","b")
        self.g.add_edge( "c","b")

    def test_init(self):
        """ should accept both directed and undirected graph on setup"""
        g = Network(directed=False)
        self.assertTrue(isinstance(g.g, nx.Graph))
        g = Network(directed=True)
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

    def test_get_nodes_degree(self):
        """should return the degree of each node"""
        self.add_nx_data() 
        deg = self.g.get_nodes_degree()
        self.assertEquals(len(deg), 3)

    def test_get_network_with_limit(self):
        """ should allow limit of the graph size upon several parameters"""
        self.add_nx_data() 
        n = self.g.get()
        self.assertEquals( len(n.edges()) , len(self.g.g.edges()))
        n = self.g.get(nodes_count=2) 
        self.assertEquals( len(n.edges()) , 1)
        n = self.g.get(min_edge_weight=2)
        self.assertEquals( len(n.edges()) , 1)
        n = self.g.get(json=True)
        self.assertTrue(isinstance(n, dict))

    def test_export_to_d3_js_and_json(self):
        """ should export to JSON correctly formatted for D3.js"""
        self.add_nx_data() 

        n = self.g.to_d3_js()
        self.assertTrue(isinstance(n, dict))
        self.assertTrue(isinstance(n["nodes"], list))
        self.assertTrue(isinstance(n["links"], list))

        n = self.g.to_JSON()
        self.assertTrue(isinstance(n, dict))
        self.assertTrue(isinstance(n["nodes"], list))
        self.assertTrue(isinstance(n["links"], list))

    def test_load_from_d3_js(self):
        """should allow import from json """
        self.add_nx_data() 
        d3json = self.g.to_JSON()
        g = Network()
        g.from_JSON(d3json)
        self.assertEquals(g.g.nodes(), self.g.g.nodes())
        self.assertEquals(g.g.edges(), self.g.g.edges())

