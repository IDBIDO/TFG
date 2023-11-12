from src import mdcgenpy
from src.plotter.raw_data_plotter_2D import RawDataPlotter2D
from src.utils import get_project_root

# Initialize cluster generator (all parameters are optional)
cluster_gen = mdcgenpy.clusters.ClusterGenerator()

# Get tuple with a numpy array with samples and another with labels
data = cluster_gen.generate_data()

configGen = src.mdcgenpy.interface.json_processing.get_cluster_generator('../config/mdcgenpy_config.json')
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
df = mdcgenpy.mdcgenutils.save_csv(data1, "float_data.csv")
print(df)

root = get_project_root()
print(root)
st = str(root)
print(st + "/data/float_data.csv")
a = RawDataPlotter2D(st + "/data/float_data.csv")
print(a.get_label())

a.plot()