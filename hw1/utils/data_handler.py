"""
File: data_handler.py
Project: ExpertSystemHW
Author: staticowl
Created: 20-10-2024
Description: Utility functions for generating and reading distance matrices for the Traveling Salesman Problem.
"""

import sys

import numpy as np


def generate_distances(n, city_weights=None):
    """
    Generate a random distance matrix for a Traveling Salesman Problem with n cities.

    Parameters:
        n (int): The number of cities.
        city_weights (array_like, optional): The weights for each city. Defaults to all ones.

    Returns:
        array_like: A symmetric distance matrix as a Numpy array.
    """
    if city_weights is None:
        city_weights = np.ones(n)

    upper_indices = np.triu_indices(n, k=1)
    dists = np.zeros((n, n), dtype=int)

    weights = np.random.rand(len(upper_indices[0])) * city_weights[upper_indices[0]] * city_weights[upper_indices[1]]
    dists[upper_indices] = np.clip(np.random.randint(1, 100, size=len(upper_indices[0])) * weights, 1, 100).astype(int)
    dists += dists.T
    for i in range(n):
        for j in range(i + 1, n):
            noise = np.random.randint(-10, 11)
            dists[i, j] = max(1, dists[i, j] + noise)
            dists[j, i] = dists[i, j]

    return dists


def read_distances(filename):
    """
    Read a CSV file containing distance matrices for the Traveling Salesman Problem.
    
    Parameters:
        filename: The path to a CSV file containing the distance matrix.

    Returns:
        A Numpy array of the distances.
    """
    dists = []
    with open(filename, 'r') as file:
        for line in file:
            if line.strip() and not line.startswith('#'):
                # Split the line by comma, strip whitespace, convert to integers
                row = list(map(int, map(str.strip, line.split(','))))
                dists.append(row)
    return np.array(dists, dtype=np.float64)


def get_argv(index, default):
    """
    Get the argument at the given index from sys.argv, or return the default if not enough arguments are given.
    """
    if len(sys.argv) > index:
        return sys.argv[index]
    return default


def data_handler(input_data):
    """
    Handle the input data, either by reading a CSV file or generating a random distance matrix.

    Parameters:
        input_data (str): The input data, either a CSV file or the number of cities.

    Returns:
        array_like: A symmetric distance matrix as a Numpy array.
    """
    if input_data.endswith('.csv'):
        dists = np.array(read_distances(input_data), dtype=np.float64)
    else:
        n = int(input_data)
        dists = generate_distances(n)

    return dists