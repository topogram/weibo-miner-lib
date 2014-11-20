#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import csv
import json
from topogram import Topogram

print "start weibo"

# specific stopwords for weibo
stopwords=["转发","微博","说 ","一个","【 ","年 ","转 ","请","＂ ","问题","知道","中 ","已经","现在","说","【",'＂',"年","中","今天","应该","真的","月","希望","想","日","这是","太","转","支持", "@", "。", "/", "！","？",".",",","?","、","。","“","”","《","》","！","，","：","；","？",":","；","[","]","；",".", ".","."]

# # TIMESTAMP
# weibo.timestamp_column="created_at"    # timestamp column name
# weibo.text_column="text"
# weibo.source_column="uid"
# weibo.additional_citations_column="retweeted_uid"

MentionPattern =r"@([^:：,，\)\(（）|\\\s]+)"

# create topogram object
weibo= Topogram(languages=["zh"], stopwords=stopwords, citation_regexp=MentionPattern)

# add citations to be ignored
ignore=["ukn", "ukn：","ukn："]
for ign in ignore :
    weibo.add_citation_exception(ign)

# add regexp to ignore
urlPattern=r"\b(([\w-]+://?|www[.])[^\s()<>]+(?:\([\w\d]+\)|([^\p{P}\s]|/)))"
hashtagPattern=r"#([^#\s]+)#"
weibo.set_stop_regexp(urlPattern)
weibo.set_stop_regexp(hashtagPattern)

# GO !
weibo.time_pattern="%Y-%m-%d %H:%M:%S" # timestamp pattern


with open('sampleweibo.csv', 'rb') as csvfile:
     reader = csv.DictReader(csvfile)
     for row in reader:
        weibo.process(row)

weibo.create_networks()
weibo.create_timeframes()

# save as json
timeframes_file='data.json'
with open(timeframes_file, 'w') as outfile:
    outfile.write(weibo.timeframes_to_JSON())
    print "json file saved to %s"%(timeframes_file)
