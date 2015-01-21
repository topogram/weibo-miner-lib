#!/usr/bin/env python
# -*- coding: utf-8 -*-

from topogram.corpus import Corpus
from topogram.utils import any2utf8

import pandas as pd

import logging
logger = logging.getLogger('topogram.corpora.elastic')

class ElasticCorpus(Corpus): 
    """
    Corpus index with elasticsearch

    """
    def __init__(self, elastic_instance, index_name, query="query"):
        self.elastic = elastic_instance
        self.index_name = index_name
        self.query = query

        # Get the total number of results
        res = self.elastic.search(query,index=index_name)
        self.length = res['hits']['total']

        # logger.info( "%n results in elasticsearch search"%self.total)
        self.chunk = 0
        self.chunksize = 10

    def __len__(self):
        return self.length

    def __iter__(self):
        """
        We process results by chunk to free more memory 
        """
        i=0
        for chunk in xrange(0, len(self), self.chunksize):
            results=self.elastic.search(self.query, index=self.index_name, size=self.chunksize, es_from=self.chunk)

            # percentage of completion
            per=round(float(chunk)/len(self)*100, 1)
            if chunk +self.chunksize > len(self) : per = 100

            for message in results["hits"]["hits"] :
                yield message['_source']


    # def get_results_by_chunk(self):
    #     chunksize=200
    #         i=0
    #         # display progress as percent

    #         # request data
    #         messages=[]
    #         for message in res['hits']["hits"]:
    #             yield message
