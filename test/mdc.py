import csv

from matplotlib import pyplot as plt

import mdcgenpy

import numpy as np


# Initialize cluster generator (all parameters are optional)
cluster_gen = mdcgenpy.clusters.ClusterGenerator()

# Get tuple with a numpy array with samples and another with labels
data = cluster_gen.generate_data()

configGen = mdcgenpy.interface.json_processing.get_cluster_generator('mdc.json')
# data1 is a generator
data1 = configGen.generate_data()

# Specify the CSV file path
#csv_file = "float_data.csv"
# print(data1[1][0])
# datax = np.array(data1[0])
# datay = np.array(data1[1])
# datax = np.column_stack((datax, datay))
# print(datax)

# Save the data to the CSV file
df = mdcgenpy.saveData.saveCSV(data1, "float_data.csv")
print(df)