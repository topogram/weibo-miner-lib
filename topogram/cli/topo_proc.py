#!/usr/bin/env python

import sys
import os
import argparse

import json
from bson import json_util

# mysterious bug from stack overflow http://newbebweb.blogspot.fr/2012/02/python-head-ioerror-errno-32-broken.html
from signal import signal, SIGPIPE, SIG_DFL
signal(SIGPIPE,SIG_DFL) 

from topogram.processors.time_rounder import TimeRounder
from topogram.processors.nlp import NLP

def parse_args():

    # parse command line arguments
    p = argparse.ArgumentParser()

    p.add_argument("-p", "--processor", help='Specifies the processor to use. Available : nlp, timerounder', required=True)
    p.add_argument("-c", "--config", help='Config for the processor.', required=True)
    p.add_argument('--format', '-j', default="json")

    # in/out format with default to stdin / stdout
    p.add_argument( '-i' ,'--infile', nargs='?', type=argparse.FileType('r'), default=sys.stdin, help='Specifies the intput file.  The default is stdin.')
    p.add_argument( "-o" ,'--outfile', nargs='?', type=argparse.FileType('w'), default=sys.stdout, help='Specifies the output file.  The default is stdout.')

    return p

def get_processor(args):

    if args.processor == "timerounder":
        proc = TimeRounder(args.config)
    elif args.processor == "nlp":
        proc = NLP(args.config)
    else :
        raise NotImplemented("This option doesn't exist")

    return proc

def map_input(proc, stdin):
    for line in stdin: 
        row = json.loads(line, object_hook=json_util.object_hook)
        result = proc.process_row(row)
        yield result

def map_output(row, stdout):
    """Dump json into the stream"""
    stdout.write( json.dumps(row, default=json_util.default)+ '\n' )

def main():

    p = parse_args()

    # get cli args
    args = p.parse_args(sys.argv[1:])

    proc = get_processor(args)

    # make sure everything is processed line by line
    for row in map_input(proc, args.infile):
        map_output(row, args.outfile)
