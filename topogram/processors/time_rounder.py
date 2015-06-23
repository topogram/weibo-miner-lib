#!/usr/bin/env python
# -*- coding: utf-8 -*-

from topogram.processor import Processor

from datetime import  datetime 

class TimeRounder(Processor):

    def __init__(self, timescale):
        authorized_timescales = ["second", "minute", "hour", "day", "month", "year"]
        if timescale not in authorized_timescales :
            raise ValueError("Unauthorized timescale (only : y,m,d,h,m,s)")

        self.timescale= timescale

    def round_to_second(self,dt):
        return datetime(dt.year,dt.month,dt.day,dt.hour,dt.minute, dt.second)

    def round_to_minute(self,dt):
        return datetime(dt.year,dt.month,dt.day,dt.hour,dt.minute)

    def round_to_hour(self,dt):
        return datetime(dt.year,dt.month,dt.day,dt.hour)

    def round_to_day(self,dt):
        return datetime(dt.year, dt.month, dt.day )

    def round_to_month(self,dt):
        return datetime(dt.year, dt.month, 1)

    def round_to_year(self,dt):
        return datetime(dt.year, 1, 1)

    def __call__(self, timestamp):

        if not isinstance(timestamp , datetime) :
            raise ValueError("Not a valid datetime object")

        # parse function using str name
        function_name = "round_to_" + self.timescale
        getter = getattr( self, function_name)

        return  getter( timestamp )


