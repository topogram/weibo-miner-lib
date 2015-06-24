#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pymongo import MongoClient

from topogram.corpus import Corpus
from topogram.processors.time_rounder import TimeRounder
from topogram.vizparsers.time_series import TimeSeries

import logging
import sys
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)


# setup mongo
client = MongoClient()
db = client["bandstour"]
bandsintown =  db["london_bandsintown"]

# init corpus
corpus = Corpus(
    dict,
    timestamp_column = "datetime",
    time_pattern = None,
    content_column ="venue",
    origin_column ="artists",
    additional_columns = [ "artist_event_id", "description"]
)

# init processors
time_rounder = TimeRounder("day")

# init viz parsers
timeseries = TimeSeries()

# get records from Mongo
for record in bandsintown.find() :

    # stream to corpus
    clean_data = corpus(record) # output correctly formatted

    # pre-process the data
    time_by_day = time_rounder(clean_data["time_column"])

    # load data into viz container 
    timeseries(time_by_day)

print timeseries.to_JSON()
