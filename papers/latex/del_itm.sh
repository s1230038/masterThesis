#!/bin/sh

for INTERMEDIATE in `cat .gitignore`
do
    rm $INTERMEDIATE
done
