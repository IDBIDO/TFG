from __future__ import division
import math
import sys

import numpy as np
import scipy.linalg


def delete_one_old_cluster(clus_cfg):
    # extract keys and probabilities
    keys, probabilities = zip(*clus_cfg.clusters_live_probability.items())
    # choose one cluster to delete
    delete_cluster = np.random.choice(keys, p=probabilities)
    del clus_cfg.clusters_live_probability[delete_cluster]


def apply_dead_factor(clus_cfg):
    # apply dead factor
    decrease_prob = 0.2 * clus_cfg.dead_factor  # 0.2 is a magic number, need to be tuned
    for key, prob in clus_cfg.clusters_live_probability.items():
        clus_cfg.clusters_live_probability[key] = prob * (1 - decrease_prob)


def decrease_old_probabilities(clus_cfg):
    period_clusters = clus_cfg.n_old_cluster + clus_cfg.n_new_cluster
    # old_clusters = clus_cfg.clus_cfg.n_old_cluster
    free_probability = (1 / period_clusters) * clus_cfg.n_new_cluster
    # reduce all old probabilities by free_probability

    for key, prob in clus_cfg.clusters_live_probability.items():
        reduce_prob = prob * free_probability
        clus_cfg.clusters_live_probability[key] = prob - reduce_prob


def update_live_clusters(clus_cfg):
    print("current live probabilities: ", clus_cfg.clusters_live_probability)

    size_live_probability = len(list(clus_cfg.clusters_live_probability.values()))
    if size_live_probability >= clus_cfg.n_old_cluster + clus_cfg.n_new_cluster:
        # delete one old cluster
        delete_one_old_cluster(clus_cfg)
    else:
        # normalize new probabilities
        decrease_old_probabilities(clus_cfg)

    # apply dead factor
    apply_dead_factor(clus_cfg)

    # add new clusters, choose clus_cfg.n_new_cluster clusters with uniform probability
    print("new clusters: ", clus_cfg.new_clusters)
    new_clusters = np.random.choice(clus_cfg.new_clusters, clus_cfg.n_new_cluster, replace=False)
    probability_used = sum(list(clus_cfg.clusters_live_probability.values()))
    # remaining probability divided uniformly to new clusters
    new_clusters_prob = (1 - probability_used) / clus_cfg.n_new_cluster
    # add new clusters to live probability
    for cluster in new_clusters:
        clus_cfg.clusters_live_probability[cluster] = new_clusters_prob
    # update new clusters, delete assigned clusters
    indices = np.where(np.in1d(clus_cfg.new_clusters, new_clusters))[0]
    clus_cfg.new_clusters = np.delete(clus_cfg.new_clusters, indices)
    print("new clusters array: ", clus_cfg.new_clusters)
    print("new live probabilities: ", clus_cfg.clusters_live_probability)

    return clus_cfg.clusters_live_probability


def compute_current_label(clus_cfg):
    # extract keys for current live clusters
    keys_t, _ = zip(*clus_cfg.clusters_live_probability.items())
    keys = list(keys_t)

    # get mass for current clusters
    keys_mass = {}
    sum_mass = 0
    print("keys: ", keys)
    for key in keys:
        keys_mass[key] = clus_cfg.mass[key]
        sum_mass += clus_cfg.mass[key]

    # compute clusters probability for labels
    prob = []
    aux_label = []
    for key in keys_mass:
        prob.append(keys_mass[key] / sum_mass)
        aux_label.append(key)
    print("prob: ", prob)
    # compute current label
    current_label = np.random.choice(aux_label, clus_cfg.n_samples_per_period, p=prob)
    print("current label: ", current_label)
    print("current label size: ", len(current_label))

    # compute current label probability
    current_label_prob = {}
    for key in keys:
        current_label_prob[key] = 0
    for label in current_label:
        current_label_prob[label] += 1

    print("current label probability: ", current_label_prob)
    for key in keys:
        current_label_prob[key] /= clus_cfg.n_samples_per_period

    print("current label probability: ", current_label_prob)
    return current_label


def compute_all_labels(clus_cfg):
    clus_cfg.labels = np.concatenate((clus_cfg.labels, compute_current_label(clus_cfg)))
    for i in range(clus_cfg.n_periods - 1):
        update_live_clusters(clus_cfg)
        clus_cfg.labels = np.concatenate((clus_cfg.labels, compute_current_label(clus_cfg)))
        #compute_current_label(clus_cfg)
        print("---------period: ", i, "-------------------------")
    print("labels: ", clus_cfg.labels)
    print("labels size: ", len(clus_cfg.labels))

def generate_mass(clus_cfg):
    """
    Get the number of samples to generate for each cluster.

    Args:
        clus_cfg (clusters.DataConfig): Configuration

    Returns:
        np.array: Array with len == nr of clusters, where each entry is the number of samples in the corresponding
            to generate in the corresponding cluster.
    """
    if type(clus_cfg.k) == list:
        mass = np.array(clus_cfg.k)
    else:
        mass = np.random.uniform(0, 1, clus_cfg.n_clusters)
        total_mass = mass.sum()
        mass = np.vectorize(math.floor)(clus_cfg.n_samples * mass / total_mass)
        abs_mass = mass.sum()
        if abs_mass < clus_cfg.n_samples:  # if samples are unassigned, send them to the cluster with least samples
            min_ind = np.argmin(mass)
            mass[min_ind] += clus_cfg.n_samples - abs_mass

        # guarantee there are enough samples in each cluster
        if clus_cfg.min_samples <= 0:
            min_mass = round(clus_cfg.n_samples / (clus_cfg.ki_coeff * clus_cfg.n_clusters))
        else:
            min_mass = clus_cfg.min_samples
        need_to_add = True
        while need_to_add:
            need_to_add = False
            min_ind = np.argmin(mass)
            if mass[min_ind] < min_mass:
                max_ind = np.argmax(mass)
                extra = min_mass - mass[min_ind]
                mass[max_ind] -= extra
                mass[min_ind] += extra
                need_to_add = True

    return mass.astype(dtype=float)


def locate_centroids(clus_cfg):
    """
    Generate locations for the centroids of the clusters.

    Args:
        clus_cfg (clusters.DataConfig): Configuration.

    Returns:
        np.array: Matrix (n_clusters, n_feats) with positions of centroids.
    """
    centroids = np.zeros((clus_cfg.n_clusters, clus_cfg.n_feats))

    p = 1.
    idx = 1
    for i, c in enumerate(clus_cfg._cmax):
        p *= c
        if p > 2 * clus_cfg.n_clusters + clus_cfg.outliers / clus_cfg.n_clusters:
            idx = i
            break
    idx += 1

    locis = np.arange(p)
    np.random.shuffle(locis)
    clin = locis[:clus_cfg.n_clusters]

    # voodoo magic for obtaining centroids
    res = clin
    for j in range(idx):
        center = ((res % clus_cfg._cmax[j]) + 1) / (clus_cfg._cmax[j] + 1)
        noise = (np.random.rand(clus_cfg.n_clusters) - 0.5) * clus_cfg.compactness_factor
        centroids[:, j] = center + noise
        res = np.floor(res / clus_cfg._cmax[j])
    for j in range(idx, clus_cfg.n_feats):
        center = np.floor(clus_cfg._cmax[j] * np.random.rand(clus_cfg.n_clusters) + 1) / (clus_cfg._cmax[j] + 1)
        noise = (np.random.rand(clus_cfg.n_clusters) - 0.5) * clus_cfg.compactness_factor
        centroids[:, j] = center + noise

    return centroids, locis, idx


def generate_clusters(clus_cfg, batch_size=0):
    """
    Generate data.

    Args:
        clus_cfg (clusters.DataConfig): Configuration.
        batch_size (int): Number of samples for each batch.

    Yields:
        np.array: Generated samples.
        np.array: Labels for the samples.
    """
    # generate correlation and rotation matrices
    for cluster in clus_cfg.clusters:
        # generate random symmetric matrix with ones in the diagonal
        # uses the vine method described here
        # http://stats.stackexchange.com/questions/2746/how-to-efficiently-generate-random-positive-semidefinite-correlation-matrices
        # using the correlation input parameter to set a threshold on the values of the correlation matrix
        corr = np.eye(clus_cfg.n_feats)
        aux = np.zeros(corr.shape)

        beta_param = 4

        for k in range(clus_cfg.n_feats - 1):
            for i in range(k + 1, clus_cfg.n_feats):
                aux[k, i] = 2 * cluster.corr * (np.random.beta(beta_param, beta_param) - 0.5)
                p = aux[k, i]
                for l in range(k - 1, -1, -1):
                    p = p * np.sqrt((1 - aux[l, i] ** 2) * (1 - aux[l, k] ** 2)) + aux[l, i] * aux[l, k]
                corr[k, i] = p
                corr[i, k] = p
        perm = np.random.permutation(clus_cfg.n_feats)
        corr = corr[perm, :][:, perm]
        cluster.corr_matrix = np.linalg.cholesky(corr)
        cluster.correlation_matrix = corr

        # rotation matrix
        if cluster.rotate:
            cluster.rotation_matrix = get_rotation_matrix(clus_cfg.n_feats)

    if batch_size == 0:
        batch_size = clus_cfg.n_samples
    print(f'batch_size: {batch_size}')
    for batch in range(((clus_cfg.n_samples - 1) // batch_size) + 1):
        n_samples = min(batch_size, clus_cfg.n_samples - batch * batch_size)
        data, labels = compute_batch(clus_cfg, n_samples)
        yield data, np.reshape(labels, (len(labels), 1))


def get_rotation_matrix(n_feats):
    rot_mat = 2 * (np.random.rand(n_feats, n_feats) - 0.5)
    ort = scipy.linalg.orth(rot_mat)
    if ort.shape == rot_mat.shape:  # check if `rot_mat` is full rank, so that `ort` keeps the same shape
        return ort
    else:
        return get_rotation_matrix(n_feats)


def compute_batch(clus_cfg, n_samples):
    """
    Generates one batch of data.

    Args:
        clus_cfg (clusters.DataConfig): Configuration.
        n_samples (int): Number of samples in the batch.

    Returns:
        np.array: Generated sample.
    """
    # get probabilities of each class
    mass = clus_cfg.mass

    mass = np.insert(mass, 0, clus_cfg.outliers)  # class 0 is now the outliers (this changes to -1 further down)
    mass /= mass.sum()

    # print(f'mass: {mass}')
    # labels = np.arange(clus_cfg.n_clusters)
    # labels = np.tile(labels, n_samples // clus_cfg.n_clusters)[:n_samples]

    labels = clus_cfg.labels # np.random.choice(clus_cfg.n_clusters + 1, n_samples, p=mass) - 1

    # np.set_printoptions(threshold=np.inf)
    # print(f'labels: {labels}')
    # print(f'len(labels): {len(labels)}')
    # label -1 corresponds to outliers
    data = np.zeros((n_samples, clus_cfg.n_feats))

    # generate samples for each cluster
    for label in range(clus_cfg.n_clusters):
        print(f'cluster: {label}')
        print(clus_cfg.k)
        print(clus_cfg.n_clusters)
        # print(f'cluster: {label}')
        cluster = clus_cfg.clusters[label]
        indexes = (labels == label)
        # print(f'indexes: {indexes}')
        samples = sum(indexes)  # nr of samples in this cluster
        data[indexes] = cluster.generate_data(samples)

        data[indexes] = data[indexes].dot(cluster.corr_matrix)  # apply correlation to data

        # apply rotation
        if cluster.rotate:
            data[indexes] = data[indexes].dot(cluster.rotation_matrix)

        # add centroid
        data[indexes] += clus_cfg._centroids[label]

        # add noisy variables
        for d in cluster.n_noise:
            data[indexes, d] = np.random.rand(samples)

    # generate outliers
    indexes = (labels == -1)
    out = sum(indexes)

    # voodoo magic for generating outliers
    locis = clus_cfg._locis[clus_cfg.n_clusters:]
    res = locis[np.arange(out) % len(locis)]
    for j in range(clus_cfg._idx):
        center = ((res % clus_cfg._cmax[j]) + 1) / (clus_cfg._cmax[j] + 1)
        noise = (1 / (clus_cfg._cmax[j] + 1)) * np.random.rand(out) - (1 / (2 * (clus_cfg._cmax[j] + 1)))
        data[indexes, j] = center + noise
        res = np.floor(res / clus_cfg._cmax[j])
    for j in range(clus_cfg._idx, clus_cfg.n_feats):
        center = np.floor(clus_cfg._cmax[j] * (np.random.rand(out) + 1)) / (clus_cfg._cmax[j] + 1)
        noise = (1 / (clus_cfg._cmax[j] + 1)) * np.random.rand(out) - (1 / (2 * (clus_cfg._cmax[j] + 1)))
        data[indexes, j] = center + noise

    return data, labels
