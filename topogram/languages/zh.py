#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import jieba
import jieba.analyse
from topogram.nlp import NLP
from topogram.utils import any2utf8

import logging 

logger = logging.getLogger('topogram.nlp.zh')
here = os.path.dirname(os.path.abspath(__file__))

# from topogram.utils import any2utf8

class ChineseNLP(NLP): 
    """
        NLP routines for Chinese Language
    """

    def __init__(self):

        logger.info("init Chinese NLP logger")
        self.stopwords=[" "]

        # parse chinese stopwords
        stopwords_file=os.path.join(here,os.path.join("stopwords","zh.txt"))
        self.stopwords+=[i.strip() for i in open(stopwords_file,"r")]

        print len(self.stopwords)

        # parse generic stopwords
        stopwords_file=os.path.join(here,os.path.join("stopwords","all.txt"))
        self.stopwords+=[i.strip() for i in open(stopwords_file,"r")]

        self.stop_regexps = []

        # add better support for traditional character
        dico_file=os.path.join(here,'dict/dict.txt.big')
        jieba.set_dictionary(dico_file)

    def extract_keywords(self,txt):
        """ Extract keywords from Chinese text""" 
        tags = jieba.analyse.extract_tags(txt, 20)
        return [ any2utf8(tag) for tag in tags]

    def extract_dictionary(self,txt):
        """ Extract from Chinese text"""
        seg_list = jieba.cut(txt, cut_all=False)  # 搜索引擎模式
        return list(seg_list)
