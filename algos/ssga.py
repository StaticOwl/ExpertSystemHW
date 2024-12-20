"""
File: ssga.py
Project: ExpertSystemHW
Author: staticowl
Created: 20-10-2024
Description: Implementation of a genetic algorithm for solving the traveling-salesman problem.
"""

import math

import numpy as np

from utils.plotter import plot_best_distances, finalize_plot


def evaluate_fitness(tours, distance_matrix):
    """
    Evaluate fitness scores for a set of tours.
    
    Parameters:
        tours (array_like): Shape (num_tours, num_cities).
        distance_matrix (array_like): Shape (num_cities, num_cities).
    
    Returns:
        array_like: Fitness scores, shape (num_tours,).
    """
    distances = np.sum(distance_matrix[tours[:, :-1], tours[:, 1:]], axis=1)
    distances += distance_matrix[tours[:, -1], tours[:, 0]]
    return 1.0 / distances


def select_parents(population, fitness_scores, num_parents, percent_reduction = 4):
    """
    Select parents using diversified elitism.
    
    Parameters:
        population (array_like): Current population of tours.
        fitness_scores (array_like): Fitness scores of the population.
        num_parents (int): Number of parents to select.
        percent_reduction (int): Percent reduction in number of parents.
    Returns:
        array_like: Selected parents for crossover.
    """
    sorted_indices = np.argsort(fitness_scores)[::-1]
    elite_count = max(1, num_parents // percent_reduction)
    elites = population[sorted_indices[:elite_count]]

    diversity_count = num_parents - elite_count
    remaining_indices = np.random.choice(len(population), size=diversity_count, replace=False)
    diverse_parents = population[remaining_indices]
    return np.vstack((elites, diverse_parents))


def ordered_crossover(parent1, parent2):
    """
    Perform ordered crossover between two parents.
    
    Parameters:
        parent1, parent2 (array_like): Parent tours.
    
    Returns:
        array_like: A child tour.
    """
    size = len(parent1)
    child = [-1] * size
    start_idx, end_idx = sorted(np.random.randint(0, size, 2))
    child[start_idx:end_idx] = parent1[start_idx:end_idx]

    parent2_ptr = 0
    for i in range(size):
        if child[i] == -1:
            while parent2[parent2_ptr] in child:
                parent2_ptr += 1
            child[i] = parent2[parent2_ptr]

    return np.array(child)


def crossover(parents, num_children):
    """
    Generate children using ordered crossover.
    
    Parameters:
        parents (array_like): Selected parents for crossover.
        num_children (int): Number of children to generate.
    
    Returns:
        array_like: Generated children.
    """
    num_parents = len(parents)
    num_cities = parents.shape[1]
    children = np.zeros((num_children, num_cities), dtype=parents.dtype)

    for idx in range(num_children):
        parent1_idx = np.random.randint(0, num_parents)
        parent2_idx = np.random.randint(0, num_parents)
        children[idx] = ordered_crossover(parents[parent1_idx], parents[parent2_idx])

    return children


def mutate(children, mutation_prob):
    """
    Perform mutation on the children.
    
    Parameters:
        children (array_like): Children tours.
        mutation_prob (float): Probability of mutation.
    
    Returns:
        array_like: Mutated children.
    """
    num_children = children.shape[0]
    for idx in range(num_children):
        if np.random.rand() < mutation_prob:
            i, j = np.random.randint(0, children.shape[1], size=2)
            children[idx, i], children[idx, j] = children[idx, j], children[idx, i]
    return children


def adaptive_mutation_rate(generation, max_generations, mutation_seed=0.1):
    """
    Compute adaptive mutation rate.
    
    Parameters:
        generation (int): Current generation number.
        max_generations (int): Maximum number of generations.
        mutation_seed (float): Initial mutation rate.
    Returns:
        float: Mutation rate.
    """
    mutation = max(0.01, mutation_seed * (1 - generation / max_generations))
    print(f"Mutation Rate: {mutation}")
    return mutation


def ssga(distance_matrix, args):
    """
    Run the Steady-State Genetic Algorithm.
    
    Parameters:
        distance_matrix (array_like): Distance matrix between cities.
        num_generations (int): Number of generations to run the algorithm.
        population_size (int): Size of the population.
        mutation_seed (float): Initial mutation rate.
        percent_reduction (int): Percent reduction in number of parents.
        noout (bool): Whether to print the output or not.
    
    Returns:
        tuple: Best tour cost and the tour path.
    """
    num_generations, population_size, mutation_seed, percent_reduction = args.num_gen, args.pop_size, args.mutation_rate, args.parents_percent
    num_cities = distance_matrix.shape[0]
    population = np.array([np.random.permutation(num_cities) for _ in range(population_size)])
    best_distances = []

    for generation in range(num_generations):
        fitness_scores = evaluate_fitness(population, distance_matrix)
        parents = select_parents(population, fitness_scores, population_size // 2, percent_reduction)
        children = crossover(parents, population_size // 2)
        current_mutation_prob = adaptive_mutation_rate(generation, num_generations, mutation_seed)
        children = mutate(children, current_mutation_prob)
        population = np.concatenate([parents, children], axis=0)

        best_tour_idx = np.argmax(fitness_scores)
        best_distance = 1.0 / fitness_scores[best_tour_idx]
        best_distances.append(best_distance)

        # if not noout:
        #     print(
        #         f"Generation {generation + 1}, Best Distance: {math.ceil(best_distance)}, Mutation Rate: {current_mutation_prob:.4f}")

    best_tour_idx = np.argmax(fitness_scores)
    best_distance = 1.0 / fitness_scores[best_tour_idx]
    best_tour = population[best_tour_idx]

    plot_best_distances(best_distances, num_cities)

    finalize_plot()

    return math.ceil(best_distance), best_tour
