#!/bin/bash
trap "exit" INT

# single-task experiments
for e in {1..4}
do
    for t in {1..20}
    do
        echo "### Experiment ${e}, task ${t} ###"
        ./run-experiment.sh -t=${t} -e=${e} -r=10
    done
done

# joint-tasks experiments
for e in {5..9}
do
    echo "### Experiment ${e} ###"
    ./run-experiment.sh -e=${e} -r=10
done
