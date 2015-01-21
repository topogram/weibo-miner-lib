#!/usr/bin/env python
# -*- coding: utf-8 -*-

import itertools
import csv
import chardet
import codecs
from datetime import datetime

from topogram.corpus import Corpus
from topogram.utils import any2utf8

import logging
logger = logging.getLogger('topogram.corpora.csvcorpus')


class CSVCorpus(Corpus): 
    """
    Corpus in CSV format.
    
    The CSV delimiter, headers etc. are guessed automatically
    based on the file content.
    
    CSV is validated based on headers and first row only.
    
    fname = file path
    timestamp_column="created_at" (should be an existing column name)
    time_pattern='%Y-%m-%dT%H:%M:%S' )
    text_column="text" (should be an existing column name)
    source_column="uid" (should be an existing column name)
 
    """

    def __init__(self, fname, timestamp_column="created_at", time_pattern="%Y-%m-%dT%H:%M:%S", text_column="text", source_column="user_id", additional_columns = []):
        """
        Initialize the corpus from a file.
        """

        logger.info("loading corpus from %s" % fname)
        self.fname = fname
        self.length = None
        self.timestamp_column = timestamp_column
        self.time_pattern = time_pattern
        self.text_column = text_column
        self.source_column = source_column
        self.length = 0
        self.additional_columns = additional_columns

        # load the first few lines, to guess the CSV dialect
        head = ''.join(itertools.islice(open(self.fname, "r"), 5))
        self.has_headers = csv.Sniffer().has_header(head)
        self.dialect = csv.Sniffer().sniff(head)
        logger.info("sniffed CSV delimiter=%r, headers=%s" % (self.dialect.delimiter, self.has_headers))

        # test encoding
        encoding = chardet.detect(head)
        self.encoding  = encoding['encoding']

        if encoding['confidence'] <  0.99 or encoding['encoding'] != 'utf-8': 
            raise TypeError("File has an unknown encoding : %s. Please try UTF-8 for better compatibility"% encoding['encoding'])

        logger.info("encoding detected as %s" % (encoding["encoding"]))
        self.reader = csv.DictReader(open(self.fname, "r"), dialect=self.dialect)

        # headers are required
        if not self.has_headers :
            raise KeyError("CSV file should have headers")

        # store headers
        self.headers = self.reader.fieldnames


    def raw_sample(self, length):
        """ 
        Get a sample of the raw corpus of a specific length.
        
        args : length should be an int
        returns : list of row (row are dict)
        """

        if type(length) is not int : raise TypeError("sample length should be an int")

        sample= []
        for index, row in enumerate(self.reader, start=1):
            sample.append(row)
            if index == length : break
        return sample

    def validate(self):
            """
            Perform several checks on CSV files

            * file should have headers
            * columns should exist
            * timestamp format should be valid 
            
            """
            # headers are required
            if not self.has_headers :
                raise KeyError("CSV file should have headers")

            # check if required columns exist
            if any2utf8(self.timestamp_column) not in self.headers: 
                raise ValueError("column '%s' not present in CSV"%self.timestamp_column)
            if any2utf8(self.text_column) not in self.headers:
                raise ValueError("column '%s' not present in CSV"%self.text_column)
            if any2utf8(self.source_column) not in self.headers:
                raise ValueError("column '%s' not present in CSV"%self.source_column)

            for column_name in self.additional_columns : 
                if any2utf8(column_name) not in self.headers:
                    raise ValueError("column '%s' not present in CSV"%column_name)

            # check time format (will raise ValueError)
            first_line = self.reader.next()
            timestamp = first_line[any2utf8(self.timestamp_column)]
            datetime.strptime(timestamp, any2utf8(self.time_pattern))

    def reset_timeframe(self):
        self.start = None
        self.stop = None

    def __iter__(self):
        """
        Iterate over the corpus, returning a tuple with text as a 'str' and timestamp as a 'datetime' object.
        """ 
        for index, row in enumerate(self.reader, start=1):
            result = {}

            result["text_column"] = any2utf8(row[any2utf8(self.text_column)])
            result["time_column"] = datetime.strptime(row[any2utf8(self.timestamp_column)], self.time_pattern)
            result["source_column"] = row[any2utf8(self.source_column)]

            for column_name in self.additional_columns :
                result[any2utf8(column_name)] = row[any2utf8(self.source_column)]

            self.length =  self.length + 1  # store the total number of CSV rows

            yield(result)



    def __len__(self):
        """ this gives the length of the corpus - works only it has already been processed once"""
        return self.length
