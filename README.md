# End-To-End_Memory_Network
End-To-End Memory Network implementation and experiments

# Documentation
- [v1](https://demo.hedgedoc.org/q6ECn9yVQam88qt6V47kPw?both)
- [final](https://demo.hedgedoc.org/fb0incRUReC2PJciRZXvcA)

# Requirements
- python 2.7
```
sudo apt-install python2.7
python2.7 --version
```

- pip 20.3.4 (for python2.7)
```
sudo apt update
sudo apt install curl
sudo add-apt-repository universe
sudo apt update
curl https://bootstrap.pypa.io/pip/2.7/get-pip.py --output get-pip.py
sudo python2.7 get-pip.py
rm get-pip.py
pip --version
```

-- virtualenv
```
sudo pip install virtualenv
```

# Configuration
- create virtual environment:
```
virtualenv -p /usr/bin/python2.7 venv2.7
source venv2.7/bin/activate
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
rm tasks_1-20_v1-2.tar.gz
```

# Execution
1. Scripts for model training
- Python script
```
python2.7 babi_runner.py -t 1
```

- To run specific experiment run:
```
./run-experiment.sh -t=1 -e=1 -d=1 -r=2
```
 * t - task number
 * e - experiment number
 * d - dataset type (1 - for 1k, 10 - for 10k)
 * r - number of repeats

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
| 10* | PE + LS + LW + RN + NL |

##### 10* - only for 10k dataset (embedding dimension = 100)

- To run one single-task experiment 10 times on all tasks run:
```
./run-one-single.sh <exp_nr> <dataset_type>
```

- To run one joint-task experiment 10 times run:
```
./run-one-joint.sh <exp_nr> <dataset_type>
```

- To run all experiments 10 times on all tasks run:
```
./run-all.sh <dataset_type>
```

2. Script for results visualisation
```
python2.7 show_results.py --agg "(train, min)" --results-path "results/" --dataset_exp 10k_10
```
