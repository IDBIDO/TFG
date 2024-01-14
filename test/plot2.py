import matplotlib.pyplot as plt

plt.rcParams.update({'font.size': 18})

# Data for averages for the 4 datasets (4, 7, 10, 20 dimensions)
dimensions = [2, 4, 7, 10, 20]

# Averages of Training Time, Testing Time, EN Accuracy, and F-measure for each dataset
average_training_times = [0.78482, 0.8546934, 0.8936074, 0.9783662, 0.966024]
average_testing_times = [53.4631566, 59.0747744, 60.9524396, 62.8507018, 65.0495664]
average_en_accuracies = [0.9714, 0.9299, 0.9224, 0.918, 0.8855]
average_f_measures = [0.95134, 0.888608, 0.878108, 0.872084, 0.83003]


# average_training_times = [0.819816, 0.8206878, 0.81511, 0.858829, 0.8543264]
# average_testing_times = [58.52969, 67.7539788, 68.04064, 73.850808, 80.7866756]
# average_en_accuracies = [0.8858, 0.7725, 0.6918, 0.6798, 0.6474]
# average_f_measures = [0.78997, 0.553858, 0.25801, 0.27372, 0.276936]


# average_training_times average_testing_times average_en_accuracies average_f_measures
# 0.78482 53.4631566 0.9714 0.95134
# 0.8546934 59.0747744 0.9299 0.888608
# 0.8936074 60.9524396 0.9224 0.878108
# 0.9783662 62.8507018 0.918 0.872084
# 0.966024 65.0495664 0.8855 0.83003

# Creating 4 plots for each metric
fig, axes = plt.subplots(2, 2, figsize=(12, 10))
axes = axes.ravel()  # Flatten the array of axes for easier indexing

metrics = [average_training_times, average_testing_times, average_en_accuracies, average_f_measures]
metric_names = ['Average Training Time (s)', 'Average Testing Time (s)', 'Average EN Accuracy', 'Average F-measure']

for i in range(4):
    axes[i].plot(dimensions, metrics[i], marker='o')
    axes[i].set_title(metric_names[i])
    axes[i].set_xlabel('Dimensions')
    axes[i].set_ylabel(metric_names[i])
    axes[i].grid(True)
    # Ensuring that the scale starts from 0
    axes[i].set_ylim(0, max(metrics[i]) * 1.1)  # Add an additional 10% for space above

plt.tight_layout()
plt.show()
