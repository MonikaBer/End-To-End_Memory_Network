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
    batch_size):
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
        batch_size = batch_size
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
        batch_size):
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
            batch_size = batch_size
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
        batch_size):
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
        batch_size = batch_size
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

if __name__ == "__main__":
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
                        help = "non-linearity (default: %(default)s)")

    # another parameters
    parser.add_argument("--batch-size", type = int, default = 32,
                        help = "batch size (default: %(default)s)")


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
            batch_size = args.batch_size
        )
    elif args.joint_tasks:
        run_joint_tasks(
            data_dir = args.data_dir,
            epochs = args.epochs,
            hops = args.hops,
            LS = args.LS,
            RN = args.RN,
            BoW = args.BoW,
            LW = args.LW,
            NL = args.NL,
            batch_size = args.batch_size
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
            batch_size = args.batch_size
        )
