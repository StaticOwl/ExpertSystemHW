"""
File: ant_colony.py
Author: Koustav Mallick
Date: 12/8/2024
Description: Implementation of the Ant Colony Optimization (ACO) algorithm for solving the Traveling Salesman Problem (TSP).
"""

import numpy as np
from utils.plotter import plot_best_distances, finalize_plot
from utils.data_handler import data_handler



def initialize_pheromones(num_cities, initial_pheromone=1.0):
    """
    Initialize pheromone levels for the paths.
    Parameters:
        num_cities (int): Number of cities.
        initial_pheromone (float): Initial pheromone value.
    Returns:
        np.ndarray: Pheromone matrix.
    """
    return np.full((num_cities, num_cities), initial_pheromone)


def heuristic(distance_matrix):
    """
    Compute the heuristic information (e.g., inverse distance).
    Parameters:
        distance_matrix (np.ndarray): Matrix of distances between cities.
    Returns:
        np.ndarray: Heuristic matrix (1 / distance).
    """
    with np.errstate(divide='ignore'):  # Ignore division by zero warnings
        h = 1 / distance_matrix
        h[np.isinf(h)] = 0
    return h


def construct_solution(pheromone, heuristic_matrix, distance_matrix, alpha, beta, num_cities, num_ants):
    """
    Construct solutions using probabilistic transitions.
    Parameters:
        pheromone (np.ndarray): Pheromone matrix.
        heuristic_matrix (np.ndarray): Heuristic matrix.
        distance_matrix (np.ndarray): Distance matrix between cities.
        alpha (float): Pheromone importance.
        beta (float): Heuristic importance.
        num_cities (int): Number of cities.
        num_ants (int): Number of ants.
    Returns:
        list of np.ndarray: Paths taken by ants.
        list of float: Costs of paths.
    """
    solutions = []
    costs = []
    for i in range(num_ants):
        # print(f"Ant {i + 1}/{num_ants} is constructing a solution...")
        path = [np.random.randint(0, num_cities)]
        while len(path) < num_cities:
            current_city = path[-1]
            unvisited = [city for city in range(num_cities) if city not in path]
            probabilities = np.array([
                (pheromone[current_city][city] ** alpha) * (heuristic_matrix[current_city][city] ** beta)
                for city in unvisited
            ])
            probabilities /= probabilities.sum()
            next_city = np.random.choice(unvisited, p=probabilities)
            path.append(next_city)
        path_cost = sum(distance_matrix[path[i], path[(i + 1) % num_cities]] for i in range(num_cities))
        solutions.append(np.array(path))
        costs.append(path_cost)
    return solutions, costs



def update_pheromones(pheromone, solutions, costs, evaporation_rate, Q=1.0):
    """
    Update the pheromone levels based on the solutions found.
    Parameters:
        pheromone (np.ndarray): Pheromone matrix.
        solutions (list of np.ndarray): Paths taken by ants.
        costs (list of float): Costs of paths.
        evaporation_rate (float): Rate at which pheromone evaporates.
        Q (float): Constant controlling the amount of pheromone deposited.
    Returns:
        np.ndarray: Updated pheromone matrix.
    """
    pheromone *= (1 - evaporation_rate)
    for path, cost in zip(solutions, costs):
        for i in range(len(path)):
            pheromone[path[i], path[(i + 1) % len(path)]] += Q / cost
    return pheromone


def aco(distance_matrix, args):
    """
    Run the Ant Colony Optimization (ACO) algorithm.
    Parameters:
        distance_matrix (np.ndarray): Matrix of distances between cities.
        args (argparse.Namespace): Arguments containing parameters for ACO.
    Returns:
        float: Best path cost.
        np.ndarray: Best path.
    """
    num_cities = len(distance_matrix)
    pheromone = initialize_pheromones(num_cities)
    heuristic_matrix = heuristic(distance_matrix)

    best_cost = float('inf')
    best_path = None
    best_distances = []

    for iteration in range(args.num_gen):
        print(f"Iteration {iteration + 1}/{args.num_gen}")
        solutions, costs = construct_solution(pheromone, heuristic_matrix, distance_matrix,args.alpha, args.beta, num_cities, args.num_ants)
        pheromone = update_pheromones(pheromone, solutions, costs, args.evaporation_rate)

        iteration_best_cost = min(costs)
        iteration_best_path = solutions[np.argmin(costs)]

        if iteration_best_cost < best_cost:
            best_cost = iteration_best_cost
            best_path = iteration_best_path

        best_distances.append(best_cost)

    plot_best_distances(best_distances, num_cities, args)
    finalize_plot()

    return best_cost, best_path

# def main():
#     distance_matrix = data_handler(input_data)
#     num_cities = len(distance_matrix)

#     # Solve TSP using Simulated Annealing
#     best_path, best_distance = aco(distance_matrix, num_cities)

#     # Finalize best distance plot
#     finalize_plot()
#     print("Best path distance found:", best_distance)

#     # Plot the best path
#     # plot_best_path(best_path, distance_matrix)
#     finalize_plot()
#     pass

# if __name__ == '__main__':
#     import sys
#     input_data = sys.argv[1] if len(sys.argv) > 1 else "100"  # Default to 100 cities
#     main(input_data)
#     main()


