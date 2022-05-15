#!/bin/bash
# Run one specific single-task experiment

# ONLY FOR EXPERIMENTS 1-4 !

trap "exit" INT

for r in {1..10}
do
    for t in {1..20}
    do
        echo "### Experiment ${1}, task ${t} ###"
        ./run-experiment.sh -t=${t} -e=${1}
    done
done
