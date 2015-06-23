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
        return count

    def to_JSON(self):
        counter = self.compute_series()
        return [ { "time" : d, "count" : counter[d] } for d in counter ]


    def __call__(self, timestamps):
        
        if type(timestamps) is not list :
            raise ValueError("Timeseries should be called with a list of datetime objects")

        self.data = timestamps


