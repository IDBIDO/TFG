import pandas as pd


def read_labeled_data(path):
    """
    Read data from a csv file with labeled data.
    """
    data = pd.read_csv(path)
    return data


def read_unlabeled_data(path):
    """
    Read data from a csv file with unlabeled data.
    """
    data = pd.read_csv(path)
    # remove last column (labels)
    data = data.iloc[:, :-1]
    return data
