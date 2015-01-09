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


        # raise UnicodeDecodeError("Your file is encoded with %s. Please use UTF-8 for better compatibility"%encoding["encoding"])
        # logger.warning("Your file is encoded with %s. Please use UTF-8 for better compatibility"%encoding["encoding"])
        # self.reader = unicodecsv.DictReader(codecs.open(self.fname, "r", encoding=self.encoding), dialect=self.dialect)

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
            text = any2utf8(row[any2utf8(self.text_column)])
            timestamp = datetime.strptime(row[any2utf8(self.timestamp_column)], self.time_pattern)
            yield(text, timestamp, row[any2utf8(self.source_column)])
            self.length =  self.length + 1  # store the total number of CSV rows

    def __len__(self):
        """ this gives the length of the corpus - works only it has already been processed once"""
        return self.length

class UnicodeDictReader:
    def __init__(self, f, fieldnames=None, restkey=None, restval=None,
                 dialect="excel", *args, **kwds):
        self.fieldnames = fieldnames    # list of keys for the dict
        self.restkey = restkey          # key to catch long rows
        self.restval = restval          # default value for short rows
        self.reader = csv.reader(f, dialect, *args, **kwds)

    def __iter__(self):
        return self

    def next(self):
        row = self.reader.next()
        if self.fieldnames is None:
            self.fieldnames = row
            row = self.reader.next()

        # unlike the basic reader, we prefer not to return blanks,
        # because we will typically wind up with a dict full of None
        # values
        while row == []:
            row = self.reader.next()
        d = dict(zip(self.fieldnames, row))
        lf = len(self.fieldnames)
        lr = len(row)
        if lf < lr:
            d[self.restkey] = row[lf:]
        elif lf > lr:
            for key in self.fieldnames[lr:]:
                d[key] = self.restval
        return d

# def UnicodeDictReader(utf8_data, **kwargs):
#     print repr(utf8_data)
#     csv_reader = csv.DictReader(utf8_data, **kwargs)
#     for row in csv_reader:
#         yield dict([(key, unicode(value, 'utf-8')) for key, value in row.iteritems()])

    # def set_timeframe(self, start, stop):
    #     self.start = pd.to_datetime(start)
    #     self.end =  pd.to_datetime(stop)

    #     if type(self.start) is not pd.tslib.Timestamp or type(self.end) is not pd.tslib.Timestamp :
    #         raise ValueError("'start' or 'stop' are not a valid date time")

    # def get_data(self):
    #     validate fields in CSV
    #     self.validate_csv()

    #     lazy load // open file w pandas // parse date
    #     date_parser = lambda x : datetime.strptime(x, self.time_pattern)
    #     self.df = pd.read_csv(self.fname, dialect=self.dialect, dtype=object, parse_dates=[self.timestamp_column], date_parser=date_parser, encoding="utf-8") # iterator=True, chunksize=100, 

    #     if self.start and self.end: 
    #         return self.df[ (self.df[self.timestamp_column] > self.start) & (self.df[self.timestamp_column] < self.end) ]
    #     else :
    #     return  self.df
