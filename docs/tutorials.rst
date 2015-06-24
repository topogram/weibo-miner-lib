**********
Tutorials 
**********

Topogram+Mongo
########

For this tutorial, you need to have `mongo DB <https://www.mongodb.org/>` installed.


Quick install
=============

>>> pip install pymongo topogram


The data
=============

Our data looks like this : 

::

    {
            "id": "9886947",
            "artist_event_id": "11977062",
            "title": "Kiss @ Donington Park in Derby, United Kingdom",
            "datetime": "2015-06-14T12:30:00",
            "formatted_datetime": "Sunday, June 14, 2015 at 12:30PM",
            "formatted_location": "Derby, United Kingdom",
            "ticket_url": "http://www.bandsintown.com/event/9886947/buy_tickets?artist=Kiss&came_from=111",
            "ticket_type": "Tickets",
            "ticket_status": "available",
            "on_sale_datetime": "2015-03-19T21:36:00",
            "facebook_rsvp_url": "http://www.bandsintown.com/event/9886947/facebook_rsvp?artist=Kiss",
            "description": "Download Festival 2015",
            "artists": [
                {
                    "id": 50049,
                    "name": "Kiss",
                    "url": "Kiss",
                    "image_url": "http://www.bandsintown.com/Kiss/photo/medium.jpg",
                    "thumb_url": "http://www.bandsintown.com/Kiss/photo/small.jpg",
                    "large_image_url": "http://www.bandsintown.com/Kiss/photo/large.jpg",
                    "on_tour": true,
                    "events_url": "https://app.bandsintown.com/artists/Kiss/events",
                    "sony_id": "2adda192840e49ad8c889c3e560d667a",
                    "tracker_count": 720695,
                    "verified": false,
                    "media_id": 2587848
                }
            ],
            "venue": {
                "name": "Donington Park",
                "address": "Castle Donington",
                "city": "Derby",
                "region": null,
                "country": "United Kingdom",
                "latitude": 52.828337,
                "longitude": -1.372481
            },
            "facebook_event_id": "1497232913870902",
            "rsvp_count": 24,
            "media_id": null
        },


Setup a mongo connection
=================

We want to find data from mongo, then to  use the Corpus to parse it properly.

::

    from pymongo import MongoClient

    # setup mongo
    client = MongoClient()
    db = client["bandstour"]
    bandsintown =  db["london_bandsintown"]

Describe your dataset into a corpus

::

    from topogram.corpus import Corpus
 
    # init corpus
    corpus = Corpus(
        "dict",
        timestamp_column = "datetime",
        time_pattern = None,
        content_column ="venue",
        origin_column ="artists",
        additional_columns = [ "artist_event_id", "description"]
    )

Select a pre-processor
========

Chose  a preprocessor that will help us to parse the date properly (by day) and initialize it 

:: 

    from topogram.processors.time_rounder import TimeRounder

    time_rounder = TimeRounder("day") # init processor


Chose a visualization model
==============

Chose a visualization container to represent a time series of the shows. This won't get any visualization but will prepare the data so showing it will be piece of cake after.

:: 

    from topogram.vizparsers.time_series import TimeSeries
    
    timeseries = TimeSeries() # init viz parsers

The pipeline
==============

Now let's plug all those pieces together : get the data from mongo, format it properly, preprocess the date by day and count all show for each date.

:: 

    # get records from Mongo
    for record in bandsintown.find() :

        # stream to corpus
        clean_data = corpus(record) # output correctly formatted

        # pre-process the data
        time_by_day = time_rounder(clean_data["time_column"])

        # load data into viz container 
        timeseries(time_by_day)

The best part : let's export it to use with a visualization tool.

>>> print timeseries.to_JSON() 


Topogram + CSV Corpus
########

.. module:: topogram


The data
======

This is sample of CSV data from the Chinese social network Sina Weibo.

::

    mid,retweeted_status_mid,uid,retweeted_uid,source,image,text,geo,created_at,deleted_last_seen,permission_denied
    mCClUNCqwe,mU5j0dIAkQ,uK3RXUJ0V,,新浪微博,0,转发微博,,2012-01-03 02:02:27,,
    mRsOcOLTlc,mJGNX5nAmo,uK3RXUJ0V,,新浪微博,0,!!!!!!!!!@uK3RXUYW3： //@u0AGMTTVD：  ！！！！！！！！,,2012-01-03 01:17:39,,
    mH44qG6iUm,mH44qL9LlF,uK3RXUJ0V,,新浪微博,0,求一切順利!!!,,2012-01-03 01:15:36,,
    mZmwFtOdVX,mcyE5GR7GJ,uK3RXUJ0V,,新浪微博,0,想要><@uK3RXUYW3： //@ukn：  全都想要啊QAQ,,2012-01-03 01:12:55,,
    mQkLJSl8bf,muy8VxftBB,uK3RXUJ0V,,新浪微博,0,//@ukn：  //@uMLLV3ZCO：  转发微博,,2012-01-03 01:10:42,,
    mnzrsoGWNN,mNfGcUeZbK,uK3RXUJ0V,,新浪微博,0,//@ukn：  //@ukn：  吐槽点太多- -//@ukn：  竟然没被吐槽//@ukn：  [偷笑]//@ukn：  而且竟然没有人吐槽他！,,2012-01-03 01:09:54,,
    m2rVkbmLsg,m7nJhJ3W6z,uK3RXUJ0V,,新浪微博,0,係時侯迫害下大家~@uK3RXUYW3： @ukn： @ukn： @uQSMQTGXO： @BOICE_yeeman,,2012-01-03 01:08:45,,
    mNfG6Xsbx5,mex2cwWppM,uK3RXUJ0V,,新浪微博,0,他又抽了xdd,,2012-01-03 00:54:07,,
    mCVHzsScoY,m7nJ3YBbyo,uK3RXUJ0V,,新浪微博,0,哈哈哈,,2012-01-03 00:51:52,,
    mdO3bmDotD,mqUTC9xyyM,uK3RXUJ0V,,新浪微博,0,@uK3RXUYW3： //@ukn：  //@ukn：  [可怜][可怜],,2012-01-03 00:44:08,,
    mu9iEJwbEt,mPoMqa8zoK,uK3RXUJ0V,,新浪微博,0,太萌了><//@uKPK1KLQA：  边叠衣服边「味覚トゥッ~」也太萌了[发嗲],,2012-01-03 00:38:10,,
    mT51VdbRj7,mrMzWfd2nM,uK3RXUJ0V,,新浪微博,0,//@ukn：  ！！！,,2012-01-02 23:00:13,,
    m3zb0aii82,mSazECdURr,uK3RXUJ0V,,新浪微博,0,霸气~//@ukn：  [太開心]//@uW0ECUEMG：  [good]//@ukn：  噗 //@uJWAI1YNJ： 好霸气。。 // @uCBTBLHPS： :すげー // @ukn： :XD明天真的满满arashi,,2012-01-02 22:58:52,,
    m2X81ImxzY,m9hq3KZgSv,uK3RXUJ0V,,新浪微博,0,//@ukn：  //@uOQZ5JAJB：  5.利达从头到尾都很紧张的样子，让看着的我都担心起来。除了要好好的完成自己的任务，有时候还要替歌手的讲话圆场。感受到了利达的紧张，nino在中途拍拍利达给他安慰。利达一定觉得安心了不少吧~6.迷宫。虽然磁石组一直抑制着，但还是互相眼神传情，颔首示意,,2012-01-02 22:51:06,,
    mT51V7GBde,mvIdeMIjOE,uK3RXUJ0V,,新浪微博,0,//@ukn：  //@ukn：  //@uVEQEW1R2：  //@ukn：  [心][心][心],,2012-01-02 22:47:58,,

First, we need to describe the file to parse it properly

::

    from topogram.corpus.csv_file import CSVCorpus 

    # import corpus
    csv_corpus = CSVCorpus('data.csv',
        origin ="user_id",
        content ="text",
        timestamp ="created_at",
        time_pattern="%Y-%m-%d %H:%M:%S",
        adds = ["permission_denied", "deleted_last_seen"])

    # validate CSV corpus formatting
    try :
        csv_corpus.validateCSV()
    except ValueError, e:
        print e.message, 422



Select multiple pre-processors
========

::

    from topogram import Topogram
    from topogram.processors.nlp import NLP
    from topogram.processors.regexp import Regexp

    # init processors
    chinese_nlp = NLP("zh")
    url = Regexp(r"\b(([\w-]+://?|www[.])[^\s()<>]+(?:\([\w\d]+\)|([^\p{P}\s]|/)))")

    # init 
    topogram = Topogram(corpus=csv_corpus, processors=[("zh", chinese_nlp), ("urls", url)])


Chose a visualization model
==============

::

    from topogram.vizparsers.network import Network

    # create viz model
    words_network = Network( directed=False )

    for row in topogram.process():
        words_network.add_edges_from_nodes_list(row["zh"])

    # get processed graph as d3js json
    print words_network.get(nodes_count=1000, min_edge_weight=3, json=True)
