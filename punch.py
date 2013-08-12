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


def stop_all(clock):
    for task in clock.running_tasks():
        clock.punch(task[0])


CLOCK_FILE = "clock.dat"

clock = Clock(CLOCK_FILE)
manual_punch = None
should_switch = False

short_opts = "f:hm:s"
long_opts = ["file", "help", "manual=", "switch"]
commands = {"categories": "List categories in clock",
            "print": "Print time summary",
            "running": "List all running processes",
            "stop": "Stop all running processes",
            "total": "Print total time"}

try:
    (opts, args) = getopt(argv[1:], short_opts, long_opts)
except GetoptError as ge:
    from sys import stderr
    stderr.write("Error parsing arguments\n")
    raise ge


for (opt, optarg) in opts:
    while opt[0] == "-":
        opt = opt[1:]
    if opt in ["f", "file"]:
        clock = Clock(optarg)
    elif opt in ["h", "help"]:
        print("Command Summary:")
        for cmd in commands:
            print("{0}: {1}".format(cmd, commands[cmd]))
        print("")
        print("Command line arguments: {0}"
              .format(", ".join(sorted(long_opts))))
        exit(0)
    elif opt in ["m", "manual"]:
        manual_punch = int(optarg)
    elif opt in ["s", "switch"]:
        should_switch = True


if not args:
    display_times(clock)
    exit(0)


command = args[0]

if command == "categories":
    print(", ".join(sorted(clock.get_categories())))
elif command == "print":
    display_times(clock)
elif command == "running":
    now = get_timestamp()
    for task in clock.running_tasks():
        print("{0}: {1} seconds".format(task[0], now - task[1]))
elif command == "stop":
    stop_all(clock)
elif command == "total":
    times = sorted(clock.get_timestamps())
    print("Started on {0}".format(times[0]))
    print("Last punch on {0}".format(times[-1]))
    print("Total time span: {0} seconds".format(times[-1] - times[0]))
else:
    clock.punch(command, manual_punch)
