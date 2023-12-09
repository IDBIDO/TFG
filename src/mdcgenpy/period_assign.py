import numpy as np

# Example arrays
new_clusters = np.array([1, 2, 3, 4, 1, 2, 5, 6])
old_clusters = np.array([1, 2])

# Find indices of occurrences of old_clusters in new_clusters
indices = np.where(np.in1d(new_clusters, old_clusters))[0]

# Delete occurrences of old_clusters from new_clusters
result = np.delete(new_clusters, indices)

print("Original array:", new_clusters)
print("Subarray to remove:", old_clusters)
print("Resulting array:", result)