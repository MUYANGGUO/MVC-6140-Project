#!/bin/sh
echo "performing experiments in a grid search fashion ... \n"
datafiles=`ls ./DATA/*.graph`
for datafile in $datafiles
do
    for CUTTIME in 10.0 50.0 100.0 500.0 1000.0
    do
        python3 MVC.py $datafile LS2 $CUTTIME 1
    done
done
