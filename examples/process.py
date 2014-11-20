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
meme_id=ObjectId("546cdd54ab4fc838d23cd947")
meme=db["memes"].find_one({ "_id" : meme_id })

# create topogram object
weibo= Topogram(["zh"])

# specific stopwords for weibo

stopwords=[]
# weibo_stopwords=os.path.join(os.getcwd(), "examples/stopwords/weibo.txt")
# stopwords+=[i.strip() for i in open(weibo_stopwords,"r")]

stopwords+=["转发","微博","说 ","一个","【 ","年 ","转 ","请","＂ ","问题","知道","中 ","已经","现在","说","【",'＂',"年","中","今天","应该","真的","月","希望","想","日","这是","太","转","支持", "@", "。", "/", "！","？",".",",","?","、","。","“","”","《","》","！","，","：","；","？",":","；","[","]","；",".", ".","."]

for word in stopwords : weibo.add_stopword(word, "zh")

# stop regexp
urlPattern=r"\b(([\w-]+://?|www[.])[^\s()<>]+(?:\([\w\d]+\)|([^\p{P}\s]|/)))"
hashtagPattern=r"#([^#\s]+)#"

weibo.set_stop_regexp(urlPattern)
weibo.set_stop_regexp(hashtagPattern)

# TIMESTAMP
weibo.timestamp_column="created_at"    # timestamp column name
weibo.time_pattern="%Y-%m-%dT%H:%M:%S" # timestamp pattern

# CITATIONS
weibo.source_column="uid"
weibo.additional_citations_column="retweeted_uid"

MentionPattern =r"@([^:：,，\)\(（）|\\\s]+)"
weibo.set_citation_regexp(MentionPattern)

# add citations to be ignored
ignore=["ukn", "ukn：","ukn："]
for ign in ignore :
    weibo.add_citation_exception(ign)

# GO !
for message in meme["messages"]:
    weibo.process(message)

weibo.create_networks()

weibo.create_timeframes()

timeframes_file='data.json'
with open(timeframes_file, 'w') as outfile:
    outfile.write(weibo.to_JSON())
    print "json file saved to %s"%(timeframes_file)

# test_id=db.test.insert(json.loads(weibo.to_JSON()))
db.memes.update({
               '_id':meme_id
               },{
               '$set':{
                "timeframes": json.loads(weibo.to_JSON())
                 }
            })
# print "saved in mongo as ",test_id
