#!/usr/bin/env python
# -*- coding: utf-8 -*-

from topogram.vizparser import Visualizer
from collections import Counter

class MapPoint(Visualizer):

    def __init__(self): 
    	self.coordinates=[]

    def to_JSON(self):
    	count = dict(self.count())

    	 
    	array_result = [{ "latitude" : c[0], "longitude" : c[1], "count" :count[c] } for c in count]
    	print array_result
    	# array_result = [count["latitude"] count["longitude"] for count in self.count()]
    	
    	return array_result

    def from_JSON(self):
    	pass

    def __call__(self, row):

    	self.coordinates.append((row["latitude"], row["longitude"]))

    def count(self):
    	tab_coordinates=Counter(self.coordinates)
    	return tab_coordinates
