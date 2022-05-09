# End-To-End_Memory_Network
End-To-End Memory Network implementation and experiments

# Documentation
- [v1](https://demo.hedgedoc.org/q6ECn9yVQam88qt6V47kPw?both)
- [final](https://demo.hedgedoc.org/fb0incRUReC2PJciRZXvcA)

# Requirements
- python 3.8.10
- pip 20.0.2

# Configuration
- create virtual environment:
```
python -m venv venv
source venv/bin/activate
```

- install [PyTorch](https://pytorch.org/)

- install another modules:
```
pip install click
pip install torchtext==0.6.0
```

# Execution
```
python MemN2N/cli.py --help
python MemN2N/cli.py --train --gpu
```
