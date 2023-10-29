import numpy as np
import pandas as pd

def saveCSV(data, path):
    attributes = np.array(data[0])
    cluster_num = np.array(data[1])
    print(attributes[0])
    colum_names = [f'Attribute{i}' for i in range(1, len(attributes[0]) + 1)]

    df = pd.DataFrame(attributes, columns=colum_names)
    df['Cluster'] = cluster_num

    df.to_csv(path, index=False)
