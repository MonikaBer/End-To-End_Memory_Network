import glob
import os
import random
import sys

import argparse
import numpy as np

from config import BabiConfig, BabiConfigJoint
from train_test import train, train_linear_start, test
from util import parse_babi_task, build_model

seed_val = 42
random.seed(seed_val)
np.random.seed(seed_val)  # for reproducing


def run_task(
    task_id,
    data_dir,
    epochs,
    hops,
    LS,
    RN,
    BoW,
    LW,
    NL,
    batch_size,
    lrate_decay_step,
    randomize_time,
    AP,
    ls_nepochs,
    ls_lrate_decay_step,
    init_lrate,
    max_grad_norm,
    embed_dim,
    sent_nr):
    """
    Train and test for each task
    """
    print("Train and test for task %d ..." % task_id)

    # Parse data
    train_files = glob.glob('%s/qa%d_*_train.txt' % (data_dir, task_id))
    test_files  = glob.glob('%s/qa%d_*_test.txt' % (data_dir, task_id))

    dictionary = {"nil": 0}
    train_story, train_questions, train_qstory = parse_babi_task(train_files, dictionary, False)
    test_story, test_questions, test_qstory    = parse_babi_task(test_files, dictionary, False)

    general_config = BabiConfig(
        train_story = train_story,
        train_questions = train_questions,
        dictionary = dictionary,
        epochs = epochs,
        hops = hops,
        LS = LS,
        RN = RN,
        BoW = BoW,
        LW = LW,
        NL = NL,
        batch_size = batch_size,
        lrate_decay_step = lrate_decay_step,
        randomize_time = randomize_time,
        AP = AP,
        ls_nepochs = ls_nepochs,
        ls_lrate_decay_step = ls_lrate_decay_step,
        init_lrate = init_lrate,
        max_grad_norm = max_grad_norm,
        embed_dim = embed_dim,
        sent_nr = sent_nr
    )

    memory, model, loss = build_model(general_config)

    if general_config.linear_start:
        train_linear_start(train_story, train_questions, train_qstory, memory, model, loss, general_config)
    else:
        train(train_story, train_questions, train_qstory, memory, model, loss, general_config)

    test(test_story, test_questions, test_qstory, memory, model, loss, general_config)


def run_all_tasks(
        data_dir,
        epochs,
        hops,
        LS,
        RN,
        BoW,
        LW,
        NL,
        batch_size,
        lrate_decay_step,
        randomize_time,
        AP,
        ls_nepochs,
        ls_lrate_decay_step,
        init_lrate,
        max_grad_norm,
        embed_dim,
        sent_nr):
    """
    Train and test for all tasks
    """
    print("Training and testing for all tasks ...")
    for t in range(20):
        run_task(
            task_id = t + 1,
            data_dir = data_dir,
            epochs = epochs,
            hops = hops,
            LS = LS,
            RN = RN,
            BoW = BoW,
            LW = LW,
            NL = NL,
            batch_size = batch_size,
            lrate_decay_step = lrate_decay_step,
            randomize_time = randomize_time,
            AP = AP,
            ls_nepochs = ls_nepochs,
            ls_lrate_decay_step = ls_lrate_decay_step,
            init_lrate = init_lrate,
            max_grad_norm = max_grad_norm,
            embed_dim = embed_dim,
            sent_nr = sent_nr
        )


def run_joint_tasks(
        data_dir,
        epochs,
        hops,
        LS,
        RN,
        BoW,
        LW,
        NL,
        batch_size,
        lrate_decay_step,
        randomize_time,
        AP,
        ls_nepochs,
        ls_lrate_decay_step,
        init_lrate,
        max_grad_norm,
        embed_dim,
        sent_nr):
    """
    Train and test for all tasks but the trained model is built using training data from all tasks.
    """
    print("Jointly train and test for all tasks ...")
    tasks = range(20)

    # Parse training data
    train_data_path = []
    for t in tasks:
        train_data_path += glob.glob('%s/qa%d_*_train.txt' % (data_dir, t + 1))

    dictionary = {"nil": 0}
    train_story, train_questions, train_qstory = parse_babi_task(train_data_path, dictionary, False)

    # Parse test data for each task so that the dictionary covers all words before training
    for t in tasks:
        test_data_path = glob.glob('%s/qa%d_*_test.txt' % (data_dir, t + 1))
        parse_babi_task(test_data_path, dictionary, False) # ignore output for now

    general_config = BabiConfigJoint(
        train_story = train_story,
        train_questions = train_questions,
        dictionary = dictionary,
        epochs = epochs,
        hops = hops,
        LS = LS,
        RN = RN,
        BoW = BoW,
        LW = LW,
        NL = NL,
        batch_size = batch_size,
        lrate_decay_step = lrate_decay_step,
        randomize_time = randomize_time,
        AP = AP,
        ls_nepochs = ls_nepochs,
        ls_lrate_decay_step = ls_lrate_decay_step,
        init_lrate = init_lrate,
        max_grad_norm = max_grad_norm,
        embed_dim = embed_dim,
        sent_nr = sent_nr
    )

    memory, model, loss = build_model(general_config)

    if general_config.linear_start:
        train_linear_start(train_story, train_questions, train_qstory, memory, model, loss, general_config)
    else:
        train(train_story, train_questions, train_qstory, memory, model, loss, general_config)

    # Test on each task
    for t in tasks:
        print("Testing for task %d ..." % (t + 1))
        test_data_path = glob.glob('%s/qa%d_*_test.txt' % (data_dir, t + 1))
        dc = len(dictionary)
        test_story, test_questions, test_qstory = parse_babi_task(test_data_path, dictionary, False)
        assert dc == len(dictionary)  # make sure that the dictionary already covers all words

        test(test_story, test_questions, test_qstory, memory, model, loss, general_config)


def main():
    parser = argparse.ArgumentParser()
    # dataset 1k/10k
    parser.add_argument("-d", "--data-dir", default = "data/tasks_1-20_v1-2/en",
                        help = "path to dataset directory (default: %(default)s)")

    # experiment variants
    parser.add_argument("--epochs", type = int,
                        help = "number of epochs (default: 100 - single, 60 - joint)")
    parser.add_argument("--hops", type = int, default = 3,
                        help = "number of hops (default: %(default)s)")
    parser.add_argument("--LS", action = "store_true",
                        help = "linear-start (default: %(default)s)")
    parser.add_argument("--RN", action = "store_true",
                        help = "random noise (default: %(default)s)")
    parser.add_argument("--BoW", action = "store_true",
                        help = "Bag of Words (instead of Position Encoding) (default: %(default)s)")
    parser.add_argument("--LW", action = "store_true",
                        help = "layer-wise (instead of adjacent) weight tying (default: %(default)s)")
    parser.add_argument("--NL", action = "store_true",
                        help = "add non-linearity to internal states (default: %(default)s)")

    # another parameters
    parser.add_argument("--batch-size", type = int, default = 32,
                        help = "batch size (default: %(default)s)")
    parser.add_argument("--lrate-decay-step", type = int,
                        help = "learning rate decay step (default: 25 - single, 15 - joint)")
    parser.add_argument("--randomize-time", type = float, default = 0.1,
                        help = "amount of noise injected into time index (default: %(default)s)")
    parser.add_argument("--AP", action = "store_true",
                        help = "add linear layer between internal states (default: %(default)s)")
    parser.add_argument("--ls-nepochs", type = int,
                        help = "number of epochs for LS (default: 20 - single, 30 - joint))")
    parser.add_argument("--ls-lrate-decay-step", type = int,
                        help = "learning rate decay step for LS (default: 21 - single, 31 - joint)")
    parser.add_argument("--init-lrate", type = float, default = 0.01,
                        help = "initial learning rate (default: %(default)s)")
    parser.add_argument("--max-grad-norm", type = int, default = 40,
                        help = "max gradient norm (default: %(default)s)")
    parser.add_argument("--embed-dim", type = int,
                        help = "embedding dimension (for input and output) (default: 20 - single, 50 - joint)")
    parser.add_argument("--sent-nr", type = int, default = 50,
                        help = "number of recent sentences in memory (default: %(default)s)")

    # single/all/joint training
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-t", "--task", default = "1", type = int,
                       help = "train and test for a single task (default: %(default)s)")
    group.add_argument("-a", "--all-tasks", action = "store_true",
                       help = "train and test for all tasks (one by one) (default: %(default)s)")
    group.add_argument("-j", "--joint-tasks", action = "store_true",
                       help = "train and test for all tasks (all together) (default: %(default)s)")
    args = parser.parse_args()

    # Check if data is available
    if not os.path.exists(args.data_dir):
        print("The data directory '%s' does not exist. Please download it first." % args.data_dir)
        sys.exit(1)
    print("Using data from %s" % args.data_dir)

    if args.joint_tasks:
        # joint training
        if args.epochs == None:
            args.epochs = 60
        if args.lrate_decay_step == None:
            args.lrate_decay_step = 15
        if args.ls_nepochs == None:
            args.ls_nepochs = 30
        if args.ls_lrate_decay_step == None:
            args.ls_lrate_decay_step = 31
        if args.embed_dim == None:
            args.embed_dim = 50

        run_joint_tasks(
            data_dir = args.data_dir,
            epochs = args.epochs,
            hops = args.hops,
            LS = args.LS,
            RN = args.RN,
            BoW = args.BoW,
            LW = args.LW,
            NL = args.NL,
            batch_size = args.batch_size,
            lrate_decay_step = args.lrate_decay_step,
            randomize_time = args.randomize_time,
            AP = args.AP,
            ls_nepochs = args.ls_nepochs,
            ls_lrate_decay_step = args.ls_lrate_decay_step,
            init_lrate = args.init_lrate,
            max_grad_norm = args.max_grad_norm,
            embed_dim = args.embed_dim,
            sent_nr = args.sent_nr
        )
        return 0

    # per-task training
    if args.epochs == None:
        args.epochs = 100
    if args.lrate_decay_step == None:
        args.lrate_decay_step = 25
    if args.ls_nepochs == None:
        args.ls_nepochs = 20
    if args.ls_lrate_decay_step == None:
        args.ls_lrate_decay_step = 21
    if args.embed_dim == None:
        args.embed_dim = 20

    if args.all_tasks:
        run_all_tasks(
            data_dir = args.data_dir,
            epochs = args.epochs,
            hops = args.hops,
            LS = args.LS,
            RN = args.RN,
            BoW = args.BoW,
            LW = args.LW,
            NL = args.NL,
            batch_size = args.batch_size,
            lrate_decay_step = args.lrate_decay_step,
            randomize_time = args.randomize_time,
            AP = args.AP,
            ls_nepochs = args.ls_nepochs,
            ls_lrate_decay_step = args.ls_lrate_decay_step,
            init_lrate = args.init_lrate,
            max_grad_norm = args.max_grad_norm,
            embed_dim = args.embed_dim,
            sent_nr = args.sent_nr
        )
    else:
        run_task(
            task_id = args.task,
            data_dir = args.data_dir,
            epochs = args.epochs,
            hops = args.hops,
            LS = args.LS,
            RN = args.RN,
            BoW = args.BoW,
            LW = args.LW,
            NL = args.NL,
            batch_size = args.batch_size,
            lrate_decay_step = args.lrate_decay_step,
            randomize_time = args.randomize_time,
            AP = args.AP,
            ls_nepochs = args.ls_nepochs,
            ls_lrate_decay_step = args.ls_lrate_decay_step,
            init_lrate = args.init_lrate,
            max_grad_norm = args.max_grad_norm,
            embed_dim = args.embed_dim,
            sent_nr = args.sent_nr
        )

    return 0


if __name__ == "__main__":
    exit(main())
