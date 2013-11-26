#!/usr/bin/env python

# Makes a database for markovtwitter from a corpus file.
# The corpus file is expected to be one sentence per line.
#
# usage: make_db.py [-h] -c corpusfile -n depth -o outfile
import argparse
from markovchain import MarkovChain

parser = argparse.ArgumentParser()
parser.add_argument('-c', '--corpus',
                    help='Name of corpus file', required=True,
                    metavar='corpusfile')
parser.add_argument('-n', '--order', help='Chain depth', 
                    type=int, required=True, default=1, metavar='depth')
parser.add_argument('-o', '--out', help='Output DB filename',
                    required=True, metavar='outfile')
args = parser.parse_args()

print 'Generating markov chain database from %s' % args.corpus

mc = MarkovChain(corpusfile=args.corpus,order=args.order)
print mc

print 'Saving database to %s' % args.out
mc.save_db(args.out)

