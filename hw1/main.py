"""
File: main.py
Project: ExpertSystemHW
Author: staticowl
Created: 20-10-2024
Description: Main entry point for the Traveling Salesman Problem (TSP) solver.
             This script takes several command line arguments, allowing the user to
             select the genetic algorithm to use, the size of the input data, the
             number of generations, the population size, and whether to print the
             output.
"""

import argparse
import time

import algos
from utils.data_handler import data_handler
from utils.printer import print_matrix


def parse_arguments():
    """
    Parse command line arguments.

    Returns:
        argparse.Namespace: A namespace containing the parsed arguments.
    """
    parser = argparse.ArgumentParser(description='Run TSP algorithms with different modes and settings.')
    parser.add_argument('--algo', default='ssga', choices=['ssga', 'aco'],
                        help='Genetic Algorithm to use for solving TSP. Choices: ssga, aco.')
    parser.add_argument('--input_size', default="input", type=str,
                        help='Size of the input data. If "input", the user will be prompted to enter the input size.')
    parser.add_argument('--num_gen', default=100, type=int,
                        help='Number of generations.')
    parser.add_argument('--pop_size', default=50, type=int,
                        help='Population size.')
    parser.add_argument('--noout', default=False, action='store_true',
                        help='Do not print the output.')
    return parser.parse_args()


def main(args=None):
    """
    Main entry point.

    Parameters:
        args (argparse.Namespace): The parsed arguments. If None, the arguments will be parsed from sys.argv.
    """
    start_time = time.time()

    if args is None:
        print("You have to pass some arguments. Run 'python tsp.py --help' for more information.")
        return

    try:
        if args.input_size == "input":
            input_size = input("Please enter the input size: ")
            args.input_size = input_size
        dists = data_handler(args.input_size)
        print_matrix(dists, args.noout)
        print("Data Generation Time:", time.time() - start_time, "s")

        tsp_start_time = time.time()

        algo = getattr(algos, args.algo)

        cost, path = algo(dists, args.num_gen, args.pop_size, args.noout)

        print("TSP Time:", time.time() - tsp_start_time, "s")
        print("Cost:", cost)
        if not args.noout:
            print("Path:", path)
        print("Total Time:", time.time() - start_time, "s")
    except Exception as e:
        print(e)


if __name__ == '__main__':
    main(args=parse_arguments())