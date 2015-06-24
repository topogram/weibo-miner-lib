#!/usr/bin/env python

import sys
import os
import argparse

import json
from bson import json_util

from topogram.corpus import Corpus

from topogram.processors.time_rounder import TimeRounder
from topogram.processors.nlp import NLP

from topogram.vizparsers.time_series import TimeSeries
from topogram.vizparsers.network import Network

# mysterious bug from stack overflow http://newbebweb.blogspot.fr/2012/02/python-head-ioerror-errno-32-broken.html
from signal import signal, SIGPIPE, SIG_DFL
signal(SIGPIPE,SIG_DFL) 

def topo_corpus():

    # parse command line arguments
    p = argparse.ArgumentParser()

    p.add_argument('--timestamp', '-t', default="created_at", required=True)
    p.add_argument('--time-pattern', '-p', default=None)
    p.add_argument('--origin', '-r', default="user_id")
    p.add_argument('--content', '-c', default="text", required=True)
    p.add_argument('--exclude', '-e', default="ObjectId")
    p.add_argument('--format', '-j', default="json")

    # in/out format with default to stdin / stdout
    p.add_argument('infile', nargs='?', type=argparse.FileType('r'), default=sys.stdin, help='Specifies the intput file.  The default is stdin.')
    p.add_argument('outfile', nargs='?', type=argparse.FileType('w'), default=sys.stdout, help='Specifies the output file.  The default is stdout.')

    # get cli args
    args = p.parse_args(sys.argv[1:])
    # print args

    # parse corpus  
    corpus = Corpus(
                    args.format,
                    content=args.content,
                    origin=args.origin,
                    timestamp=args.timestamp,
                    time_pattern=args.time_pattern
                )

    # make sure everything is processed line by line
    if args.infile is sys.stdin : 
        for line in sys.stdin:
            row = corpus(line)
            if args.outfile is sys.stdout : 
                sys.stdout.write(json.dumps(row, default=json_util.default)+ '\n' )

def topo_proc():

    # parse command line arguments
    p = argparse.ArgumentParser()

    p.add_argument("-p", "--processor", help='Specifies the processor to use. Available : nlp, timerounder', required=True)
    p.add_argument("-c", "--config", help='Config for the processor.', required=True)
    p.add_argument('--format', '-j', default="json")

    # in/out format with default to stdin / stdout
    p.add_argument( '-i' ,'--infile', nargs='?', type=argparse.FileType('r'), default=sys.stdin, help='Specifies the intput file.  The default is stdin.')
    p.add_argument( "-o" ,'--outfile', nargs='?', type=argparse.FileType('w'), default=sys.stdout, help='Specifies the output file.  The default is stdout.')

    # get cli args
    args = p.parse_args(sys.argv[1:])
    
    if args.processor == "timerounder":
        proc = TimeRounder(args.config)
    elif args.processor == "nlp":
        proc = NLP(args.config)
    else :
        raise NotImplemented("This option doesn't exist")
    
    # make sure everything is processed line by line
    if args.infile is sys.stdin : 
        for line in sys.stdin: 
            if args.format == "json":
                row = json.loads(line, object_hook=json_util.object_hook)
                result = proc.process_row(row)

                if args.outfile is sys.stdout : 
                    sys.stdout.write(json.dumps(result, default=json_util.default)+ '\n' )

def topo_viz():
    # if __name__ == "__main__":

    # parse command line arguments
    p = argparse.ArgumentParser()

    p.add_argument("-v", "--vizmodel", help='Specifies the processor to use. Available : timeseries, network', required=True)
    p.add_argument("-c", "--config", help='Config for the processor.',default="minute")
    p.add_argument('--format', '-j', default="json")

    # in/out format with default to stdin / stdout
    p.add_argument( '-i' ,'--infile', nargs='?', type=argparse.FileType('r'), default=sys.stdin, help='Specifies the intput file.  The default is stdin.')
    p.add_argument( "-o" ,'--outfile', nargs='?', type=argparse.FileType('w'), default=sys.stdout, help='Specifies the output file.  The default is stdout.')

    # get cli args
    args = p.parse_args(sys.argv[1:])
    
    if args.vizmodel == "timeseries":
        viz = TimeSeries(timescale=args.config)
    elif args.vizmodel == "network":
        viz = Network(args.config)
    else :
        raise NotImplemented("This option doesn't exist")

    # make sure everything is processed line by line
    if args.infile is sys.stdin :
        for line in sys.stdin: 
            if args.format == "json":
                row = json.loads(line, object_hook=json_util.object_hook)
                viz(row)
    if args.outfile is sys.stdout : 
        sys.stdout.write( json.dumps(viz.to_JSON()) ) 
    else :
        json.dump(viz.to_JSON(), args.outfile )

