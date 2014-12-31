#!/usr/bin/env python
# -*- coding: utf-8 -*-

from topogram.corpora.csv_corpus import CSVCorpus
import unittest
import os
from datetime import datetime

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
        self.assertRaises(ValueError, lambda : self.corpus.validate_csv())

    def test_wrong_date_format(self):
        self.corpus.source_column="%Y-%m-%dT%H:%M:%S"
        self.assertRaises(ValueError, lambda : self.corpus.validate_csv())

    def test_iterate_corpus(self):
        for row in self.corpus:
            self.assertTrue(isinstance(row[0], str))
            self.assertTrue(isinstance(row[1], datetime))

if __name__ == '__main__':
    unittest.main()
