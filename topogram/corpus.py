#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pickle
import logging
from datetime import datetime
from dateutil import parser

import json
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
                 time_pattern=None, 
                 content="text", 
                 origin="user_id",
                 longitude=None,
                 latitude=None, 
                 adds=[]
                 ):

        self.format = self.parse_keys(typeof)
        self.timestamp = self.parse_keys(timestamp) # time
        
        self.content = self.parse_keys(content) # some content
        self.origin = self.parse_keys(origin) # origin column
        self.adds = self.parse_keys(adds) # additional columns
        
        self.longitude = self.parse_keys(longitude) #longitude
        self.latitude = self.parse_keys(latitude) #latitude

        if time_pattern is None : 
            self.time_pattern = None
        elif isinstance(time_pattern, datetime) : 
            self.time_pattern = time_pattern
        else: 
           self.time_pattern = any2utf8(time_pattern) 

        # if timestamp is a datetime already use None else use %time parser
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
        
        if self.format == "json" :
            row = json.loads(row)

        # is already a dict
        result = {}

        # parse content
        content = self.lookup(row, self.content)

        if type(content) is str : 
            result["content"] = any2utf8(content)
        else : 
            result["content"] = content

        # parse time
        ts = self.lookup(row, self.timestamp)
        
        if self.time_pattern is None : 
            result["timestamp"] = parser.parse(ts)
        elif isinstance(self.time_pattern, datetime) : 
            result["timestamp"] =  ts# already a datetime 
        else : 
            result["timestamp"] = datetime.strptime(ts, self.time_pattern)

        # origin 
        origin = self.lookup(row, self.origin)

        if type(origin) is str : 
            result["origin"] = any2utf8(origin)
        else: 
            result["origin"] = origin
        #longitude
        if self.longitude is not None:
            result["longitude"] = self.lookup(row, self.longitude)
        #latitude
        if self.latitude is not None:
            result["latitude"] = self.lookup(row, self.latitude)


        # additional fields
        for column_name in self.adds :
            try : 
                result[column_name] = self.lookup(row, column_name)
            except:
                result[column_name] = None

        return result


    def parse_keys(self, keys):
        """Check if it is a list and parse each element into a proper format"""
        if keys is None : return None

        if type(keys) is list :
            return [self.parse_key(key) for key in keys]
        else : 
            return self.parse_key(keys)

    def parse_key(self, key): 
        """Extract JS-like path from key"""

        if type(key) is not str :
            raise ValueError("Keys should be str")

        path= key.split(".")

        if len(path) == 1 : # is a string without a path
            return any2utf8(key)

        else : # is a JS path like "this.property"
            return [any2utf8(i) for i in path]

    def lookup(self, dic, key):
        """Get a dict property from a key or a list of keys
            dic : a dict object
            key : a str or a list 
        """
        if type(key) is list:
            d = dic
            for k in key :
                try :
                    d= d.get(k)
                except :
                    return None
            return d
        else :
            return dic.get(key) 


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
