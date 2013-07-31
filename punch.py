#!/usr/bin/env python

from os.path import isfile
from sys import argv
from clock import Clock, get_timestamp
from getopt import getopt, GetoptError

CLOCK_FILE = "clock.dat"

clock = Clock(CLOCK_FILE)

(opts, args) = getopt(argv[1:], "prs", ["print", "running", "switch"])


for (opt, optarg) in opts:
    while opt[0] == "-":
        opt = opt[1:]
    if opt in ["p", "print"]:
        clock.print_times()
        exit(0)
    elif opt in ["r", "running"]:
        now = get_timestamp()
        for task in clock.running_tasks():
            print("{0}: {1} seconds".format(task[0], now - task[1]))
        exit(0)
    elif opt in ["s", "switch"]:
        for task in clock.running_tasks():
            clock.punch(task)
            
category = args[0]

clock.punch(category)
