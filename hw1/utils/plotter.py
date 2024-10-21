"""
File: plotter.py
Project: ExpertSystemHW
Author: staticowl
Created: 20-10-2024
Description: Plotting utility for visualizing best distances over generations in a genetic algorithm.
"""

import matplotlib.pyplot as plt

from hw1.utils.data_handler import generate_city_coordinates


def plot_best_distances(best_distances, num_cities, show_legend=True):
    """Plot the best distances over generations.

    Parameters:
        best_distances (list): List of best distances at each generation.
        generation (int): Current generation number for labeling.
        show_legend (bool): Whether to show the legend in the plot.
    """
    plt.figure(figsize=(30, 24))

    plt.plot(best_distances, marker='o', linestyle='-', color='b', markersize=2, markerfacecolor='red',
             label='Best Distance')
    plt.title('Best Tour Distance Over Generations')
    plt.xlabel('Generation')
    plt.ylabel('Best Distance')
    plt.grid()

    plt.title(f'Best Tour Distance Over Generations ({num_cities} cities)')

    if show_legend:
        plt.legend()

    plt.pause(0.01)  # Pause to update the plot interactively


def plot_best_path(best_tour, distance_matrix, show_legend=True):
    """Plot the best path between cities."""
    plt.figure(figsize=(30, 24))

    city_coordinates = generate_city_coordinates(distance_matrix)

    # Unpack city coordinates
    x = city_coordinates[:, 0]
    y = city_coordinates[:, 1]

    # Plot the path
    for i in range(len(best_tour)):
        start_city = best_tour[i]
        end_city = best_tour[(i + 1) % len(best_tour)]
        plt.plot([x[start_city], x[end_city]], [y[start_city], y[end_city]], color='blue', linewidth=1,
                 label='Path' if i == 0 else "")

    plt.scatter(x, y, color='red', marker='o', s=50, label='Cities')
    for i, (cx, cy) in enumerate(zip(x, y)):
        plt.text(cx, cy, str(i), fontsize=12, ha='right')

    plt.title('Best Path Between Cities')
    plt.xlabel('X Coordinate')
    plt.ylabel('Y Coordinate')
    if show_legend:
        plt.legend()

    plt.pause(0.01)


def finalize_plot():
    """Finalizes the plot display."""
    plt.ioff()
    plt.show()
