from typing import Callable, Optional, Tuple, Union

import numpy as np
from sklearn.metrics import pairwise_distances
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import connected_components
from sklearn.base import BaseEstimator, ClusterMixin


def _check_matrix(a: np.ndarray) -> bool:
    return a.ndim == 2


def _check_matrix_is_square(a: np.ndarray) -> bool:
    M, N = a.shape
    return M == N


def _check_square_matrix_is_symmetric(a: np.ndarray) -> bool:
    return np.allclose(a, a.T)


def check_symmetric(a: np.ndarray) -> bool:
    if not _check_matrix(a):
        return False

    if not _check_matrix_is_square(a):
        return False

    if not _check_square_matrix_is_symmetric(a):
        return False

    return True


def _check_binary(a: np.ndarray) -> bool:
    return ((a == 0) | (a == 1)).all()


def check_adjacency_matrix(a: np.ndarray) -> bool:
    if not check_symmetric(a):
        return False

    if not _check_binary(a):
        return False

    # nonzero diagonal - graph with loops
    if np.any(np.diag(a)):
        return False

    return True


def _pairwise_distances(
        X: np.ndarray,
        metric: Union[str, Callable] = "euclidean",
        n_jobs: Optional[int] = None,
) -> np.ndarray:
    assert _check_matrix(X)

    distances = pairwise_distances(X=X, metric=metric, n_jobs=n_jobs)

    return distances


def distances_to_adjacency_matrix(
        distances: np.ndarray,
        threshold: float,
) -> np.ndarray:
    assert check_symmetric(distances)

    N = distances.shape[0]

    adjacency_matrix = (distances < threshold[:, None]).astype(int) - np.eye(N, dtype=int)
    adjacency_matrix_fd = np.rot90(np.fliplr(adjacency_matrix))
    adjacency_matrix = np.logical_and(adjacency_matrix, adjacency_matrix_fd).astype(int)

    return adjacency_matrix


class ConnectedComponentsClustering(ClusterMixin, BaseEstimator):

    def __init__(
            self,
            zeta: float,
            chi: int,
            chi_min: int,
            chi_prop: float,
            metric: Union[str, Callable] = "euclidean",
            n_jobs: Optional[int] = None,
    ) -> None:
        self.threshold = 0
        self.zeta = zeta
        self.chi = chi
        self.chi_min = chi_min
        self.chi_prop = chi_prop
        self.metric = metric
        self.n_jobs = n_jobs

    def fit(self, X: np.ndarray):
        X = self._validate_data(X, accept_sparse="csr")

        distances = _pairwise_distances(
            X=X,
            metric=self.metric,
            n_jobs=self.n_jobs,
        )

        [m, n] = distances.shape
        dist_sorted = np.sort(distances, axis=1)

        chi = self.chi
        if chi is None:
            chi = np.max([int(m * self.chi_prop), self.chi_min])

        aux = dist_sorted[:, chi]
        mean_aux = np.mean(aux)
        self.threshold = self.zeta * aux + (1 - self.zeta) * mean_aux

        adjacency_matrix = distances_to_adjacency_matrix(
            distances=distances,
            threshold=self.threshold,
        )

        graph = csr_matrix(adjacency_matrix)

        _, labels = connected_components(
            csgraph=graph,
            directed=False,
            return_labels=True,
        )

        self.labels_ = labels

        return self

    def fit_predict(
            self,
            X: np.ndarray,
    ):
        self.fit(X)
        return self.labels_
