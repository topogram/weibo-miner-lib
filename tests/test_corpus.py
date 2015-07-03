#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import os
from datetime import datetime

from topogram.corpus import Corpus
from topogram.corpora.csv_file import CSVCorpus

class TestDefaultCorpus(unittest.TestCase):
    """ Default methods should raise NotImplementedError"""

    def setUp(self): 
        self.corpus = Corpus(
                    "dict",
                     timestamp="created_at", 
                     time_pattern="%Y-%m-%dT%H:%M:%S", 
                     content="content", 
                     origin="user_id", 
                     adds=["test"]
                     )

    def test_properties_stored(self):
        """Properties should be stored correctly"""
        self.assertEquals(self.corpus.timestamp, "created_at")
        self.assertEquals(self.corpus.time_pattern, "%Y-%m-%dT%H:%M:%S")
        self.assertEquals(self.corpus.content, "content")
        self.assertEquals(self.corpus.origin, "user_id")
        self.assertEquals(self.corpus.adds, ["test"] )

    def test__call__parsing(self):
        """ __call__ should parse all data correctly according to init parser"""
        test_row = {
            "created_at" : "2015-06-23T20:00:05",
            "content" : "blabla",
            "user_id" : 001,
            "test" : "test",
            "other" : "shouldn' be taken into account"
        }

        clean = self.corpus(test_row)
        self.assertEquals(clean["content"], "blabla")
        self.assertTrue( isinstance(clean["timestamp"], datetime) )
        self.assertEquals(clean["test"], "test")
        self.assertRaises(KeyError, lambda : clean["other"])

    def test_len_raise_NotImplementedError(self):
        self.assertRaises(NotImplementedError, lambda : len(self.corpus))

    def test_iter_raise_NotImplementedError(self):
        self.assertRaises(NotImplementedError, lambda : [i for i in self.corpus])

    def test_load_JSON_raise_NotImplementedError(self):
        self.assertRaises(NotImplementedError, lambda : self.corpus.load_from_JSON(""))

    def test_json_dumps_raise_NotImplementedError(self):
        self.assertRaises(NotImplementedError, lambda : self.corpus.to_JSON())

class TestCSVCorpus(unittest.TestCase):

    def setUp(self):
        csv_path = os.path.join(os.getcwd(), "tests/sampleweibo.csv")
        self.corpus = CSVCorpus(csv_path, origin="uid", time_pattern="%Y-%m-%d %H:%M:%S")

    def test_csv_sniffer(self):
        """  Dialect and headers should be detected sniffer given a raw file """
        self.assertEqual(self.corpus.dialect.delimiter, ",")
        self.assertTrue(self.corpus.headers, True)

    def test_wrong_column_names(self): 
        """ Wrong column names should raise ValueError """
        self.corpus.origin="haha"
        self.assertRaises(ValueError, lambda : self.corpus.validateCSV())

    def test_wrong_date_format(self):
        """ Wrong data format should raise a ValueError """  
        self.corpus.origin="%Y-%m-%dT%H:%M:%S"
        self.assertRaises(ValueError, lambda : self.corpus.validateCSV())

    def test_iterate_corpus(self):
        """ Corpus should be an interable """ 
        for row in self.corpus:
            self.assertTrue(isinstance(row["content"], str))
            self.assertTrue(isinstance(row["timestamp"], datetime))

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

    def test_wrong_adds(self):
        """ Wrong additional column should raise an error """
        csv_path = os.path.join(os.getcwd(), "tests/sampleweibo.csv")
        bad_corpus = CSVCorpus(csv_path, origin="uid", time_pattern="%Y-%m-%d %H:%M:%S", adds=["image", "blabla"])
        self.assertEquals(["image", "blabla"], bad_corpus.adds)
        self.assertRaises(ValueError, lambda : bad_corpus.validateCSV())

    def test_adds(self):
        """ Additional column should be parsed and returned as string"""
        csv_path = os.path.join(os.getcwd(), "tests/sampleweibo.csv")
        corpus = CSVCorpus(csv_path, origin="uid", time_pattern="%Y-%m-%d %H:%M:%S", adds=["image", "source"])
        self.assertEquals(["image", "source"], corpus.adds)
        for row in corpus :
            self.assertEquals(len(row), 5)
            for col in corpus.adds : 
                self.assertEquals(type(row[col]), str)

    def test_missing_headers(self):
        csv_path = os.path.join(os.getcwd(), "tests/missingheaders.csv") 
        self.assertRaises(KeyError, lambda : CSVCorpus(csv_path) )

    def test_default_values(self):
        csv_path = os.path.join(os.getcwd(), "tests/sampleweibo.csv")
        corpus = CSVCorpus(csv_path, origin="uid", time_pattern="%Y-%m-%d %H:%M:%S", adds=None)
        self.assertEquals(corpus.adds, [])

if __name__ == '__main__':
    unittest.main()
