import os

import pandas as pd
import numpy as np

from src.utils import get_project_root
from scipy.io import savemat

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
    #print(attributes[0])
    #colum_names = [f'Attribute{i}' for i in range(1, len(attributes[0]) + 1)]

    df = pd.DataFrame(attributes)
    df['Cluster'] = cluster_num

    # print(__file__)
    # path = f'../data/{name}'
    file_path = data_path(name)
    print(file_path)
    df.to_csv(file_path, index=False, header=False)


def save_mat(data, name):
    attributes = np.array(data[0])
    cluster_num = np.array(data[1])

    # Combine attributes and cluster_num into a single matrix
    combined_data = np.column_stack((attributes, cluster_num))

    # Create a dictionary to hold the data, with a key name of your choice
    data_dict = {'cluster_data': combined_data}

    # Define the file path (modify the path as needed)
    file_path = data_path(name)  # Ensure this function returns the desired path

    #print(file_path)

    # Save the data as a .mat file
    savemat(file_path, data_dict)

