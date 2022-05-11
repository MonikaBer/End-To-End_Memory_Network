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

source venv/bin/activate
mkdir results 2>/dev/null
RESULT_REGEX='(?<=Test error: )([0-9]{1,3}([\.]?[0-9]*))'

for i in $( eval echo {1..${TIMES}} ) 
do
    echo "Iteration $i"

    if [ ${EXPERIMENT} -eq 1 ]; then
        #BoW
        python2.7 babi_runner.py -t $TASK --BoW | tee >( grep -Po "$RESULT_REGEX" >> results/experiment_1.txt )
    elif [ ${EXPERIMENT} -eq 2 ]; then
        #PE
        python2.7 babi_runner.py -t $TASK  | tee >( grep  -Po "$RESULT_REGEX" >> results/experiment_2.txt )
    elif [ ${EXPERIMENT} -eq 3 ]; then
        # PE + LS
        python2.7 babi_runner.py -t $TASK --LS | tee >( grep  -Po "$RESULT_REGEX" >> results/experiment_3.txt )
    elif [ ${EXPERIMENT} -eq 4 ]; then
        # PE + LS + RN
        python2.7 babi_runner.py -t $TASK --LS --RN | tee >( grep  -Po "$RESULT_REGEX" >> results/experiment_4.txt )
    elif [ ${EXPERIMENT} -eq 5 ]; then
        # 1 hop + PE + LS + joint
        python2.7 babi_runner.py --LS --hops 1 -j | tee >( grep  -Po "$RESULT_REGEX" >> results/experiment_5.txt )
    elif [ ${EXPERIMENT} -eq 6 ]; then
        # 2 hop + PE + LS + joint
        python2.7 babi_runner.py --LS --hops 2 -j | tee >( grep  -Po "$RESULT_REGEX" >> results/experiment_6.txt )
    elif [ ${EXPERIMENT} -eq 7 ]; then
        # 3 hop + PE + LS + joint
        python2.7 babi_runner.py --LS --hops 3 -j | tee >( grep  -Po "$RESULT_REGEX" >> results/experiment_7.txt )
    elif [ ${EXPERIMENT} -eq 8 ]; then
        # PE + LS + RN + joint
        python2.7 babi_runner.py --LS -j -RN | tee >( grep  -Po "$RESULT_REGEX" >> results/experiment_8.txt )
    elif [ ${EXPERIMENT} -eq 9 ]; then
        # PE + LS + LW + joint
        python2.7 babi_runner.py --LS -j -LW | tee >( grep  -Po "$RESULT_REGEX" >> results/experiment_9.txt )
    else
        echo "Unknown experiment"
    fi
done