#!/bin/bash

programname=$0
function usage {
    echo "usage: $programname [-e=experinent] [-t=task] [-r=reapeat]"
    echo "  -e, --experiment        Number of experiment, 1..9      "
    echo "  -t, --task              Number of task, 1..20"
    echo "  -r, --reapeat           Repeat this many times"
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

if [ -z "$TASK" ]
then
      usage
fi

if [ -z "$TIMES" ]
then
      TIMES=1
fi

RESULT_REGEX='100 \| train error: .*\nTest error: ([0-9]{1,3}([\.]?[0-9]*))'

if [ ! -f results.csv ]; then
    echo "EXPERIMENT;TASK;TRAIN;VAL;TEST" > results.csv
fi

for i in $( eval echo {1..${TIMES}} )
do
    echo "Iteration $i"

    if [ ${EXPERIMENT} -eq 1 ]; then
        #BoW
        RES=$( python2.7 babi_runner.py -t $TASK --BoW | tee /dev/stderr | tee /dev/stderr | grep -Poz "$RESULT_REGEX" )
    elif [ ${EXPERIMENT} -eq 2 ]; then
        #PE
        RES=$( python2.7 babi_runner.py -t $TASK | tee /dev/stderr | grep -Poz "$RESULT_REGEX")
    elif [ ${EXPERIMENT} -eq 3 ]; then
        # PE + LS
        RES=$( python2.7 babi_runner.py -t $TASK --LS | tee /dev/stderr | grep -Poz "$RESULT_REGEX")
    elif [ ${EXPERIMENT} -eq 4 ]; then
        # PE + LS + RN
        RES=$( python2.7 babi_runner.py -t $TASK --LS --RN | tee /dev/stderr | grep -Poz "$RESULT_REGEX")
    elif [ ${EXPERIMENT} -eq 5 ]; then
        # 1 hop + PE + LS + joint
        RES=$( python2.7 babi_runner.py --LS --hops 1 -j | tee /dev/stderr | grep -Poz "$RESULT_REGEX")
    elif [ ${EXPERIMENT} -eq 6 ]; then
        # 2 hop + PE + LS + joint
        RES=$( python2.7 babi_runner.py --LS --hops 2 -j | tee /dev/stderr | grep -Poz "$RESULT_REGEX")
    elif [ ${EXPERIMENT} -eq 7 ]; then
        # 3 hop + PE + LS + joint
        RES=$( python2.7 babi_runner.py --LS --hops 3 -j | tee /dev/stderr | grep -Poz "$RESULT_REGEX")
    elif [ ${EXPERIMENT} -eq 8 ]; then
        # PE + LS + RN + joint
        RES=$( python2.7 babi_runner.py --LS -j -RN | tee /dev/stderr | grep -Poz "$RESULT_REGEX")
    elif [ ${EXPERIMENT} -eq 9 ]; then
        # PE + LS + LW + joint
        RES=$( python2.7 babi_runner.py --LS -j -LW | tee /dev/stderr | grep -Poz "$RESULT_REGEX")
    else
        echo "Unknown experiment"
    fi

    TRAIN=`echo $RES | tee /dev/stderr | grep -Po '(?<=train error: )([0-9]{1,3}([\.]?[0-9]*))'`
    VAL=`echo $RES | tee /dev/stderr | grep -Po '(?<=val error: )([0-9]{1,3}([\.]?[0-9]*))'`
    TEST=`echo $RES | tee /dev/stderr | grep -Po '(?<=Test error: )([0-9]{1,3}([\.]?[0-9]*))'`

    echo "$EXPERIMENT;$TASK;$TRAIN;$VAL;$TEST" >> results.csv
done
