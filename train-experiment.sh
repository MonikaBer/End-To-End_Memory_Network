#!/bin/bash
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
            # unknown option
    ;;
esac
done

if [ ${EXPERIMENT} -ge 5 ]; then
    echo "Running joint, task number wont matter"
fi


source venv/bin/activate
mkdir results 2>/dev/null
RESULT_REGEX='(?<=Test error: )([0-9]{1,3}([\.]?[0-9]*))'

for i in $( eval echo {1..${TIMES}} ) 
do
    echo "Iteration $i"

    if [ ${EXPERIMENT} -eq 1 ]; then
        #BoW
        python2.7 babi_runner.py -t $TASK --BoW | grep -Po "$RESULT_REGEX" >> results/e_1.txt
    elif [ ${EXPERIMENT} -eq 2 ]; then
        #PE
        python2.7 babi_runner.py -t $TASK  | grep -Po "$RESULT_REGEX" >> results/e_2.txt
    elif [ ${EXPERIMENT} -eq 3 ]; then
        # PE + LS
        python2.7 babi_runner.py -t $TASK --LS | grep -Po "$RESULT_REGEX" >> results/e_3.txt
    elif [ ${EXPERIMENT} -eq 4 ]; then
        # PE + LS + RN
        python2.7 babi_runner.py -t $TASK --LS --RN | grep -Po "$RESULT_REGEX" >> results/e_4.txt
    elif [ ${EXPERIMENT} -eq 5 ]; then
        # 1 hop + PE + LS + joint
        python2.7 babi_runner.py --LS --hops 1 -j | grep -Po "$RESULT_REGEX" >> results/e_5.txt
    elif [ ${EXPERIMENT} -eq 6 ]; then
        # 2 hop + PE + LS + joint
        python2.7 babi_runner.py --LS --hops 2 -j | grep -Po "$RESULT_REGEX" >> results/e_6.txt
    elif [ ${EXPERIMENT} -eq 7 ]; then
        # 3 hop + PE + LS + joint
        python2.7 babi_runner.py --LS --hops 3 -j | grep -Po "$RESULT_REGEX" >> results/e_7.txt
    elif [ ${EXPERIMENT} -eq 8 ]; then
        # PE + LS + RN + joint
        python2.7 babi_runner.py --LS -j -RN | grep -Po "$RESULT_REGEX" >> results/e_8.txt
    elif [ ${EXPERIMENT} -eq 9 ]; then
        # PE + LS + LW + joint
        python2.7 babi_runner.py --LS -j -LW | grep -Po "$RESULT_REGEX" >> results/e_9.txt
    else
        echo "Unknown experiment"
    fi
done