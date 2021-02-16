#!/bin/sh

# $ ./getTaggedFiles.sh GIT_TAG
# $ ./getTaggedFiles.sh 1st_thesis

mkdir $1
for TEX in `ls *.tex`
do
    git show $1:./$TEX > ./$1/$TEX
done