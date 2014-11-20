#!/usr/bin/env python
# -*- coding: utf-8 -*-

import jieba 
import jieba.analyse
from os import path

here=path.dirname(path.abspath(__file__))

class NLP:
    def __init__(self, language): 
        print "init NLP toolkit"

        # parse list of stopwords
        

        if language == "zh":
            stopwords_file=path.join(here,path.join("stopwords",language+".txt"))
            self.stopwords=[]
            self.stopwords+=[i.strip() for i in open(stopwords_file,"r")]
            
            dico_file=path.join(here,'dict/dict.txt.big')
            
            # add better support for traditional character
            jieba.set_dictionary(dico_file)
            
            # setup word extractor
            # self.extract_keywords = self.zh_extract_keywords
            self.extract_dictionary = self.zh_extract_dictionary

        else :
            raise NotImplementedError("More languages to come...")

    def zh_extract_keywords(self,txt):
        """ Extract keywords from Chinese text""" 
        tags = jieba.analyse.extract_tags(txt, 20)
        return tags

    def zh_extract_dictionary(self,txt):
        """ Extract from Chinese text"""
        seg_list = jieba.cut(txt, cut_all=False)  # 搜索引擎模式
        return list(seg_list)

    def get_words(self, txt):
        """ Get words w/o stopwords. Returns a list of words"""
        dico=self.extract_dictionary(txt)
        words=[w for w in dico if w.encode('utf-8') not in self.stopwords]
        return dico

    def add_stopword(self, word): 
        """ Add a stopword to the list of stopwords"""
        self.stopwords.append(word)

    def filter_stopwords(self,txt):
        """ Remove stopwords from text"""
        txt_wo_stopwords=[w for w in txt if w not in self.stopwords]
        return txt_wo_stopwords
