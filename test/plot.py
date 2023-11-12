from src import mdcgenpy as mdc
import matplotlib.pyplot as plt

data = mdc.mdcgenutils.read_data_and_label('float_data.csv')
print(data)
print(data["Attribute1"])
data_row0 = data.iloc[0]

print("\nData row 0: ")
print(data_row0)
print(data_row0["Attribute1"])

"""
Plot the data in 2D using matplotlib.
"""
x = data["Attribute1"]
y = data["Attribute2"]
plt.scatter(x, y, label='Data Points', color='blue', marker='o')
# Set plot labels
plt.xlabel('Attribute1 (x)')
plt.ylabel('Attribute2 (y)')
plt.title('Scatter Plot of Attribute1 vs. Attribute2')
# Display the plot
plt.legend()
plt.grid(True)
plt.show()
