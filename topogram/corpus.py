#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pickle
import logging
from datetime import datetime

from utils import any2utf8

logger = logging.getLogger('topogram.corpus')

class Corpus:
    """
    Interface (abstract base class) for corpora.

    Objects which inherit from this class have save/load functions, which un/pickle
    them to disk. 
    This uses pickle for de/serializing, so objects must not contain 
    unpicklable attributes, such as lambda functions etc.

    """

    def __init__(self,  
                 typeof,
                 timestamp="created_at", 
                 time_pattern="%Y-%m-%dT%H:%M:%S", 
                 content="text", 
                 origin="user_id", 
                 adds = []
                 ):

        self.type = typeof
        self.timestamp = timestamp # time
        self.time_pattern = time_pattern # if timestamp is a datetime already use None else use %time parser
        self.content = content # some content
        self.origin = origin # origin column
        self.adds = adds # additional columns

    def __iter__(self):
        """
        Iterate over the corpus, yielding one document at a time.
        """
        raise NotImplementedError('cannot instantiate abstract base class')

    def __len__(self):
        """
        Return the number of documents in the corpus.
        """
        raise NotImplementedError("must override __len__() before calling len(corpus)")

    def to_JSON(self):
        """ Serialize the whole corpus to JSON"""
        # return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)
        raise NotImplementedError("dump the corpus")

    def load_from_JSON(self,data):
        """ Load from a serialized JSON"""
        # self.__dict__ = data
        raise NotImplementedError("load the corpus")


    def __call__(self, row, validation=False):
        """
        Receive a dict or an array of data and parse it according to the description
        
        """

        result = {}

        # parse content
        content = row[any2utf8( self.content )]
        if type(content) is str : result["content"] = any2utf8(content)
        else : result["content"] = content

        # parse time
        if self.time_pattern  is None : 
            result["timestamp"] = row[any2utf8(self.timestamp)] # already a datetime 
        else : 
            result["timestamp"] = datetime.strptime(row[any2utf8(self.timestamp)], self.time_pattern)

        # origin 
        origin = row[any2utf8(self.origin)]
        if type(origin) is str : result["origin"] = any2utf8(origin)
        else: result["origin"] = origin

        # additional fields
        for column_name in self.adds :
            try : 
                result[any2utf8(column_name)] = row[any2utf8(column_name)]
            except:
                result[any2utf8(column_name)] = None
        return result

    # def load(cls, fname):
    #     """
    #     Load a previously saved object from file (also see `save`).
    #     """

    #     with open(fname) as f:
    #         obj = pickle.load(f)
    #         self.__dict__ = obj
    #         return obj

    # def save(self, fname, protocol=-1):
    #     """
    #     Save the object to file (also see `load`).
    #     """
    #     with open(fname, 'wb') as fout: # 'b' for binary, needed on Windows
    #         pickle.dump(__self__.dict, fout, protocol=protocol)
