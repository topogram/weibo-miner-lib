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
        """  Dialect and headers should be detected sniffer given a raw file """
        self.assertEqual(self.corpus.dialect.delimiter, ",")
        self.assertTrue(self.corpus.headers, True)

    def test_wrong_column_names(self):
        """ Wrong column names should raise ValueError """
        self.corpus.source_column="haha"
        self.assertRaises(ValueError, lambda : self.corpus.validate())

    def test_wrong_date_format(self):
        """ Wrong data format should raise a ValueError """
        self.corpus.source_column="%Y-%m-%dT%H:%M:%S"
        self.assertRaises(ValueError, lambda : self.corpus.validate())

    def test_iterate_corpus(self):
        """ Corpus should be an interable """
        for row in self.corpus:
            self.assertTrue(isinstance(row["text_column"], str))
            self.assertTrue(isinstance(row["time_column"], datetime))
            self.assertTrue(isinstance(row["time_column"], datetime))

    def test_store_headers(self):
        """ CSV headers should be available as a list """
        self.assertIn("mid", self.corpus.headers)
        self.assertTrue(self.corpus.headers is not None)

    def test_raw_sample(self):
        """raw_sample should returns a sample of x lines of raw data"""
        sample = self.corpus.raw_sample(10)
        self.assertEquals(len(sample), 10)

    def test_len(self):
        """ Corpus length should return a number """
        self.assertTrue(len(self.corpus) == 0)

    def test_wrong_encoding(self):
        """ Wrong file encoding should raise an error"""
        csv_path = os.path.join(os.getcwd(), "tests/nonutf8sample.csv")
        self.assertRaises(TypeError, lambda : CSVCorpus(csv_path))
        # self.assertTrue(len(self.corpus) == 12)

    def test_wrong_additional_columns(self):
        """ Wrong additional column should raise an error """
        csv_path = os.path.join(os.getcwd(), "tests/sampleweibo.csv")
        bad_corpus = CSVCorpus(csv_path, source_column="uid", time_pattern="%Y-%m-%d %H:%M:%S", additional_columns=["image", "blabla"])
        self.assertEquals(["image", "blabla"], bad_corpus.additional_columns)
        self.assertRaises(ValueError, lambda : bad_corpus.validate())

    def test_additional_columns(self):
        """ Additional column should be parsed and returned as string or float depending on their"""
        csv_path = os.path.join(os.getcwd(), "tests/sampleweibo.csv")
        corpus = CSVCorpus(csv_path, source_column="uid", time_pattern="%Y-%m-%d %H:%M:%S", additional_columns=["image", "source"])
        self.assertEquals(["image", "source"], corpus.additional_columns)
        for row in corpus :
            self.assertEquals(len(row), 5)
            self.assertEquals(type(row["source"]), str)
            self.assertEquals(type(row["image"]), int)



if __name__ == '__main__':
    unittest.main()
