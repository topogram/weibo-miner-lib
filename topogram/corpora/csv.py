#!/usr/bin/env python
# -*- coding: utf-8 -*-

import itertools
import csv
from datetime import datetime
import pandas as pd

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

    def validate_csv(self):
            """
            Perform several checks on CSV files

            * file should have headers
            * columns should exist
            * timestamp format should be valid 
            
            """
            # headers are required
            if not self.has_headers :
                raise KeyError("CSV file should have headers")

            reader = csv.reader(open(self.fname), self.dialect)

            # check if required columns exist
            self.headers = reader.next()
            if self.timestamp_column not in self.headers: 
                raise ValueError("column '%s' not present in CSV"%self.timestamp_column)
            if self.text_column not in self.headers:
                raise ValueError("column '%s' not present in CSV"%self.text_column)
            if self.source_column not in self.headers:
                raise ValueError("column '%s' not present in CSV"%self.source_column)


            # check time format (will raise ValueError)
            first_line = reader.next()
            timestamp = first_line[self.headers.index(self.timestamp_column)]
            datetime.strptime(timestamp, self.time_pattern)

    def __init__(self, fname, timestamp_column="created_at", time_pattern="%Y-%m-%dT%H:%M:%S", text_column="text", source_column="user_id"):
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

        # load the first few lines, to guess the CSV dialect
        head = ''.join(itertools.islice(open(self.fname), 5))
        self.has_headers = csv.Sniffer().has_header(head)
        self.dialect = csv.Sniffer().sniff(head)
        logger.info("sniffed CSV delimiter=%r, headers=%s" % (self.dialect.delimiter, self.has_headers))

        # validate fields in CSV
        self.validate_csv()

        # lazy load // open file w pandas // parse date
        date_parser = lambda x : datetime.strptime(x, self.time_pattern)
        self.df = pd.read_csv(self.fname, dialect=self.dialect, dtype=object, parse_dates=[self.timestamp_column], date_parser=date_parser, encoding="utf-8") # iterator=True, chunksize=100, 
        
        # time frames
        self.start = None
        self.end = None

    def reset_timeframe(self):
        self.start = None
        self.stop = None

    def set_timeframe(self, start, stop):
        self.start = pd.to_datetime(start)
        self.end =  pd.to_datetime(stop)

        if type(self.start) is not pd.tslib.Timestamp or type(self.end) is not pd.tslib.Timestamp :
            raise ValueError("'start' or 'stop' are not a valid date time")

    def get_data(self):
        if self.start and self.end: 
            return self.df[ (self.df[self.timestamp_column] > self.start) & (self.df[self.timestamp_column] < self.end) ]
        else :
            return  self.df

    def __iter__(self):
        """
        Iterate over the corpus, returning a tuple with text as a 'str' and timestamp as a 'datetime' object.
        """

        for index, row in self.get_data().iterrows():
            text = any2utf8(row[self.text_column])
            yield(text, row[self.timestamp_column], row[self.source_column])
            self.length =  self.length + 1  # store the total number of CSV rows

    def __len__(self):
        """ this gives the length of the corpus - works only it has already been processed once"""
        return self.get_data().shape[0]
