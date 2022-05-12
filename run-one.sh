#!/bin/bash
trap "exit" INT

for r in {1..10}
do
    for t in {1..20}
    do
        echo "### Experiment ${1}, task ${t} ###"
        ./run-experiment.sh -t=${t} -e=${1}
    done
done
    