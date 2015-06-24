#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

from topogram.cli import topo_corpus
from topogram.cli import topo_proc
from topogram.cli import topo_viz

from topogram.corpus import Corpus
from topogram.processor import Processor
from topogram.vizparser import Visualizer

class TestImportCli(unittest.TestCase):

    def test_import(self): 
        import topogram.cli as cmd
        self.assertIn("topo_corpus", dir(cmd))
        self.assertIn("topo_proc", dir(cmd))
        self.assertIn("topo_viz", dir(cmd))

class TestTopoCorpus(unittest.TestCase):

    def setUp(self):
        self.parser = topo_corpus.parse_args()

    def test_with_empty_args(self):
        """ User passes no args, should fail with SystemExit"""                                    
        with self.assertRaises(SystemExit):
            self.parser.parse_args([])

    def test_get_coprus(self):

        args = self.parser.parse_args(['-t', 'time', '-r', 'venue', '-c', "artists"])
        c = topo_corpus.get_corpus(args)
        self.assertTrue(isinstance(c, Corpus) )

    # def test_with_args(self):
    #     

    # # def test_topo_corpus(self):

    # #     # for line in fileinput.input():
    # #         # line topo_corpus()

class TestTopoProc(unittest.TestCase):

    def setUp(self):
        self.parser = topo_proc.parse_args()

    def test_with_empty_args(self):
        """
        User passes no args, should fail with SystemExit
        """                                    
        with self.assertRaises(SystemExit):
            self.parser.parse_args([])

class TestTopoViz(unittest.TestCase):

    def setUp(self):
        self.parser = topo_viz.parse_args()

    def test_with_empty_args(self):
        """
        User passes no args, should fail with SystemExit
        """                                    
        with self.assertRaises(SystemExit):
            self.parser.parse_args([])
