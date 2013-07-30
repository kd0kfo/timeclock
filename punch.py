#!/usr/bin/env python

from os.path import isfile
from sys import argv


def get_timestamp():
    import time
    return int(time.time())


def load_file(filename):
    cats = {}
    with open(filename, "r") as infile:
        for line in infile:
            tokens = line.split()
            if len(tokens) != 2:
                raise Exception("Broken line: {0}".format(line))
            cat = tokens[0]
            timestamp = int(tokens[1])
            if not tokens[0] in cats:
                cats[cat] = [timestamp]
            else:
                cats[cat].append(timestamp)
    return cats

def print_times(cats):
    for cat in cats:
        punches = cats[cat]
        total_time = 0
        length = len(punches)
        if length  % 2 != 0:
            length -= 1
        idx = 0
        while idx < length:
            start = punches[idx]
            stop = punches[idx + 1]
            total_time += stop - start
            idx += 2
            
        if len(punches) % 2 != 0:
            total_time += get_timestamp() - punches[-1]
            suffix = "+ seconds"
        else:
            suffix = " seconds"
        print("{0}: {1}{2}".format(cat, total_time, suffix))


CLOCK_FILE = "clock.dat"

category = argv[1]

if argv[1] == "--print":
    categories = load_file(CLOCK_FILE)
    print_times(categories)
    exit(0)

with open(CLOCK_FILE, "a") as outfile:
    outfile.write("{0}\t{1}\n".format(category, get_timestamp()))
