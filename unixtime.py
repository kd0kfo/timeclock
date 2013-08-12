#!/usr/bin/env python

from sys import argv
from time import mktime
from datetime import datetime

time_str = " ".join(argv[1:])

fmt = "%Y%m%d"
if len(argv) > 2:
    fmt += " %H:%M"

unixtime = mktime(datetime.strptime(time_str, fmt).timetuple())

print(int(unixtime))
