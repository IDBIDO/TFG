import numpy as np

distribution = []


# decorator to add distribution generator method to the list
def distribution_method(dist_func):
    distribution.append(dist_func)
    return dist_func


# normal
@distribution_method
def normal_distribution(mean, std, size):
    return np.random.normal(mean, std, size)


@distribution_method
def uniform_distribution(low, high, size):
    return np.random.uniform(low, high, size)


@distribution_method
def poisson_distribution(lam, size):
    return np.random.poisson(lam, size)


@distribution_method
def exponential_distribution(scale, size):
    return np.random.exponential(scale, size)

@distribution_method
def gamma_distribution(shape, scale, size):
    return np.random.gamma(shape, scale, size)
