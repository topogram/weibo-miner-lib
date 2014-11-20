#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from pymongo import Connection
from bson import ObjectId
import json
from topogram import Topogram

print "start weibo"

# get data from mongo
host="localhost"
port=27017
connection = Connection(host=host, port=port)
db = connection["topogram"]
meme_id=ObjectId("546dd8c9ab4fc845187f410d")
meme=db["test"].find_one({ "_id" : meme_id })

# load data from DB
weibo=Topogram(["zh"])
weibo.load_from_JSON(meme)

print "%s words"%len(weibo.words)
print "%s words edges"%len(weibo.words_to_words)

print "%s cited"%len(weibo.cited)
print "%s citations"%len(weibo.citations)
print "%s timeframes"%len(weibo.by_time)
print

weibo.create_networks()
weibo.create_timeframes()

