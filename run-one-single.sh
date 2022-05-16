#!/bin/bash
# Run one specific single-task experiment on specific dataset (1k / 10k)

# ONLY FOR EXPERIMENTS 1-4, 10 !

# $1 - {1..4, 10}
# $2 - {1, 10}

programname=$0
function usage {
    echo "usage: $programname [exp_nr] [dataset_type]"
    echo "  exp_nr              Experiment nr, {1..4, 10}"
    echo "  dataset_type        Dataset type, {1, 10}"
    exit 1
}

trap "exit" INT

# check experiment number
if [[ ${1} -ge 5 && ${1} -le 9 ]]; then
    echo "Wrong experiment number!"
    usage
fi

# check dataset type
if [[ ${2} -ne 1 && ${2} -ne 10 ]]; then
    echo "Wrong dataset type!"
    usage
fi

# check if experiment nr is not 10 for dataset 1k
if [[ ${1} -eq 10 && ${2} -eq 1 ]]; then
    echo "Additional 10. experiment is only for 10k dataset!"
    exit 1
fi


echo "### RUN SINGLE EXPERIMENT ${1} ON DATASET ${2} ###"

for r in {1..10}
do
    for t in {1..20}
    do
        echo "### Experiment ${1}, task ${t} ###"
        ./run-experiment.sh -t=${t} -e=${1} -d=${2}
    done
done
