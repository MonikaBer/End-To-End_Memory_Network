import os
import sys
from numpy import int16
import pandas as pd
from argparse import ArgumentParser

'''
arg:
  string - ex. "(train, min)"
returns:
  tuple - ex. ("train", "min"), where 1st - error type, 2nd - agg func
'''

METRIC_MEAN = "Mean error (%)"
METRIC_COUNT = "Failed tasks (err. > 5%)"

def str2list(s):
    s = s.replace('(', '').replace(')', '').replace(' ', '')
    list_str = map(str, s.split(','))
    return list(list_str)

def get_results_for_one_exp(dataset_exp_setting, agg_setting, results_path):
    try:
        filepath = [f for f in os.listdir(results_path) if dataset_exp_setting in f][0]
        filepath = '%s%s' % (results_path, filepath)
    except:
        print('File with results for %s does not exist' % dataset_exp_setting)
        sys.exit(1)

    df = create_df_with_results(
        filepath = filepath,
        dataset_type = dataset_exp_setting.split('_')[0]
    )

    print(get_aggregation(
            df = df,
            error_type = agg_setting[0],
            agg_func = agg_setting[1])
    )


def get_results_for_all_exps(agg_setting, results_path):
    results_1k_files = []
    results_10k_files = []

    for f in os.listdir(results_path):
        if '10k' in f:
            results_10k_files.append('%s%s' % (results_path, f))
        else:
            results_1k_files.append('%s%s' % (results_path, f))

    df_1k_results = get_results(agg_setting = agg_setting, dataset_type = '1k', results_files = results_1k_files)
    df_10k_results = get_results(agg_setting = agg_setting, dataset_type = '10k', results_files = results_10k_files)
    
    df_paper_results1k = pd.read_csv("./paper_results_table.csv", delimiter=" ")
    df_paper_results1k.index = list(pd.RangeIndex(1,21,1)) + [METRIC_MEAN, METRIC_COUNT]

    df_paper_results10k = pd.read_csv("./paper_results_table_10k.csv", delimiter=" ")
    print(df_paper_results10k.columns)
    # move exp 10 from 5th column to the end
    df_paper_results10k = df_paper_results10k[[str(i) for i in range(1,11,1)]]
    df_paper_results10k.index = list(pd.RangeIndex(1,21,1)) + [METRIC_MEAN, METRIC_COUNT]
    
    df_diff_1k = df_1k_results.subtract(df_paper_results1k)
    df_diff_10k = df_10k_results.subtract(df_paper_results10k)

    print('\nRESULTS FOR 1K DATASET:\n%s' % df_1k_results)
    print('\nRESULTS FOR 10K DATASET:\n%s' % df_10k_results)
    print('\nDIFFERENCE FOR 1K DATASET(CALCULATED RESULTS - PAPER RESULTS):\n%s' % df_diff_1k)
    print('\nDIFFERENCE FOR 10K DATASET(CALCULATED RESULTS - PAPER RESULTS):\n%s' % df_diff_10k)

def create_df_with_results(filepath, dataset_type):
    df = pd.read_csv(filepath, engine = 'python')

    # check if repeats number is correct
    if dataset_type == '1k':
        correct_repeats_cnt = 10
    elif dataset_type == '10k':
        correct_repeats_cnt = 5
    else:
        print('Unrecognized dataset type (only 1k/10k are correct)')
        sys.exit(1)
    try:
        assert all(repeats_cnt == correct_repeats_cnt for repeats_cnt in df['task_id'].value_counts().tolist())
    except:
        print('[WARNING] Number of repeats is incorrect (file: "%s") -> correctly: 5 repeats for 10k, 10 repeats for 1k\n' % filepath)

    return df

def get_aggregation(df, error_type, agg_func):
    if error_type == 'train':
        error_type = 'train_error'
    elif error_type == 'val':
        error_type = 'val_error'
    elif error_type == 'test':
        error_type = 'test_error'
    else:
        print('Unrecognized error type for aggregation (only train/val/test are correct)')
        sys.exit(1)

    if agg_func == 'min':
        return df.loc[df.groupby('task_id')[error_type].idxmin()].reset_index().drop(columns = ['index',])
    elif agg_func == 'max':
        return df.loc[df.groupby('task_id')[error_type].idxmax()].reset_index().drop(columns = ['index',])
    else:
        print('Unrecognized function for aggregation (only min/max are correct)')
        sys.exit(1)

def get_results(agg_setting, dataset_type, results_files):
    tasks_ids = [i for i in range(1, 21)]

    if dataset_type == '1k':
        # 1k dataset
        experiments_ids = [str(i) for i in range(1, 10)]
    else:
        # 10k dataset
        experiments_ids = [str(i) for i in range(1, 11)]

    results_df = pd.DataFrame(index = tasks_ids, columns = experiments_ids, dtype=object)
    results_df = results_df.fillna(0)  # fill new DataFrame with 0s

    for filepath in results_files:
        if dataset_type == '1k':
            # 1k dataset
            exp_nr = filepath[(filepath.find(dataset_type) + 3) : -4]
        else:
            # 10k dataset
            exp_nr = filepath[(filepath.find(dataset_type) + 4) : -4]

        df = create_df_with_results(
            filepath = filepath,
            dataset_type = dataset_type
        )

        df = get_aggregation(
            df = df,
            error_type = agg_setting[0],
            agg_func = agg_setting[1]
        )

        for task in range(1, 21):
            results_df.loc[task, exp_nr] = (df.iloc[task - 1]['test_error'] * 100).round(1)

    results_df.loc[METRIC_MEAN] = results_df.mean().round(1)
    results_df.loc[METRIC_COUNT] = results_df.iloc[:20,:][results_df > 5].count()
    return results_df

def get_additional_metrics(df):
    assert(df.shape[0] == 20)
    return

def main():
    parser = ArgumentParser()
    parser.add_argument("--results-path", type = str, default = "results/",
                        help = "path to results directory (default: %(default)s)")
    parser.add_argument("--agg", type = str, default = "(train, min)",
                        help = "error type and function for aggregation "
                                "(default: '%(default)s' - aggregation by minimal train error); "
                                "1st: train/val/test, "
                                "2nd: max/min")
    parser.add_argument("--dataset_exp", type = str, default = None,
                        help = "show aggregated results for one specific experiment and dataset, "
                        "ex. 10k_1 - dataset 10k, experiment 1. "
                        "(default: %(default)s - show aggregation for all experiments and datasets)")
    args = parser.parse_args()

     # Check if path to results exists
    if not os.path.exists(args.results_path):
        print("The results directory '%s' does not exist" % args.results_path)
        sys.exit(1)

    if args.results_path[-1] != '/':
        args.results_path += '/'

    agg_setting = str2list(args.agg)
    dataset_exp_setting = args.dataset_exp

    if dataset_exp_setting:
        get_results_for_one_exp(dataset_exp_setting, agg_setting, args.results_path)
    else:
        get_results_for_all_exps(agg_setting, args.results_path)

    return 0


if __name__ == "__main__":
    exit(main())
