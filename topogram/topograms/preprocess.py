#!/usr/bin/env python
# -*- coding: utf-8 -*-

from topogram.topogram import Topogram

import logging 
logger = logging.getLogger('topogram.topograms.basic')

class NLPPreProcess(Topogram):
    """
    Simple topogram to extract citations networks and co-occurence of words in documents.
    """

    def process(self):
        """ process the whole corpus"""
        logger.info("Start processing the corpus")
        for i, row in enumerate(self.corpus):
            # if i ==10 : break
            print row

            # logger.info("new row")
            txt = row["text_column"]

            clean = self.nlp.filter_out_regexps(txt)
            keywords = self.nlp.get_words(clean)
            row["text_column"] = keywords
            yield row

