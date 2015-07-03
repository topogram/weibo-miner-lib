#!/usr/bin/env python

import sys
import argparse

import json
from bson import json_util

# mysterious bug from stack overflow http://newbebweb.blogspot.fr/2012/02/python-head-ioerror-errno-32-broken.html
from signal import signal, SIGPIPE, SIG_DFL
signal(SIGPIPE,SIG_DFL) 

from topogram.corpus import Corpus

def parse_args():
    # parse command line arguments
    p = argparse.ArgumentParser()

    p.add_argument('--timestamp', '-t', default="created_at", required=False)
    p.add_argument('--time-pattern', '-p', default=None)
    p.add_argument('--origin', '-r', default="user_id")
    p.add_argument('--content', '-c', default="text", required=True)
    p.add_argument('--exclude', '-e', default="ObjectId")
    p.add_argument('--format', '-j', default="json")
    p.add_argument('--longitude', '-L', default="0")
    p.add_argument('--latitude', '-l', default="0")
    p.add_argument('--additional', '-a', default="0")



    # in/out format with default to stdin / stdout
    p.add_argument('infile', nargs='?', type=argparse.FileType('r'), default=sys.stdin, help='Specifies the intput file.  The default is stdin.')
    p.add_argument('outfile', nargs='?', type=argparse.FileType('w'), default=sys.stdout, help='Specifies the output file.  The default is stdout.')

    return p

def get_corpus(args):
    # parse corpus  
    corpus = Corpus(
                    args.format,
                    content=args.content,
                    origin=args.origin,
                    timestamp=args.timestamp,
                    time_pattern=args.time_pattern,
                    longitude=args.longitude,
                    latitude=args.latitude,
                    adds=args.additional
                )
    return corpus

def map_input(corpus, stdin):
    for line in stdin:
            yield corpus(line)

def map_output(row, stdout):
    """Dump json into the stream"""
    stdout.write( json.dumps(row, default=json_util.default)+ '\n' )

def main():

    # load parser
    parser = parse_args()

    # get cli args
    args = parser.parse_args(sys.argv[1:])

    # parse corpus
    corpus = get_corpus(args)

    # make sure everything is processed line by line
    for row in map_input(corpus, args.infile):
        map_output(row, args.outfile)
