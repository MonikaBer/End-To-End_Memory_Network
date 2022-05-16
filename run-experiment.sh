#!/bin/bash

programname=$0
function usage {
    echo "usage: $programname [-e=experiment] [-t=task] [-r=repeat]"
    echo "  -e, --experiment        Number of experiment, 1..10"
    echo "  -t, --task              Number of task, 1..20"
    echo "  -d, --dataset           Dataset type (1 - for 1k, 10 - for 10k)"
    echo "  -r, --repeat            Repeat this many times"
    exit 1
}

trap exit SIGINT

for i in "$@"
do
case $i in
    -e=*|--experiment=*)
    EXPERIMENT="${i#*=}"
    ;;
    -t=*|--task=*)
    TASK="${i#*=}"
    ;;
    -d=*|--dataset=*)
    DATASET="${i#*=}"
    ;;
    -r=*|--repeat=*)
    TIMES="${i#*=}"
    ;;
    *)
    usage        # unknown option
    ;;
esac
done

if [ -z "$EXPERIMENT" ]
then
    usage
fi

if [ -z "$TASK" ] && [[ $EXPERIMENT -le 4 || $EXPERIMENT -ge 10 ]]
then
    usage
fi

if [ -z "$DATASET" ]
then
    usage
fi

if [ -z "$TIMES" ]
then
    TIMES=1
fi


# check if experiment nr is not 10 for dataset 1k
if [[ $EXPERIMENT -eq 10 && $DATASET -eq 1 ]]; then
    echo "Additional 10. experiment is only for 10k dataset!"
    exit 1
fi

# check if task nr is specified for joint experiment
if [[ $EXPERIMENT -ge 5 && $EXPERIMENT -le 9 ]] && [[ $TASK -ge 1 && $TASK -le 20 ]]; then
    echo "Task specified for joint training - it is not acceptable!"
    exit 1
fi


DATA_DIR=""
if [ ${DATASET} -eq 1 ]; then
    DATA_DIR="data/tasks_1-20_v1-2/en"
elif [ ${DATASET} -eq 10 ]; then
    DATA_DIR="data/tasks_1-20_v1-2/en-10k"
else
    echo "Unknown dataset type"
    usage
fi


for i in $( eval echo {1..${TIMES}} )
do
    echo "Repeat nr: $i"

    if [ ${EXPERIMENT} -eq 1 ]; then
        #BoW
        RES=$( python2.7 babi_runner.py --data-dir $DATA_DIR -t $TASK --BoW --save-results --results-path "results/results_${DATASET}k_1.csv" | tee /dev/stderr )
    elif [ ${EXPERIMENT} -eq 2 ]; then
        #PE
        RES=$( python2.7 babi_runner.py --data-dir $DATA_DIR -t $TASK --save-results --results-path "results/results_${DATASET}k_2.csv" | tee /dev/stderr )
    elif [ ${EXPERIMENT} -eq 3 ]; then
        # PE + LS
        RES=$( python2.7 babi_runner.py --data-dir $DATA_DIR -t $TASK --LS --save-results --results-path "results/results_${DATASET}k_3.csv" | tee /dev/stderr )
    elif [ ${EXPERIMENT} -eq 4 ]; then
        # PE + LS + RN
        RES=$( python2.7 babi_runner.py --data-dir $DATA_DIR -t $TASK --LS --RN --save-results --results-path "results/results_${DATASET}k_4.csv" | tee /dev/stderr )
    elif [ ${EXPERIMENT} -eq 5 ]; then
        # 1 hop + PE + LS + joint
        RES=$( python2.7 babi_runner.py --data-dir $DATA_DIR --LS --hops 1 -j --save-results --results-path "results/results_${DATASET}k_5.csv" | tee /dev/stderr )
    elif [ ${EXPERIMENT} -eq 6 ]; then
        # 2 hop + PE + LS + joint
        RES=$( python2.7 babi_runner.py --data-dir $DATA_DIR --LS --hops 2 -j --save-results --results-path "results/results_${DATASET}k_6.csv" | tee /dev/stderr )
    elif [ ${EXPERIMENT} -eq 7 ]; then
        # 3 hop + PE + LS + joint
        RES=$( python2.7 babi_runner.py --data-dir $DATA_DIR --LS --hops 3 -j --save-results --results-path "results/results_${DATASET}k_7.csv" | tee /dev/stderr )
    elif [ ${EXPERIMENT} -eq 8 ]; then
        # PE + LS + RN + joint
        RES=$( python2.7 babi_runner.py --data-dir $DATA_DIR --LS -j --RN --save-results --results-path "results/results_${DATASET}k_8.csv" | tee /dev/stderr )
    elif [ ${EXPERIMENT} -eq 9 ]; then
        # PE + LS + LW + joint
        RES=$( python2.7 babi_runner.py --data-dir $DATA_DIR --LS -j --LW --save-results --results-path "results/results_${DATASET}k_9.csv" | tee /dev/stderr )
    elif [ ${EXPERIMENT} -eq 10 ]; then
        # PE + LS + LW + RN + NL
        RES=$( python2.7 babi_runner.py --data-dir $DATA_DIR --LS -t $TASK --LW --RN --NL --embed-dim 100 --save-results --results-path "results/results_${DATASET}k_10.csv" | tee /dev/stderr )
    else
        echo "Unknown experiment"
    fi
done
