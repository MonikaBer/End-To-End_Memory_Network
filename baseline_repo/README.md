# MemN2N-babi-python repo [link](https://github.com/vinhkhuc/MemN2N-babi-python)

## End-To-End Memory Networks for Question Answering
This is an implementation of MemN2N model in Python for the [bAbI question-answering tasks](http://fb.ai/babi)
as shown in the Section 4 of the paper "[End-To-End Memory Networks](http://arxiv.org/abs/1503.08895)". It is based on
Facebook's [Matlab code](https://github.com/facebook/MemNN/tree/master/MemN2N-babi-matlab).

## Requirements
* Python 2.7
* Numpy, can be installed via pip:
```
$ sudo pip install -r requirements.txt
```
* [bAbI dataset](http://fb.ai/babi) should be downloaded to `data/tasks_1-20_v1-2`:
```
$ wget -qO- http://www.thespermwhale.com/jaseweston/babi/tasks_1-20_v1-2.tar.gz | tar xvz -C data
```

### Author
Vinh Khuc

### References
* Sainbayar Sukhbaatar, Arthur Szlam, Jason Weston, Rob Fergus,
  "[End-To-End Memory Networks](http://arxiv.org/abs/1503.08895)",
  *arXiv:1503.08895 [cs.NE]*.
