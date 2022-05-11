# End-To-End_Memory_Network
End-To-End Memory Network implementation and experiments

# Documentation
- [v1](https://demo.hedgedoc.org/q6ECn9yVQam88qt6V47kPw?both)
- [final](https://demo.hedgedoc.org/fb0incRUReC2PJciRZXvcA)

# Requirements
- python 2.7
- pip 20.3.4

# Configuration
- create virtual environment:
```
python -m venv venv
source venv/bin/activate
```

- install modules:
```
pip install numpy==1.12.1
```

- download data:
```
cd data/
wget http://www.thespermwhale.com/jaseweston/babi/tasks_1-20_v1-2.tar.gz
tar -xvzf tasks_1-20_v1-2.tar.gz
```

# Execution
```
python2.7 babi_runner.py -t 1
```

To run specific experiment run:
```
./train-experiment.sh -t=1 -e=1 -r=2
```
 * t - task number
 * e - experiment number
 * r - reapet r times
Experiments numeration:


|No |Experiment|
|---|---|
| 1 | BoW |
| 2 | PE |
| 3 | PE + LS |
| 4 | PE + LS + RN |
| 5 | 1 hop + PE + LS + joint | 
| 6 | 2 hop + PE + LS + joint |
| 7 | 3 hop + PE + LS + joint |
| 8 | PE + LS + RN + joint |
| 9 | PE + LS + LW + joint |



To run training for all experiments 10 times on all tasks run:

```
./run-all.sh
```

