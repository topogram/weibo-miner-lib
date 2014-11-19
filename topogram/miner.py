import os
from time import time

text_column="text"
timestamp_column="created_at"
time_pattern="%Y-%m-%dT%H:%M:%S"
language="zh"
message_type="weibo"


def check():
    return "haha"

def create_stopwords_list(message_type, language):
    stoplist=[]

    # specific pattern
    stop_message_type=os.path.abspath(os.path.join(os.path.dirname(__file__), "lib/stopwords/"+ message_type +".txt"))
    stoplist=[i.strip() for i in open(stop_message_type,"r")]

    # language
    stop_language=os.path.abspath(os.path.join(os.path.dirname(__file__), "lib/stopwords/"+ language +".txt"))
    stoplist+=[i.strip() for i in open(stop_language,"r")]

    # weibo additional
    if(stop_message_type == "weibo"):
        stoplist+=["转发","微博","说 ","一个","【 ","年 ","转 ","请","＂ ","问题","知道","中 ","已经","现在","说","【",'＂',"年","中","今天","应该","真的","月","希望","想","日","这是","太","转","支持"]

    return stoplist

def analyse_text(meme_id, citation_regexp, text_column, timestamp_column, time_pattern, language):

    meme=mongo.db.memes.find_one({ "_id" : meme_id })
    for row in meme["messages"]:


