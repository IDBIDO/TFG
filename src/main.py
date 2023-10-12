import numpy as np
import matplotlib.pyplot as plt

import curses_test

mu = 5.0
sigma = 0.5
num_samples = 1000

# generate random values from normal distribution
random_values = np.random.normal(mu, sigma, num_samples)

print(random_values)

# Create a histogram of the random values
plt.hist(random_values, bins=30, density=True, alpha=0.5, color='b', label='Random Values')

# Plot the probability density function (PDF) of the normal distribution
x = np.linspace(mu - mu * sigma, mu + mu * sigma, 100)
pdf = (1 / (sigma * np.sqrt(2 * np.pi))) * np.exp(-(x - mu) ** 2 / (2 * sigma ** 2))
plt.plot(x, pdf, 'r', linewidth=2, label='Normal Distribution PDF')

# Add labels and a legend
plt.xlabel('Value')
plt.ylabel('Probability Density')
plt.title('Normal Distribution')
plt.legend()

# Show the plot
plt.show()


# Define a function with keyword parameters
def greet(name, *, greeting="Hello"):
    print(f"{greeting}, {name}!")


# Call the function with keyword arguments
greet(name="Alice", greeting="Hi")  # Using keyword arguments


def f(a, *, b):
    return a, b
print(f(1, b=2))

print(globals())