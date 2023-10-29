import numpy as np
import matplotlib.pyplot as plt
from scipy.special import rel_entr



# # generate a normal distribution with mean and std
def normal_distribution(mean, std, size):
    return np.random.normal(mean, std, size)


normal = normal_distribution(100, 1, 10000)
print(normal)
mean = 0
std = 1


def plot(data, mean, std):
    count, bins, ignored = plt.hist(data, 30, density=True)
    plt.plot(bins, 1 / (std * np.sqrt(2 * np.pi)) *
             np.exp(- (bins - mean) ** 2 / (2 * std ** 2)),
             linewidth=2, color='r')
    plt.show()


# plot the distribution
plot(normal, mean, std)

normal2 = normal_distribution(100, 1, 10000)
plot(normal2, 10, 5)


def kl_divergence(a, b):
    return sum(a[i] * np.log(a[i] / b[i]) for i in range(len(a)))


print(kl_divergence(normal, normal2))

print('KL-divergence(box_1 || box_2): %.3f ' % sum(rel_entr(normal, normal2)))


