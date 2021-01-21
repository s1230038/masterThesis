#!/bin/sh

for CSV in `ls *csv`
do
    cat $CSV | awk -F, '$6 != "0"' > test.csv
    mv test.csv $CSV 
done
