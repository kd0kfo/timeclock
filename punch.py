#!/usr/bin/env python

from os.path import isfile
from sys import argv
from clock import Clock, get_timestamp
from getopt import getopt, GetoptError


def display_times(_clock):
    _clock.print_times(alphabetic=True)
    total_time = _clock.total_time()
    print("---")
    print("Total counted time: {0} seconds ({1:.2f} hrs)"
          .format(total_time, total_time/3600.))


CLOCK_FILE = "clock.dat"

clock = Clock(CLOCK_FILE)

short_opts = "hcprst"
long_opts = ["categories", "help", "print", "running", "stop", "switch", "total"]
try:
    (opts, args) = getopt(argv[1:], short_opts, long_opts)
except GetoptError as ge:
    from sys import stderr
    stderr.write("Error parsing arguments\n")
    raise ge


for (opt, optarg) in opts:
    while opt[0] == "-":
        opt = opt[1:]
    if opt in ["c", "categories"]:
        print(", ".join(sorted(clock.get_categories())))
        exit(0)
    elif opt in ["h", "help"]:
        print("Command line arguments: {0}"
              .format(", ".join(sorted(long_opts))))
        exit(0)
    elif opt in ["p", "print"]:
        display_times(clock)
        exit(0)
    elif opt in ["r", "running"]:
        now = get_timestamp()
        for task in clock.running_tasks():
            print("{0}: {1} seconds".format(task[0], now - task[1]))
        exit(0)
    elif opt in ["s", "switch", "stop"]:
        for task in clock.running_tasks():
            clock.punch(task[0])
        if opt == "stop":
            exit(0)
    elif opt in ["t", "total"]:
        times = sorted(clock.get_timestamps())
        print("Started on {0}".format(times[0]))
        print("Last punch on {0}".format(times[-1]))
        print("Total time span: {0} seconds".format(times[-1] - times[0]))
        exit(0)

if not args:
    display_times(clock)
    exit(0)

category = args[0]

clock.punch(category)
