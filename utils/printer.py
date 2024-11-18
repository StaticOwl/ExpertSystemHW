"""
File: printer.py
Project: ExpertSystemHW
Author: staticowl
Created: 20-10-2024
Description: Utility functions for printing matrices and paths.
"""


def print_matrix(dists, noout=False):
    """
    Print a matrix of distances.

    Parameters:
        dists (array_like): A 2D array of distances.
        noout (bool, optional): If set, nothing is printed. Defaults to False.
    """
    if noout:
        return
    for row in dists:
        print(' '.join(f"{int(n):3d}" for n in row))
    print("")
