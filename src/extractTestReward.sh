#!/bin/sh

grep "Episode 1: reward: " ./result_MA*/output.txt | awk '{print $4}' > ./analysis/rewardVStest.csv

