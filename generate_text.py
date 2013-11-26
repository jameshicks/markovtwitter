#!/usr/bin/env python

import argparse
from markovchain import MarkovChain

parser = argparse.ArgumentParser()
parser.add_argument('-d', '--db', help='Filename of saved database',
                    metavar='database', required=True)
parser.add_argument('-n', '--number', type=int, default=10,
                    help='Number of lines to generate', metavar='numlines')
args = parser.parse_args()

mc = MarkovChain(saveddb=args.db)
for i in xrange(args.number):
    print mc.random_title()
