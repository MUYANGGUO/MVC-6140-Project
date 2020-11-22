#!/bin/sh
echo "performing experiments in a grid search fashion ... \n"
datafiles=`ls ./DATA/*.graph`
for datafile in $datafiles
do
    for CUTTIME in 10.0 50.0 250.0 500.0
    do
        python MVC.py $datafile Approx $CUTTIME 1
    done
done
