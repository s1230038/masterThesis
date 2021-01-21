#!/bin/sh

for CSV in `ls *csv`
do
    tr -d \\r < $CSV > test.csv
    mv test.csv $CSV 
done
