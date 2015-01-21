#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import os
from datetime import datetime

from topogram.corpora.csv_file import CSVCorpus

class TestCSVCorpus(unittest.TestCase):

    def setUp(self):
        csv_path = os.path.join(os.getcwd(), "tests/sampleweibo.csv")
        self.corpus = CSVCorpus(csv_path, source_column="uid", time_pattern="%Y-%m-%d %H:%M:%S")

    def test_csv_sniffer(self):
        # sniff dialect and headers from raw file
        self.assertEqual(self.corpus.dialect.delimiter, ",")
        self.assertTrue(self.corpus.headers, True)

    def test_wrong_column_names(self): 
        self.corpus.source_column="haha"
        self.assertRaises(ValueError, lambda : self.corpus.validate())

    def test_wrong_date_format(self):
        self.corpus.source_column="%Y-%m-%dT%H:%M:%S"
        self.assertRaises(ValueError, lambda : self.corpus.validate())

    def test_iterate_corpus(self):
        for row in self.corpus:
            self.assertTrue(isinstance(row[0], str))
            self.assertTrue(isinstance(row[1], datetime))

    def test_store_headers(self):
        self.assertIn("mid", self.corpus.headers)
        self.assertTrue(self.corpus.headers is not None)

    def test_raw_sample(self):
        sample = self.corpus.raw_sample(10)
        self.assertEquals(len(sample), 10)

    def test_len(self):
        self.assertTrue(len(self.corpus) == 0)

    def test_wrong_encoding(self):
        """ wrong encoding should raise an error"""
        csv_path = os.path.join(os.getcwd(), "tests/nonutf8sample.csv")
        self.assertRaises(TypeError, lambda : CSVCorpus(csv_path))
        # self.assertTrue(len(self.corpus) == 12)

    # def test_index(self):
    # def test_pandas_csv_parsing(self):
    #     # date parsing
    #     self.assertTrue(self.corpus.df["created_at"][0].year == 2012)

    # def test_timeframe(self):
    #     self.assertRaises(ValueError, lambda : self.corpus.set_timeframe('bla', 0))
    #     self.corpus.set_timeframe('2012-01-03',  '2012-04-02')
    #     self.assertTrue(len(self.corpus) == 58)
    #     self.assertTrue(len([row for row in self.corpus]) == 58)
    #     self.corpus.reset_timeframe()
    #     self.assertTrue(len([row for row in self.corpus]) == 121)

if __name__ == '__main__':
    unittest.main()
