import matplotlib.pyplot as plt

plt.rcParams.update({'font.size': 18})

# Data from tables (averages)
attributes = ['Training Time (s)', 'Testing Time (s)', 'EN Accuracy', 'F-measure']
values1 = [0.819816, 58.52969, 0.8858, 0.78997]  # Averages from the first table
values2 = [0.78482, 53.4631566, 0.9714, 0.95134]  # Averages from the second table

# Creation of four bar charts in a 2x2 subplot configuration
fig, axes = plt.subplots(2, 2, figsize=(10, 10))  # Adjust to a 2x2 subplot configuration

# Adjusting font size


# Drawing the charts
for i in range(4):
    row, col = i // 2, i % 2  # Determines the subplot position
    axes[row, col].bar('Compacted', values1[i], color='red')
    axes[row, col].bar('Isolated', values2[i], color='blue')
    axes[row, col].set_title(attributes[i])
    axes[row, col].set_ylabel('Value')
    axes[row, col].set_ylim(0, max(values1[i], values2[i]) + 0.1)  # Set the y-axis limit to be slightly higher than the maximum value for clarity

plt.tight_layout()
plt.show()
