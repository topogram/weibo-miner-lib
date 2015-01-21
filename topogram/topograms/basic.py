#!/usr/bin/env python
# -*- coding: utf-8 -*-

from topogram.topogram import Topogram

import logging 
logger = logging.getLogger('topogram.topograms.basic')


class BasicTopogram(Topogram):
    """
    Simple topogram to extract citations networks and co-occurence of words in documents.
    """

    def process_row(self, row) :
        """
        Extract citations from a single row of raw data.
        """
        # logger.info("new row")
        txt = row["text_column"]
        timestamp = row["time_column"]
        source = row["source_column"]

        clean = self.nlp.filter_out_regexps(txt)

        # citations
        citations = self.extract_citations(clean)

        for citation in citations :
            self.add_citations_edge(source, citation)

        # words co-ocurence
        keywords = self.nlp.get_words(clean)
        for w1 in keywords:
            for w2 in keywords : 
                if w1!=w2 :
                    self.add_words_edge(w1, w2)

        # words to citations
        for w in keywords:
            for u in citations:
                self.words_to_citations.add_edge(w,u)

    def process(self):
        """ process the whole corpus"""
        logger.info("Start processing the corpus")
        for row in self.corpus:
            self.process_row(row)

        logger.info("All row processed. %d documents"%self.corpus.length)
        logger.info("All row processed. %d words and %d edges"%(self.words.number_of_nodes(), self.words.number_of_edges() ), )
        logger.info("All row processed. %d citations and %d edges"%(self.citations.number_of_nodes(), self.citations.number_of_edges() ), )
