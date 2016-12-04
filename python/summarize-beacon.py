#!/usr/bin/env python3

"""
Test assignment of mine.

Without additional arguments, it retrieves the most recent event
from the randomness beacon, and counts the number of characters
in the OutputValue the beacon returns. Then it prints that
output to standard out in comma-delimited format.

./summarize-beacon.py

0,2
1,1
4,1
A,1
F,2

When given optional --from and --to arguments, the script output
the character count over a span of beacon values using relative time.
For example, if we provided the script the following arguments:

./summarize-beacon.py --from "3 months 1 day 1 hour ago" --to "1 month 1 hour ago"

2,2
A,2
...
B,2
F,1

Script summarizes beacons found via REST API.
Details https://beacon.nist.gov/home
        https://www.nist.gov/programs-projects/nist-randomness-beacon
"""

import requests
import time
import dateparser
import xmltodict
import argparse
import sys


parser = argparse.ArgumentParser(add_help=True)

parser.add_argument('--from', action="store", dest="from_time")
parser.add_argument('--to', action="store", dest="to_time")

args = parser.parse_args()

from_time_rel = args.from_time
to_time_rel = args.to_time


def get_outputValue(api_var):
    link = 'https://beacon.nist.gov/rest/record/{}'.format(api_var)
    resp = requests.get(link)
    doc = xmltodict.parse(resp.content)
    outputValue = doc['record']['outputValue']
    return outputValue

def create_output(line):
    # create dic with each letter as a key and amount of it as a variable
    dict = {x:line.count(x) for x in line}
    for key, value in dict.items():
        print("{},{}".format(key, value))

def get_unix_time_minute_accuracy(relative_time):
    unix_time = dateparser.parse(relative_time).timestamp()
    unix_time_minutes_accuracy = int(unix_time // 60 * 60)
    return unix_time_minutes_accuracy

def main():

    if len(sys.argv) > 1:

        outputValuesList = ''
        from_time = get_unix_time_minute_accuracy(from_time_rel)
        to_time = get_unix_time_minute_accuracy(to_time_rel)

        if from_time > to_time:
            print("You have entered wrong time range.")

        for unix_time in range(from_time, to_time+60, 60):
            outputValue = get_outputValue(unix_time)
            outputValuesList = outputValuesList + outputValue

        create_output(outputValuesList)

    else:
        outputValue = get_outputValue('last')
        create_output(outputValue)


if __name__ == "__main__":
    main()
