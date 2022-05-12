#!/bin/bash
trap "exit" INT

for t in {1..20}
do
    echo "### Experiment ${1}, task ${t} ###"
    ./run-experiment.sh -t=${t} -e=${1} -r=10
done

  