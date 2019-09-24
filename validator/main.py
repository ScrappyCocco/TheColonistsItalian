#!/usr/bin/env python3

import sys

from CSVValidator import CSVValidator

print("Starting script...")

if len(sys.argv) > 2:
    print("Passed more than 1 arguments! You must pass only the filename! "
          "(if necessary pass it as \"filename\" with quotes")
elif len(sys.argv) == 2:
    if sys.argv[1].endswith(".csv"):
        validator = CSVValidator()
        validator.process_file(sys.argv[1])
    else:
        print("You passed a filename without the .csv extension!")
else:
    print("Passed 0 arguments! You must pass the filename!")

print("Script end...")
