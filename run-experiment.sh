#!/bin/bash

programname=$0
function usage {
    echo "usage: $programname [-e=experiment] [-t=task] [-r=repeat]"
    echo "  -e, --experiment        Number of experiment, 1..9"
    echo "  -t, --task              Number of task, 1..20"
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

if [ -z "$TASK" ] && [ $EXPERIMENT -le 4 ]
then
    usage
fi

if [ -z "$TIMES" ]
then
    TIMES=1
fi

for i in $( eval echo {1..${TIMES}} )
do
    echo "Repeat nr: $i"

    if [ ${EXPERIMENT} -eq 1 ]; then
        #BoW
        RES=$( python2.7 babi_runner.py -t $TASK --BoW --save-results --results-path 'results/results_1.csv' | tee /dev/stderr )
    elif [ ${EXPERIMENT} -eq 2 ]; then
        #PE
        RES=$( python2.7 babi_runner.py -t $TASK --save-results --results-path 'results/results_2.csv' | tee /dev/stderr )
    elif [ ${EXPERIMENT} -eq 3 ]; then
        # PE + LS
        RES=$( python2.7 babi_runner.py -t $TASK --LS --save-results --results-path 'results/results_3.csv' | tee /dev/stderr )
    elif [ ${EXPERIMENT} -eq 4 ]; then
        # PE + LS + RN
        RES=$( python2.7 babi_runner.py -t $TASK --LS --RN --save-results --results-path 'results/results_4.csv' | tee /dev/stderr )
    elif [ ${EXPERIMENT} -eq 5 ]; then
        # 1 hop + PE + LS + joint
        RES=$( python2.7 babi_runner.py --LS --hops 1 -j --save-results --results-path 'results/results_5.csv' | tee /dev/stderr )
    elif [ ${EXPERIMENT} -eq 6 ]; then
        # 2 hop + PE + LS + joint
        RES=$( python2.7 babi_runner.py --LS --hops 2 -j --save-results --results-path 'results/results_6.csv' | tee /dev/stderr )
    elif [ ${EXPERIMENT} -eq 7 ]; then
        # 3 hop + PE + LS + joint
        RES=$( python2.7 babi_runner.py --LS --hops 3 -j --save-results --results-path 'results/results_7.csv' | tee /dev/stderr )
    elif [ ${EXPERIMENT} -eq 8 ]; then
        # PE + LS + RN + joint
        RES=$( python2.7 babi_runner.py --LS -j --RN --save-results --results-path 'results/results_8.csv' | tee /dev/stderr )
    elif [ ${EXPERIMENT} -eq 9 ]; then
        # PE + LS + LW + joint
        RES=$( python2.7 babi_runner.py --LS -j --LW --save-results --results-path 'results/results_9.csv' | tee /dev/stderr )
    else
        echo "Unknown experiment"
    fi
done
