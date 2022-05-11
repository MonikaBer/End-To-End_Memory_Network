#!/bin/bash
trap "exit" INT

for e in {1..9} 
do
    for t in {1..20}
    do
        echo "### Experiment ${e}, task ${t} ###"
        ./run-experiment.sh -t=${t} -e=${e} -r=10
    done
done

  