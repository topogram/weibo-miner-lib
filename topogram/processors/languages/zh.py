#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import jieba
import jieba.analyse
from topogram.utils import any2utf8

here = os.path.dirname(os.path.abspath(__file__))

# Chinese methods
def add_support():
    # add better support for traditional character
    dico_file=os.path.join(here,'dict/dict.txt.big')
    jieba.set_dictionary(dico_file)

def extract_keywords(txt):
    """ Extract keywords from Chinese text""" 
    tags = jieba.analyse.extract_tags(txt, 20)
    return [ any2utf8(tag) for tag in tags]

def extract_dictionary(txt):
    """ Extract from Chinese text"""
    seg_list = jieba.cut(txt, cut_all=False)  # 搜索引擎模式
    return list(seg_list)
