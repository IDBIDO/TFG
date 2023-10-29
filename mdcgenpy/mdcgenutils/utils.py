import pandas as pd
import numpy as np


def read_labeled_data(name):
    """
    Read data from a csv file with labeled data.
    """
    path = f'../data/{name}'
    data = pd.read_csv(path)
    return data


def read_unlabeled_data(name):
    """
    Read data from a csv file with unlabeled data.
    """
    path = f'../data/{name}'
    data = pd.read_csv(path)
    # remove last column (labels)
    data = data.iloc[:, :-1]
    return data


def save_csv(data, name):
    attributes = np.array(data[0])
    cluster_num = np.array(data[1])
    print(attributes[0])
    colum_names = [f'Attribute{i}' for i in range(1, len(attributes[0]) + 1)]

    df = pd.DataFrame(attributes, columns=colum_names)
    df['Cluster'] = cluster_num

    path = f'../data/{name}'
    df.to_csv(path, index=False)
