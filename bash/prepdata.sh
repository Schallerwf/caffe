#!/bin/bash

# Takes in a csv dataset.
# Balances the classes.
# Randomly shuffles data.
# Splits data into 4 files.
# Converts files to hdf5.

# usage: ./prepdata.sh <csv> <truth-label>

python ../python/balanceData.py $1 --label $2 > "$1-b"
(head -n 1 "$1-b" && tail -n +2 "$1-b" | shuf) > "$1-bs"
python ../python/csvToHdf5.py "$1-bs" --label $2


