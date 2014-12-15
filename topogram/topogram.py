#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
from time import time
import datetime
import json
from nlp import NLP
from collections import Counter
import networkx as nx
import community


class Topogram:

    def __init__(self, 
                 languages=["en"], 
                 stopwords=[], 
                 timestamp_column="created_at",
                 time_pattern="%Y-%m-%dT%H:%M:%S",
                 text_column="text",
                 message_type="weibo",
                 source_column="uid",
                 citation_regexp=r"@([^:：,，\)\(（）|\\\s]+)",
                 additional_citations_column=None,
                 **kwargs):

        # columns mapping
        self.message_type=message_type
        self.text_column=text_column
        self.timestamp_column=timestamp_column
        self.time_pattern=time_pattern
        self.source_column=source_column
        self.additional_citations_column=additional_citations_column

        # regexp 
        self.citation_regexp=citation_regexp

        # internal data
        self.ignored_citations=[]
        self.ignored_text_regexp=[]
        self.cited=[]
        self.citations=[]
        self.words=[]
        self.words_to_words=[]
        self.words_to_cited=[]
        self.timeframes=[]
        self.words_edges={}
        self.by_time={}

        # deal with languages
        self.languages=languages
        self.nlp = {}
        if len(self.languages) == 1 : # only one language !
            self.create_nlp(self.languages[0])
            if len(stopwords): 
                for word in stopwords : self.add_stopword(word, languages[0])
        else :
            raise NotImplementedError("Multiple languages yet to come...")

    # NLP
    def create_nlp(self,language):
        """ Create a word extractor from different languages"""
        self.nlp[language]=NLP(language)

    def add_stopword(self, word, language):
        """ Add specific stopword"""
        self.nlp[language].add_stopword(word)

    def set_stop_regexp(self, regexp):
        self.ignored_text_regexp.append(regexp)

    def get_stop_regexp(self):
        reg=[]
        for regexp in self.ignored_text_regexp:
            reg.append(re.compile(regexp, re.UNICODE))
        return reg

    def get_clean_text(self, txt):
        """ Remove elements following patterns"""
        clean=txt
        for regexp in self.get_stop_regexp():
            for junks in regexp.findall(txt):
                if type(junks) is str:
                    clean=clean.replace(junks,"")
                else :
                    for junk in junks:
                        clean=clean.replace(junk,"")
        return clean

    # citations
    def set_citation_regexp(self, regexp):
        """ Setup regexp pattern to extract citation from text"""
        self.set_stop_regexp(regexp)
        self.citation_regexp=regexp

    def get_citation_regexp(self):
        return re.compile(self.citation_regexp, re.UNICODE)

    def add_citation_exception(self, exception):
        if type(exception) is str:
            self.ignored_citations.append(exception.decode("utf-8"))
        elif type(exception) is unicode:
            self.ignored_citations.append(exception)
        else :
            raise TypeError("wrong exception type (unicode or str excepted)", type(exception))

    def extract_citations(self, txt):
        """ Extract citations. 
            Return a list of citations
        """
        citations=[]
        for citation in self.get_citation_regexp().findall(txt):
            if citation not in self.ignored_citations:
                citations.append(citation)
        return citations

    # time
    def get_timeframe(self,timestamp):
        # time (round and store)
        d=datetime.datetime.strptime(timestamp, self.time_pattern)
        day = datetime.datetime(d.year,d.month,d.day,d.hour,0,0) 
        timeframe=day.strftime("%s")
        return timeframe

    def add_by_time(self,timestamp,key,value):

        # create time slot
        try : self.by_time[timestamp]
        except KeyError: self.by_time[timestamp]={}

        # create value in time slot
        try: self.by_time[timestamp][key]
        except KeyError: self.by_time[timestamp][key]=[]

        self.by_time[timestamp][key]+=value

    def process(self, row) :
        """Launch the network analysis process"""
        print "-"*10
        
        # CITATIONS
        citations=[]
        cited=[]

        cited.append(row[self.source_column])

        cited_list=self.extract_citations(row[self.text_column])

        for c in cited_list : 
            citations.append( (row[self.source_column],c) )
            if c not in cited : cited.append(c)

        if self.additional_citations_column != None : 
            if row[self.additional_citations_column] != None:
                citations.append( (row[self.additional_citations_column], row[self.source_column]) )
                if row[self.additional_citations_column] not in cited : cited.append(row[self.additional_citations_column])

        # global lists
        self.citations += citations
        self.cited += [c for c in cited if c not in self.cited ]

        if row[self.source_column] not in self.cited: self.cited.append(row[self.source_column])

        # TEXT
        clean=self.get_clean_text(row[self.text_column])
        language= "zh" # TODO : detect language

        words=self.nlp[language].get_words(clean)

        words_to_words=[]
        words_to_cited=[]

        for w in words:
            words_to_words+=[(w,t) for t in words if t!=w]
            words_to_cited+=[(w,u) for u in citations]

            if "." not in w: #  char '.' in key not allowed
                try: self.words_edges[w]
                except KeyError: self.words_edges[w]=[]
                self.words_edges[w]+=[t for t in words if t!=w]

        # global list
        self.words+=[w for w in words if w not in self.words]
        self.words_to_words+=words_to_words
        self.words_to_cited+=words_to_cited

        # store data by time
        timestamp=self.get_timeframe(row[self.timestamp_column])

        return {
            "timestamp" : timestamp,
            "words_nodes" : words,
            "words_edges" : words_to_words,
            "cited_edges" : citations,
            "cited_nodes" : cited,
            "words_cited_edges" : words_to_cited
        }

    def create_by_time(self, timed_info):

        self.add_by_time(timed_info["timestamp"],"words_nodes",timed_info["words_nodes"])
        self.add_by_time(timed_info["timestamp"],"words_edges",timed_info["words_edges"])

        self.add_by_time(timed_info["timestamp"],"cited_edges",timed_info["cited_edges"])
        self.add_by_time(timed_info["timestamp"],"cited_nodes",timed_info["cited_nodes"])

        self.add_by_time(timed_info["timestamp"],"words_cited_edges",timed_info["words_cited_edges"])


    def load_from_processed(self, message):

        # add by time
        self.create_by_time(message)

        # global lists
        self.citations += message["cited_edges"]
        self.cited += [c for c in message["cited_nodes"] if c not in self.cited ]
        self.words+=[w for w in message["words_nodes"] if w not in self.words]
        self.words_to_words+=message["words_edges"]
        self.words_to_cited+=message["words_cited_edges"]

    def get_top_nodes(self, nodes, limit):
        """ Apply a  size limit to an array"""
        return  [c[0] for c in Counter(nodes).most_common(limit)]

    def get_edges_containing_nodes(self, edges, top_nodes):
        """Keep only edges that contains specified nodes"""
        return [e for e in edges if e[0] in top_nodes and e[1] in top_nodes ]

    def get_weigthed_edges(self, edges, minimum_weight):

        return [
            (p[0][0],p[0][1],p[1]) 
            for p in Counter(tuple(edges)).most_common()
            if p[1]>minimum_weight
        ]

    # def create_network(self, nodes, weighted_edges):

    def create_network(self, nodes, edges, nodes_max_length, edges_min_weight):

        # limit network size
        top_nodes=self.get_top_nodes(nodes,nodes_max_length)
        print "%d top_nodes"%len(top_nodes)

        top_edges=self.get_edges_containing_nodes(edges, top_nodes)
        print "%d top_edges"%len(top_edges)

        weighted_edges = self.get_weigthed_edges(top_edges, edges_min_weight)

        weighted_edges_str=[
                str(nodes.index(w[0]))+" "+str(nodes.index(w[1]))+" "+str(w[2])
                for w in weighted_edges
                ]

        # create graph object
        G = nx.read_weighted_edgelist(weighted_edges_str, nodetype=str, delimiter=" ",create_using=nx.DiGraph())

        # dimensions
        N,K = G.order(), G.size()
        print "Nodes: ", N
        print "Edges: ", K

        return G

    def create_networks(self):
        print
        print "creating networks"

        # WORDS
        print "-"*10+" Words"
        words_graph= self.create_network(self.words, self.words_to_words, 20, 1)

        self.words_allowed=[self.words[int(w)] for w in words_graph.nodes()]
        print "%d words_allowed"%len(self.words_allowed)

        self.words_communities = community.best_partition(words_graph.to_undirected()) 
        print "Number of words partitions : ", len(set(self.words_communities.values()))

        # CITATIONS
        print
        print "-"*10+" Citations"
        citations_graph= self.create_network(self.cited, self.citations, 100, 0)

        self.cited_allowed=[self.cited[int(w)] for w in citations_graph.nodes()]
        print "%d cited_allowed"%len(self.cited_allowed)

        # Communities
        self.citations_communities = community.best_partition(citations_graph.to_undirected()) 
        print "Number of citations partitions : ", len(set(self.citations_communities.values()))

        print

    # OUTPUT DATA
    def create_timeframes(self):
        print 'Creating Timeframes'
        for timestamp in self.by_time:

            print "-"*12+str(timestamp)
            timeframe={}
            timeslot=self.by_time[timestamp]

            timeframe["cited_nodes"]=[{
                  "name":u[0],
                  "count":u[1],
                  # "community":user_communities[u[0]]
                  } 
                 for u in Counter(timeslot["cited_nodes"]).most_common() 
                 if u[0] in self.cited_allowed
                 ]
            print "%d cited"%len(timeframe["cited_nodes"])

            timeframe["cited_edges"]=[{
                "source":u[0][0],
                "target":u[0][1],
                "weight":u[1]
                } 
                for u in Counter(timeslot["cited_edges"]).most_common()
                if u[0][0] in self.cited_allowed
                and u[0][1] in self.cited_allowed
                ]
            print "%d citations"%len(timeframe["cited_edges"])

            timeframe["words_nodes"]=[{
                "name":w[0],
                "count":w[1],
                # "community":self.words_communities[str(w[0])]
                } 
                for w in Counter(timeslot["words_nodes"]).most_common()
                if w[0] in self.words_allowed
                ]
            print "%d words"%len(timeframe["words_nodes"])

            timeframe["words_edges"]=[{ 
                "source":w[0][0],
                "target":w[0][1],
                "weight":w[1]}
                for w in Counter(timeslot["words_edges"]).most_common()
                if w[0][1] in self.words_allowed
                and w[0][1] in self.words_allowed
                ]
            print "%d words edges"%len(timeframe["words_edges"])
            
            
            self.timeframes.append({"time":timestamp, "data":timeframe})
        
        print "Completed extraction for %d timeframes."%len(self.timeframes)
        print

    def timeframes_to_JSON(self):
        """ Serialize only useful parts to JSON"""
        return json.dumps(self.timeframes, default=lambda o: o.__dict__, sort_keys=True, indent=4)

    def to_JSON(self):
        """ Serialize the whole class to JSON"""
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

    def load_from_JSON(self,data):
        """ Load from a serialized JSON"""
        self.__dict__ = data
        self.words_to_words = [tuple(w) for w in self.words_to_words]
        self.citations = [tuple(w) for w in self.citations]

        for ts in self.by_time:
            tf=self.by_time[ts]
            # print tf["words_to_words"]
            tf["words_edges"]=[tuple(w) for w in tf["words_edges"]]

def sanitize_str(url):
    valid_utf8 = True
    try:
        url.decode('utf-8')
    except UnicodeDecodeError:
        valid_utf8 = False
        return url[:-1]
    return url

