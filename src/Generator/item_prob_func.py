import numpy as np

prob_method = []


# decorator to add probability method to the list
def probability_method(prob_func):
    prob_method.append(prob_func)
    return prob_func


@probability_method
def get_zipf_probability_vector(n, alfa):
    # Create a list of elements from 1 to n
    elements = np.arange(1, n + 1)

    # Calculate the probabilities according to the Zipf law
    probabilities = 1 / np.power(elements, alfa)
    probabilities /= np.sum(probabilities)  # Normalize the probabilities so that they add up to 1

    # Generate the sequence
    # sequence = np.random.choice(elements, size=N, p=probabilities)
    return probabilities


@probability_method
def get_uniform_probability_vector(n):
    return np.ones(n) / n


