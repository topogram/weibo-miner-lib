#!/usr/bin/env python
# -*- coding: utf-8 -*-

from topogram.vizparser import Visualizer
from collections import Counter

class MapPoint(Visualizer):

    def __init__(self, content=None): 
        self.coordinates=[]

        print content
        if content is not None: self.content = {}
        else : self.content = None

    def to_JSON(self):
        count = dict( self.count() )

        if self.content is not None: 
            array_result = [{ "content" : self.content[c], "latitude" : c[0], "longitude" : c[1], "count" :count[c] } for c in count]
        else :
            array_result = [{ "latitude" : c[0], "longitude" : c[1], "count" :count[c] } for c in count]

        return array_result

    def from_JSON(self):
    	pass

    def __call__(self, row):

        coords = (row["latitude"], row["longitude"])
        if self.content is not None: 
            self.content[ coords ] = row["content"]

        self.coordinates.append( coords  )

    def count(self):
        tab_coordinates=Counter(self.coordinates)
        return tab_coordinates
