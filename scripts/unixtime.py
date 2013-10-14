#!/usr/bin/env python

from sys import argv
from time import mktime
from datetime import datetime, date

if "-h" in " ".join(argv):
    print("Usage: unixtime.py [YYYYmmdd] HH:MM")
    exit(0)

fmt = "%Y%m%d %H:%M"
if len(argv) < 3:
    time_str = " ".join([date.today().strftime("%Y%m%d"), argv[1]])
else:
    time_str = " ".join(argv[1:])

unixtime = mktime(datetime.strptime(time_str, fmt).timetuple())

print(int(unixtime))
