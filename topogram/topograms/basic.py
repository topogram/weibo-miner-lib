#!/usr/bin/env python
# -*- coding: utf-8 -*-

from topogram.topogram import Topogram

import logging 
logger = logging.getLogger('topogram.topograms.basic')


class BasicTopogram(Topogram):
    """
    Simple topogram to extract citations networks and co-occurence of words in documents.
    """

    def process(self):
        """ process the whole corpus"""

        for row in self.corpus:
            # print row
            self.process_row(row)

        logger.info("All row processed. %d documents"%self.corpus.length)
        logger.info("All row processed. %d words and %d edges"%(self.words.number_of_nodes(), self.words.number_of_edges() ), )
        logger.info("All row processed. %d citations and %d edges"%(self.citations.number_of_nodes(), self.citations.number_of_edges() ), )

    def process_row(self, row) :
        """
        Extract citations from a single row of raw data.
        """
        # logger.info("new row")

        txt = row[0]
        timestamp = [1]
        source = [2]

        # words co-ocurence
        keywords = self.nlp.extract_keywords(txt)
        for w1 in keywords:
            for w2 in keywords : 
                if w1!=w2 :
                    self.words.add_edge(w1, w2, { "timestamp" : timestamp})

        # citations
        source = self.corpus.source_column
        citations = self.extract_citations(txt)

        for citation in citations :
            self.citations.add_edge( source, citation,{ "timestamp" : timestamp})

        # if self.additional_citations_column != None : 
        #     if row[self.additional_citations_column] != None:
        #         citations.append( (row[self.additional_citations_column], row[self.source_column]) )
        #         if row[self.additional_citations_column] not in cited : cited.append(row[self.additional_citations_column])

        # words to citations
        for w in keywords:
            for u in citations:
                self.words_to_citations.add_edge(w,u)
