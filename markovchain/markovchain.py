#!/usr/bin/env python
from __future__ import division
import random
from itertools import izip
try:
    import cPickle as pickle
except ImportError:
    import pickle


def sliding_window(iterable, size):
    """
    Splits a non-generator iterable into overlapping groups of size size
    In [126]: [x for x in sliding_window(range(5),2)]
    Out[126]: [[0, 1], [1, 2], [2, 3], [3, 4], [4]]
    """
    for i,x in enumerate(iterable):
        yield iterable[i:(i+size)]


def table(seq):
    """
    For each unique value in seq, runs count() on it. Returns a dictionary in
    the form of {value1: count, value2: count}.
    """
    seq = [x for x in seq]
    keys = set(seq)
    return dict([(k, seq.count(k)) for k in keys])

def icumsum(l):
    """ Lazily yields the cumulative sum of an iterable """
    z = 0
    for x in l:
        z += x
        yield z


def choice_with_probs(choices, probs):
    """ Randomly chooses items from a list with weights """
    r = random.random() * sum(probs)
    for choice, cumulative_prob in izip(choices, icumsum(probs)):
        if r < cumulative_prob:
            return choice

class MarkovChain(object):
    """ A Markov Chain for generating text from small phrases """ 

    def __init__(self, order=1, corpusfile=None, saveddb=None):
        # The size of the window used for picking the next word
        self.order = order
        # A dictionary relating a word or phrase to the words 
        # that follow it
        self.corpus = {}
        # A set of starting phrases 
        self.starts = set()
        if corpusfile:
            self.make_corpus(corpusfile)
        if saveddb:
            self.load_db(saveddb)

    def __repr__(self):
        return '%s-order Markov chain' % self.order

    def random_title(self):
        """ Generates a random title """
        # Randomly chooses a starting phrase
        sentence = self._random_start()
        while True:
            nextword = self._nextword(sentence[-self.order:])
            # None is the sentence terminator
            if nextword is None:
                break
            else:
                sentence.append(nextword)
        return ' '.join(sentence)

    def _random_start(self):
        return list(random.sample(self.starts,1)[0])

    def _nextword(self, prefix):
        """ Picks the next word in the Markov Chain """
        prefix = tuple(x.lower() for x in prefix)
        choices, probs = zip(*[(k,v) for k,v in 
                               self.db[prefix].iteritems()])
        return choice_with_probs(choices, probs)

    def make_db(self, corpusfile):
        """ Generates the data from a corpus file """
        size = self.order
        with open(corpusfile) as corpusf:
             for title in corpusf:
                # Strip the newline and split into a list
                title = title.strip().split()
                title_length = len(title)
                # Optimization:
                #
                # A title less than 6 words is probably not going to be useful:
                # Sometimes it's what seems to be heading titles, but either 
                # way it's not good for generating long strings of text
                if title_length < 6:
                    continue
                # Add the starting word(s) to the starter db.
                # Lists are mutable and can't be used in sets or as 
                # dictionary keys, so we'll have to change to tuples
                # From here on out.
                self.starts.add(tuple(title[0:size])) 
                for i, window in enumerate(sliding_window(title,size)):
                    # Optimization:
                    # Dictionary keys are case-sensitive and can reduce 
                    # the diversity of generated text. We don't actually
                    # use the keys here, so we can perform any number of
                    # transformations on them.
                    window = tuple(x.lower() for x in window)
                    # Test to make sure we aren't over shooting the end 
                    #  of the list
                    if i+size > title_length:
                        break
                    # Check if this phrase is in the corpus
                    if window not in self.db:
                        self.db[window] = []
                    # This is the end of a sentence and will terminate
                    # a randomly generated sentence.
                    if i+size == title_length:
                        self.db[window].append(None)
                    # The word that follows the window
                    else:
                        self.db[window].append(title[i+size])
        # Optimization:
        # Normalize the corpus. By picking choices with probabilities,
        # You don't have to store repeated elements within the corpus
        for key in self.db:
            nchoices = len(self.db[key])
            t = table(self.db[key])
            # Dictionary comprehension requires python 2.7
            self.db[key] = {choice: weight/nchoices for 
                                choice, weight in t.iteritems()}

    def load_db(self, filename):
        """ Loads a saved database """
        with open(filename) as inf:
            order, db = pickle.load(inf) 
            self.order = order
            self.db = db

    def save_db(self, filename):
        """ Reads a saved database """
        data = (self.order, self.db)
        with open(filename, 'w') as outf:
            pickle.dump(data,outf)


