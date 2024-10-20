"""
File: main.py
Project: ExpertSystemHW
Author: staticowl
Created: 20-10-2024
Description: write_a_description
"""
import argparse
import time

import algos
from utils.data_handler import data_handler
from utils.printer import print_matrix


def parse_arguments():
    parser = argparse.ArgumentParser(description='Run TSP algorithms with different modes and settings.')
    parser.add_argument('--algo', default='ssga', choices=['ssga', 'aco'],
                        help='Genetic Algorithm to use for solving TSP')
    parser.add_argument('--input_size', default="input", type=str, help='Size of the input data')
    parser.add_argument('--num_gen', default=100, help='Number of generations')
    parser.add_argument('--pop_size', default=50, help='Population size')
    parser.add_argument('--noout', default=False, action='store_true', help='Do not print the output')
    return parser.parse_args()


def main(args=None):
    start_time = time.time()

    if args is None:
        print("You have to pass some arguments. Run 'python tsp.py --help' for more information.")

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
