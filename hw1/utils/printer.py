"""
File: printer.py
Project: ExpertSystemHW
Author: staticowl
Created: 20-10-2024
Description: write_a_description
"""


def print_matrix(dists, noout=False):
    if noout:
        return
    for row in dists:
        print(' '.join(f"{int(n):3d}" for n in row))
    print('')
