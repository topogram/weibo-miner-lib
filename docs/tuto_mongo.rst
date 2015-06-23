**********
Tutorial Topogram+Mongo
**********

Before installing Topogram, you need to have `mongo DB <https://www.mongodb.org/>` installed.


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


Building a timeseries
=============

Setup our mongo connection to get data 

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
        dict,
        timestamp_column = "datetime",
        time_pattern = None,
        content_column ="venue",
        origin_column ="artists",
        additional_columns = [ "artist_event_id", "description"]
    )


Chose  a preprocessor that will help us to parse the date properly (by day) and initialize it 

:: 

    from topogram.processors.time_rounder import TimeRounder

    time_rounder = TimeRounder("day") # init processor


Chose a visualization container to represent a time series of the shows. This won't get any visualization but will prepare the data so showing it will be piece of cake after.

:: 

    from topogram.vizparsers.time_series import TimeSeries
    
    timeseries = TimeSeries() # init viz parsers


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
