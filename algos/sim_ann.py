"""
File: sim_ann.py
Author: Koustav Mallick
Date: 27/10/2024

Description: [Add a brief description of the file here]
"""

import numpy as np
import sys

from utils.data_handler import data_handler
from utils.plotter import plot_best_distances, plot_best_path, finalize_plot
import math

def distance(path, distance_matrix):
    return sum(distance_matrix[path[i], path[(i+1)%len(path)]] for i in range(len(path)))

def generate_neighbour(path):
    new_path = path.copy()
    i, j = np.random.choice(len(path), 2, replace=False)
    new_path[i], new_path[j] = new_path[j], new_path[i]
    return new_path

def adaptive_temperature(initial_temp, final_temp, current_iteration, max_iterations):
    """
    Calculate the temperature based on the current iteration using an exponential decay.
    
    Parameters:
        initial_temp (float): Starting temperature.
        final_temp (float): Ending temperature.
        current_iteration (int): Current iteration.
        max_iterations (int): Maximum number of iterations.
        
    Returns:
        float: Adaptively calculated temperature.
    """
    return final_temp + (initial_temp - final_temp) * np.exp(-5 * current_iteration / max_iterations)

def sim_ann(distance_matrix, args):
    """
    Run the Simulated Annealing algorithm for the TSP.
    
    Parameters:
        distance_matrix (array_like): Distance matrix between cities.
        max_iterations (int): Total iterations for annealing.
        initial_temp (float): Starting temperature.
        final_temp (float): Ending temperature.
        alpha (float): Temperature decay rate.
        
    Returns:
        tuple: Best tour cost and the tour path.
    """
    max_iterations, initial_temp, final_temp = args.num_gen, args.init_temp, args.fin_temp
    num_cities = len(distance_matrix)
    current_path = np.arange(num_cities)
    np.random.shuffle(current_path)
    current_distance = distance(current_path, distance_matrix)
    best_path = current_path.copy()
    best_distance = current_distance
    temperature = initial_temp

    best_distances = []

    for iteration in range(max_iterations):
        new_path = generate_neighbour(current_path)
        new_distance = distance(new_path, distance_matrix)
        delta_distance = new_distance - current_distance
        
        if delta_distance < 0 or np.exp(-delta_distance / temperature) > np.random.rand():
            current_path = new_path
            current_distance = new_distance
        
        if current_distance < best_distance:
            best_distance = current_distance
            best_path = current_path
        best_distances.append(best_distance)
        temperature = adaptive_temperature(initial_temp, final_temp, iteration, max_iterations)

    plot_best_distances(best_distances, num_cities, args, show_legend=False)

    finalize_plot()
    
    return math.ceil(best_distance), best_path
    pass

def main():
    distance_matrix = data_handler(input_data)
    num_cities = len(distance_matrix)

    # Solve TSP using Simulated Annealing
    best_path, best_distance, best_distances = sim_ann(distance_matrix, num_cities)

    # Finalize best distance plot
    finalize_plot()
    print("Best path distance found:", best_distance)

    # Plot the best path
    # plot_best_path(best_path, distance_matrix)
    finalize_plot()
    pass

if __name__ == '__main__':
    input_data = sys.argv[1] if len(sys.argv) > 1 else "100"  # Default to 100 cities
    main(input_data)
    main()

