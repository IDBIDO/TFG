# from algorithm import sdo
import algorithm.sdo as sdo

# from kmeansmm import KMeansMM
# import hdbscan

import matplotlib.pyplot as plt
import numpy as np

from sklearn.metrics import silhouette_score
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics.cluster import adjusted_rand_score

data_name = "float_data.csv"
name = "float_data.csv"
file_path = "../data/" + name
dataset = np.genfromtxt(file_path, delimiter=',')
print(dataset)
data, y = dataset[:, 0:2], dataset[:, 2].astype(int)

data = MinMaxScaler().fit_transform(data)
[m, n] = data.shape

GT_clusters = len(np.unique(y))  # num clusters in the GT
outBool = False
if min(y) == -1:  # GT comes with outliers (label=-1)
    outBool = True
    GT_clusters = len(np.unique(y)) - 1

sdoclust = sdo.SDOclust()
sdoclust = sdoclust.fit(data)
crisp_labels = sdoclust.predict(data)
outlier_scores = sdoclust.outlierness(data)

contamination = np.sum(y == -1)
outlier_labels = np.zeros(len(y))
if contamination > 0:
    ind = np.argpartition(outlier_scores, -contamination)[-contamination:]
    outlier_labels[ind] = 1

    try:
        S = silhouette_score(data[outlier_labels == 0, :], crisp_labels[outlier_labels == 0], metric='euclidean')
    except:
        S = np.nan
    AR = adjusted_rand_score(y, crisp_labels)

    num_clusters = len(np.unique(crisp_labels))
    if np.min(crisp_labels) == -1:
        num_clusters = num_clusters - 1

    print('Algorithm:', "sdo")
    print('- clusters(GT):', str(GT_clusters), ', clusters(pred):', str(num_clusters))
    print('- Silhouette:', round(S, 2), ', Rand Score:', round(AR, 2))

# Create a scatter plot
plt.scatter(data[outlier_labels == 0, 0], data[outlier_labels == 0, 1], c=crisp_labels[outlier_labels == 0],
            cmap=plt.cm.Paired, s=5)
plt.scatter(data[outlier_labels == 1, 0], data[outlier_labels == 1, 1], c='lightgray', s=5, alpha=0.5)
plt.tick_params(left=False, right=False, labelleft=False, labelbottom=False, bottom=False)
plt.title(data_name)

# Save the plot
plt.savefig(f"plots/2d--{data_name}.png")
