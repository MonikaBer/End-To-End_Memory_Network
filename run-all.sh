#!/bin/bash
# Run all experiments on specific dataset (1k / 10k)

# $1 - {1, 10}

programname=$0
function usage {
    echo "usage: $programname [dataset_type]"
    echo "  dataset_type        Dataset type, {1, 10}"
    exit 1
}

trap "exit" INT

# check dataset type
if [ ${1} -eq 1 ]; then
    RUN_EXP_10=0
elif [ ${1} -eq 10 ]; then
    RUN_EXP_10=1
else
    echo "Wrong dataset type: ${1}!"
    usage
fi


echo "### RUN ALL EXPERIMENTS ON DATASET: ${1} ###"

# single-task experiments
for e in {1..4}
do
    for t in {1..20}
    do
        echo "### Experiment ${e}, task ${t} ###"
        ./run-experiment.sh -t=${t} -e=${e} -d=${1} -r=10
    done
done

# joint-tasks experiments
for e in {5..9}
do
    echo "### Experiment ${e}  ###"
    ./run-experiment.sh -e=${e} -d=${1} -r=10
done

# additional experiment (only for 10k dataset)
if [ ${RUN_EXP_10} -eq 1 ]; then
    echo "### ADDITIONAL EXPERIMENT 10  ###"
    for t in {1..20}
    do
        echo "### Experiment 10, task ${t} ###"
        ./run-experiment.sh -t=${t} -e=10 -d=${1} -r=10
    done
fi
