#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

######################## 
# Detect Tweet Entities 
######################## 


def init_tweet_regex():
    
    # patterns 
    MentionPattern =r"@([^:：,，\)\(（）|\\\s]+)"

    URLPattern=r"\b(([\w-]+://?|www[.])[^\s()<>]+(?:\([\w\d]+\)|([^\p{P}\s]|/)))"
    # hashtagPattern=r"[#]+([^|#]+)[#]"
    # hashtagPattern=r"(^|\s)#([^\s]+)#"
    hashtagPattern=r"#([^#\s]+)#"

    # compile reg
    regHash=re.compile(hashtagPattern, re.UNICODE)
    regRT=re.compile(MentionPattern, re.UNICODE)
    regURL=re.compile(URLPattern, re.UNICODE)

    print 'init tweet entities regex'

    return regHash, regRT, regURL

# init 
regHash, regRT, regURL = init_tweet_regex()

def sanitize_url(url):
    valid_utf8 = True
    try:
        url.decode('utf-8')
    except UnicodeDecodeError:
        valid_utf8 = False
        return url[:-1]
    return url

def extract_tweet_entities(txt):
    
    mentions=[]
    urls=[]
    hashtags=[]
    clean=txt

    for mention in regRT.findall(txt):
        # t.mentions.append(mention)
        if mention[0] == "u":
            if mention != "ukn":
                mentions.append(mention)

        # clean string
        m="@"+mention
        clean=txt.replace(m,"") # remove mentions

    for url in regURL.findall(txt):
        if url[0][0] == "h":
            # all urls follow the same pattern http://t.cn/aE5XRc (18 characters)
            u=sanitize_url(url[0][0:18])
            urls.append(u) 
        # t.urls.append(url[0])
        clean=clean.replace(url[0][0:18],"")

    for hashtag in regHash.findall(txt):
        hashtags.append(hashtag)
        # t.hashtags.append(hashtag)
        h='#'+hashtag+'#'
        clean=clean.replace(h,"")

    return mentions,urls,hashtags,clean
