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
