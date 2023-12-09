import math

import numpy as np

import mdcgenpy
from src.plotter.raw_data_plotter_2D import RawDataPlotter2D
from src.utils import get_project_root

# Initialize cluster generator (all parameters are optional)
cluster_gen = mdcgenpy.clusters.ClusterGenerator()

# Get tuple with a numpy array with samples and another with labels
#data = cluster_gen.generate_data()

configGen = mdcgenpy.interface.json_processing.get_cluster_generator('../config/mdcgenpy_config.json')
# data1 is a generator
data1 = configGen.generate_data()

# mass = np.random.uniform(0, 1, 3)
# print(mass)
# mass = np.vectorize(math.floor)(100 * mass / mass.sum())
# print(mass)
# print("ddddd")
# Specify the CSV file path
#csv_file = "float_data.csv"
# print(data1[1][0])
# datax = np.array(data1[0])
# datay = np.array(data1[1])
# datax = np.column_stack((datax, datay))
# print(datax)

# Save the data to the CSV file
mdcgenpy.mdcgenutils.save_csv(data1, "float_data.csv")

root = get_project_root()
a = RawDataPlotter2D("float_data.csv")

a.plot()
