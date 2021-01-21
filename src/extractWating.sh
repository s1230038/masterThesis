#!/bin/sh

OUTPUT=./analysis/wating_rate.csv
rm $OUTPUT
touch $OUTPUT

declare -i i=0
declare -i j=1
declare -i k=0
declare -i WAIT_NUM=0
declare -i SUM_ACT=0

for DIR in `ls -d ./result_MA*`
do
    MA=`echo $DIR | awk -F/ '{print $2}' | awk -F_ '{print $2}'`

    for CSV in `ls $DIR/log_per_step_*.csv | sort -n`
    do
        KIND=`echo $CSV | awk -F_ '{print $5}'`
        EP=`echo $CSV | awk -F_ '{print $6}' | awk -F. '{print $1}' | sed -e 's/ep//'`
        WAIT_NUM=`awk -F, -f wating.awk $CSV | wc -l`
        SUM_ACT=`cat $CSV | wc -l`
        SUM_ACT=$SUM_ACT-1
        eval WATI_RATE=`awk "BEGIN { print $WAIT_NUM/$SUM_ACT}"`
        echo ${MA}, ${KIND}, ${EP}, ${WATI_RATE} >> $OUTPUT
    done
done

sort -t, -k 1,1 -k 3n $OUTPUT > tmp.csv
mv tmp.csv $OUTPUT

