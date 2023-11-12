import os

import pandas as pd
import numpy as np

from src.utils import get_project_root


def data_path(name):
    root = get_project_root()
    file_path = str(root) + "/data/" + name
    return file_path


def read_data_and_label(name):
    """
    Read data from a csv file with labeled data.
    """
    path = data_path(name)
    dataset = np.genfromtxt(path, delimiter=',')
    data, y = dataset[:, 0:2], dataset[:, 2].astype(int)
    return data, y

def save_csv(data, name):
    attributes = np.array(data[0])
    cluster_num = np.array(data[1])
    print(attributes[0])
    colum_names = [f'Attribute{i}' for i in range(1, len(attributes[0]) + 1)]

    df = pd.DataFrame(attributes, columns=colum_names)
    df['Cluster'] = cluster_num

    # print(__file__)
    # path = f'../data/{name}'
    file_path = data_path(name)
    print(file_path)
    df.to_csv(file_path, index=False, header=False)
