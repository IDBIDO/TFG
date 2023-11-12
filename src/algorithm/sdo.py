import math
import numpy as np
import scipy.spatial.distance as distance
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from src.algorithm.gbc import ConnectedComponentsClustering


def extend_labels(X, O, l, knn=5, chunksize=None):
    [m, n] = X.shape
    [k, n] = O.shape
    cl = len(np.unique(l))

    if chunksize is None:
        chunksize = m

    C = np.zeros((m, cl))

    for i in range(0, m, chunksize):
        dist = distance.cdist(X[i:(i + chunksize)], O)
        dist_sorted = np.argsort(dist, axis=1)
        closest = dist_sorted[:, 0:knn]
        lknn = l[closest]

        for j in range(0, cl):
            C[i:(i + chunksize), j] = np.sum(lknn == j, axis=1)

    return C / knn, np.argmax(C, axis=1)


def graph_clust(x, zeta, chi, chi_min, chi_prop):
    model = ConnectedComponentsClustering(zeta, chi, chi_min, chi_prop, metric="euclidean", n_jobs=-1)
    l = model.fit_predict(x)
    return l


def hbdiscret(O):
    [m, n] = O.shape
    Od = np.copy(O)
    nbins = int(20 * np.sqrt(m))
    for i in range(n):
        Oi = O[:, i]
        bins = np.histogram_bin_edges(Oi, bins=nbins)
        midbins = bins[:-1] + (bins[1:] - bins[:-1]) / 2
        midbins = np.append(midbins, np.max(Oi))
        ind = np.digitize(Oi, bins) - 1
        Od[:, i] = midbins[ind]
    Od = np.unique(Od, axis=0)
    kd = Od.shape[0]
    return Od, kd


def sample_size(N, s, e):
    z = 1.96
    num = N * pow(z, 2) * pow(s, 2)
    den = (N - 1) * pow(e, 2) + pow(z, 2) * pow(s, 2)
    n = int(math.floor(num / den))
    return n


def smoothing(O, x, f):
    [k, n] = O.shape
    dist = distance.cdist(O, O)
    dist_sorted = np.sort(dist, axis=1)
    O_sorted = np.argsort(dist, axis=1)
    closest = O_sorted[:, 1:x + 1]
    dist_closest = dist_sorted[:, 1:x + 1]
    dmean = np.mean(dist_closest, axis=1)
    inc = (dist_closest - dmean[:, None]) * f * -1
    Ohat = (O / np.linalg.norm(O, axis=1)[:, None])

    for i in range(k):
        O[i, :] = O[i, :] + np.sum(Ohat[closest[i]] * inc[i][:, None], axis=0)
    return O


class SDO:

    def __init__(self, x=5, qv=0.3, hbs=False, smooth=False, smooth_f=0.25, rseed=0, k=None, q=None, chunksize=None):
        self.x = x
        self.qv = qv
        self.hbs = hbs
        self.smooth = smooth
        self.smooth_f = smooth_f
        self.rseed = rseed
        self.k = k
        self.q = q
        self.chunksize = chunksize
        self.O = None

    def fit(self, X):

        [m, n] = X.shape

        if self.k is None:
            Xt = StandardScaler().fit_transform(X)
            pca = PCA(n_components=2)
            Xp = pca.fit_transform(Xt)
            sigma = np.std(Xp)
            if sigma < 1:
                sigma = 1
            error = 0.1 * np.std(Xp);
            self.k = sample_size(m, sigma, error)
            k = self.k

        chunksize = self.chunksize
        if chunksize is None:
            chunksize = m

        np.random.seed(self.rseed)
        index = np.random.permutation(m)
        O = X[index[0:k]]

        if self.hbs:
            O, k = hbdiscret(O)

        if self.smooth:
            O = smoothing(O, x, self.smooth_f)

        # TRAINING
        P = np.zeros(k)

        for i in range(0, m, chunksize):
            dist = distance.cdist(X[i:(i + chunksize)], O)
            dist_sorted = np.argsort(dist, axis=1)
            closest = dist_sorted[:, 0:self.x].flatten()

            P += np.count_nonzero(closest[:, np.newaxis] == np.arange(k), 0)

        if self.q is None:
            q = np.quantile(P, self.qv)

        O = O[P >= q]
        # P = P[P>=q]

        self.O = O

        return self

    def get_observers(self):
        return self.O

    def predict(self, X, x=5, O=None):

        [m, n] = X.shape

        if O is None:
            O = self.O

        chunksize = self.chunksize
        if chunksize is None:
            chunksize = m

        y = np.zeros(m)
        for i in range(0, m, chunksize):
            dist = distance.cdist(X[i:(i + chunksize)], O)
            dist_sorted = np.sort(dist, axis=1)
            y[i:(i + chunksize)] = np.median(dist_sorted[:, 0:x], axis=1)

        return y

    def fit_predict(self, X, x=None, O=None):

        if O is None:
            O = self.O

        if x is None:
            x = self.x

        self.fit(X)
        return self.predict(X, x, O)


class SDOclust:

    def __init__(self, x=5, qv=0.3, hbs=False, smooth=False, smooth_f=0.25, rseed=5, zeta=0.6, chi_min=8, chi_prop=0.05,
                 e=3, chi=None, cb_outlierness=False, xc=None, k=None, q=None, chunksize=None):
        self.x = x
        self.qv = qv
        self.hbs = hbs
        self.smooth = smooth
        self.smooth_f = smooth_f
        self.rseed = rseed
        self.zeta = zeta
        self.chi_min = chi_min
        self.chi_prop = chi_prop
        self.e = e
        self.chi = chi
        self.cb_outlierness = cb_outlierness
        self.xc = xc
        self.k = k
        self.q = q
        self.chunksize = chunksize
        self.O = None
        self.ol = None
        self.kmp = None
        self.sdo = None

        if xc is None:
            self.xc = x

    def fit(self, X):

        sdo = SDO(self.x, self.qv, self.hbs, self.smooth, self.smooth_f, self.rseed, self.k, self.q, self.chunksize)
        sdo = sdo.fit(X)
        O = sdo.get_observers()

        ol = graph_clust(O, self.zeta, self.chi, self.chi_min, self.chi_prop)

        ind, count = np.unique(ol, return_counts=True)
        toremove = np.zeros(len(O))
        for i in ind:
            if count[i] <= self.e:
                toremove[ol == i] = 1

        O = O[toremove == 0, :]
        ol = ol[toremove == 0]

        nl = np.copy(ol)
        for i, l in enumerate(np.unique(ol)):
            nl[ol == l] = i
        ol = nl

        self.O, self.ol = O, ol
        self.kmp = O.shape[0] / X.shape[0]
        self.sdo = sdo

        return self

    def predict(self, X, return_membership=False, xc=None):

        if xc is None:
            xc = self.xc

        m, c = extend_labels(X, self.O, self.ol, self.xc)

        if return_membership:
            return c, m
        else:
            return c

    def fit_predict(self, X, return_membership=False, xc=None):

        self.fit(X)
        return self.predict(X, return_membership=return_membership, xc=xc)

    def get_observers(self):
        return self.O

    def outlierness(self, X, x=None):

        if x is None:
            x = self.x

        return self.sdo.predict(X, x)

    def update(self, X):

        k = self.O.shape[0]
        [m, n] = X.shape
        k_new_obs = np.max([1, int(m * self.kmp)])
        k_excess = k + k_new_obs

        index = np.random.permutation(m)
        newO = X[index[0:k_new_obs]]

        O = np.concatenate((self.O, newO), axis=0)

        P = np.zeros(k_excess)

        chunksize = self.chunksize
        if chunksize is None:
            chunksize = m

        for i in range(0, m, chunksize):
            dist = distance.cdist(X[i:(i + chunksize)], O)
            dist_sorted = np.argsort(dist, axis=1)
            closest = dist_sorted[:, 0:self.x].flatten()

            P += np.count_nonzero(closest[:, np.newaxis] == np.arange(k_excess), 0)

        toremove = np.argsort(P)[:k_new_obs]
        O = np.delete(O, toremove, axis=0)
        P = np.delete(P, toremove)

        ol = graph_clust(O, self.zeta, self.chi, self.chi_min, self.chi_prop)

        self.O, self.ol = O, ol

        return self

    def update_predict(self, X, return_membership=False, xc=None):

        self.update(X)
        return self.predict(X, return_membership=return_membership, xc=xc)
