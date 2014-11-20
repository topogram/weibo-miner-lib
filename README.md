# Topogram


A Python library for text analysis and time-based visualization of citations data as networks.

### How it works

INPUT

* Select multiple documents text and date (as csv columns)
* Define timestamp column and time formatting
* Define a regexp to extract citations
* Define a language
* (optional) define source and dest column
* (optional) add stop words and stop regexp to ignore expressions or citations


OUTPUT

* citations graph
* word co-occurence graph
* time-based data frames (by day or by hour)
* community detection (using Louvain algorithm)


Packages required
    
    jieba-0.35.zip (7.4MB)
    networkx
    python-louvain

### Example

    weibo = Topogram() # default template is for Sina Weibo

    # stream and analyze documents
    for message in messages:
        weibo.process(message)

    weibo.create_networks()
    weibo.create_timeframes()


### Stop words & expressions

    # stopwords by language
    weibo.add_stopword("haha", "en")

    # ignore specific citations name
    weibo.add_citation_exception("@justinbieber")
    
    # ignore hashtags
    hashtagPattern=r"#([^#\s]+)#"
    weibo.set_stop_regexp(hashtagPattern)

### Load & save

    backup = weibo.to_JSON() # you can save directly to a file or mongodb
    weibo.load_from_JSON(backup)
