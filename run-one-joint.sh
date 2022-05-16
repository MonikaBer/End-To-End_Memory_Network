#!/bin/bash
# Run one specific joint-task experiment on specific dataset (1k / 10k)

# ONLY FOR EXPERIMENTS 5-9 !

# $1 - {5..9}
# $2 - {1, 10}

programname=$0
function usage {
    echo "usage: $programname [exp_nr] [dataset_type]"
    echo "  exp_nr              Experiment nr, {5..9}"
    echo "  dataset_type        Dataset type, {1, 10}"
    exit 1
}

trap "exit" INT

# check experiment number
if [[ ${1} -le 4 || ${1} -ge 10 ]]; then
    echo "Wrong experiment number!"
    usage
fi

# check dataset type
if [[ ${2} -ne 1 && ${2} -ne 10 ]]; then
    echo "Wrong dataset type!"
    usage
fi


echo "### RUN JOINT EXPERIMENT ${1} ON DATASET ${2} ###"

for r in {1..10}
do
    echo "### Experiment ${1} ###"
    ./run-experiment.sh -e=${1} -d=${2}
done
