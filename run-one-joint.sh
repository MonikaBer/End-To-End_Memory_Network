#!/bin/bash

# ONLY FOR EXPERIMENTS 5-9 !

trap "exit" INT

for r in {1..10}
do
    echo "### Experiment ${1} ###"
    ./run-experiment.sh -e=${1}
done
