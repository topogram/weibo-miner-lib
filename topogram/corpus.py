#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pickle
import logging

logger = logging.getLogger('topogram.corpus')

class Corpus:
    """
    Interface (abstract base class) for corpora.

    Objects which inherit from this class have save/load functions, which un/pickle
    them to disk. 
    This uses pickle for de/serializing, so objects must not contain 
    unpicklable attributes, such as lambda functions etc.

    """

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
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

    def load_from_JSON(self,data):
        """ Load from a serialized JSON"""
        # self.__dict__ = data
        raise NotImplementedError("load the corpus")

    def load(cls, fname):
        """
        Load a previously saved object from file (also see `save`).
        """

        with open(fname) as f:
            obj = pickle.load(f)
            self.__dict__ = obj
            return obj

    def save(self, fname, protocol=-1):
        """
        Save the object to file (also see `load`).
        """
        with open(fname, 'wb') as fout: # 'b' for binary, needed on Windows
            pickle.dump(__self__.dict, fout, protocol=protocol)
