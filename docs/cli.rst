******************************
Command-Line Interface
******************************

**The Command-Line interface is still in alpha-experimental-unstable phase. Use** :code:`topo-* --help` **command to get the lastest doc.**

How it works
=============

The basic principle is that you will describe all steps from raw data to clean visualization output using bash command and linux pipes.

Here is an example to extract a timeseries  from a JSON Array of objects.

>>> mongoexport --quiet --db bandstour --collection london_bandsintown  | topo-corpus -r venue -t 'datetime.$date'  -c 'artists' -j json   | topo-proc --processor 'timerounder' -c 'second' | topo-viz -v timeseries -o data/timeseries.json 

Now here is the translation step by step :

* We start with :code:`cat data.json` to read our raw Json file 
* We use :code:`jq '.[]'` to read and parse the JSON array using  `jq <http://stedolan.github.io/jq/>`_ 
* This :code:`bin/topo-corpus -c artists -r venue -t datetime -p %Y-%m-%d %H:%M:%S` is the format of each object inside the array (main keys and time format)
* :code:`topo-proc --timerounder day`
* :code:`topo-viz --timeseries`


Reference
=============

There is 3 main scripts which acts as wrappers for the 3 main features of topogram : topo-corpus, topo-proc and topo-viz

topo-corpus
##################

:: 

    $ bin/topo-corpus --help
    usage: topo-corpus [-h] --timestamp TIMESTAMP [--time-pattern TIME_PATTERN]
                       [--origin ORIGIN] --content CONTENT [--exclude EXCLUDE]
                       [--format FORMAT]
                       [infile] [outfile]

    positional arguments:
      infile                Specifies the intput file. The default is stdin.
      outfile               Specifies the output file. The default is stdout.

    optional arguments:
      -h, --help            show this help message and exit
      --timestamp TIMESTAMP, -t TIMESTAMP
      --time-pattern TIME_PATTERN, -p TIME_PATTERN
      --origin ORIGIN, -r ORIGIN
      --content CONTENT, -c CONTENT
      --exclude EXCLUDE, -e EXCLUDE
      --format FORMAT, -j FORMAT



topo-proc
#########

::

  $ bin/topo-proc -h
  usage: topo-proc [-h] -p PROCESSOR -c CONFIG [--format FORMAT] [-i [INFILE]]
                   [-o [OUTFILE]]

  optional arguments:
    -h, --help            show this help message and exit
    -p PROCESSOR, --processor PROCESSOR
                          Specifies the processor to use. Available : nlp,
                          timerounder
    -c CONFIG, --config CONFIG
                          Config for the processor.
    --format FORMAT, -j FORMAT
    -i [INFILE], --infile [INFILE]
                          Specifies the intput file. The default is stdin.
    -o [OUTFILE], --outfile [OUTFILE]
                          Specifies the output file. The default is stdout.


topo-viz
#########

::

  $ bin/topo-viz -h
  usage: topo-viz [-h] -v VIZMODEL [-c CONFIG] [--format FORMAT] [-i [INFILE]]
                  [-o [OUTFILE]]

  optional arguments:
    -h, --help            show this help message and exit
    -v VIZMODEL, --vizmodel VIZMODEL
                          Specifies the processor to use. Available :
                          timeseries, network
    -c CONFIG, --config CONFIG
                          Config for the processor.
    --format FORMAT, -j FORMAT
    -i [INFILE], --infile [INFILE]
                          Specifies the intput file. The default is stdin.
    -o [OUTFILE], --outfile [OUTFILE]
                          Specifies the output file. The default is stdout.


Bonus : use Topogram with Dat
=============

`Dat<http://dat-data.com/>` is a fine project of data versioning that may come in a handy when you are doing all your dirty work of parsing and formating. Here is a short tutorial for dat

Dat works pretty much like git. You init a rep, provide some basic information and add files to it.

::

  $ dat init
  name: (data) 7 seconds
  description: Gigs from 7 seconds between 2007 and 2015
  publisher: bandsintown.com
  Initialized dat store at .dat

  $ dat import 7_Seconds.json 
  Elapsed      : 0 s
  Parsed       : 63.82 kB  (63.82 kB/s)
   - changes : 1

  Done

Now we can stream each row of the json file using dat and pipe it directly into Topogram cli 


