#!/usr/bin/env python

import sys
import os
import argparse

import json
from bson import json_util

# mysterious bug from stack overflow http://newbebweb.blogspot.fr/2012/02/python-head-ioerror-errno-32-broken.html
from signal import signal, SIGPIPE, SIG_DFL
signal(SIGPIPE,SIG_DFL) 

from topogram.vizparsers.time_series import TimeSeries
from topogram.vizparsers.network import Network
from topogram.vizparsers.map_point import MapPoint


def parse_args():
    # parse command line arguments
    p = argparse.ArgumentParser()

    p.add_argument("-v", "--vizmodel", help='Specifies the processor to use. Available : timeseries, network', required=True)
    p.add_argument("-c", "--config", help='Config for the processor.',default="minute")
    p.add_argument("-r", "--content", help='Add content.', default=None)
    p.add_argument('--format', '-j', default="json")

    # in/out format with default to stdin / stdout
    p.add_argument( '-i' ,'--infile', nargs='?', type=argparse.FileType('r'), default=sys.stdin, help='Specifies the intput file.  The default is stdin.')
    p.add_argument( "-o" ,'--outfile', nargs='?', type=argparse.FileType('w'), default=sys.stdout, help='Specifies the output file.  The default is stdout.')

    return p

def get_viz(args):
    if args.vizmodel == "timeseries":
        viz = TimeSeries(timescale=args.config)
    elif args.vizmodel == "network":
        viz = Network(args.config)
    elif args.vizmodel == "MapPoint":
        viz = MapPoint(content=args.content)

    else :
        raise NotImplemented("This option doesn't exist")
    return viz

def map_input(viz, stdin):
    for line in stdin:
        row = json.loads(line, object_hook=json_util.object_hook)
        viz(row)
    return viz

def main():

    p = parse_args()

    # get cli args
    args = p.parse_args(sys.argv[1:])
    
    viz = get_viz(args)

    # make sure everything is processed line by line
    viz = map_input(viz, args.infile)

    if args.outfile is sys.stdout : 
        sys.stdout.write( json.dumps(viz.to_JSON()) ) 
    else :
        json.dump(viz.to_JSON(), args.outfile )


