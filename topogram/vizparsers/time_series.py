#!/usr/bin/env python
# -*- coding: utf-8 -*-

from topogram.vizparser import Visualizer
from topogram.processors.time_rounder import TimeRounder

from datetime import  datetime 
from collections import Counter

import logging 
logger = logging.getLogger('topogram.visualizers.timeseries')


class TimeSeries(Visualizer):

    def __init__(self, timescale="minute"):
        logger.info("Init timeseries viz parser graph ")

        authorized_timescales = ["second", "minute", "hour", "day", "month", "year"]
        if timescale not in authorized_timescales :
            raise ValueError("Unauthorized timescale (only : y,m,d,h,m,s)")

        self.timescale=timescale
        self.data=[]


    def add_time_point(self, timestamp, count=1):

        if not isinstance(timestamp , datetime) :
            raise ValueError("Not a valid datetime object")

        self.data.append(timestamp)

    def set_timescale(self, timescale):
        rounder = TimeRounder(timescale)
        newData=[rounder(d) for d in self.data] 
        self.data = newData
        self.timescale = timescale

    def compute_series(self):
        count= Counter([dt.strftime("%s") for dt in self.data])
        time_counts =  [ { "time" : d, "count" : count[d] } for d in count ]
        return time_counts

    def to_JSON(self):
        time_counts = self.compute_series()
        return time_counts

    def __len__(self):
        return len(self.data)

    def __call__(self, timestamp):
        
        if type(timestamp) is list :
            self.data += timestamp
        elif type(timestamp) is datetime :
           self.add_time_point(timestamp)
        else: 
            raise ValueError("Timeseries should be called with a datetime object or list of datetime objects")



