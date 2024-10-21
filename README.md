# Expert Systems Home Work

This repository contains the home work for the Expert Systems course.

# SSGA (hw1)

This is a Steady-State Genetic Algorithm for solving the Traveling Salesman Problem.

## Description

The SSGA is a genetic algorithm that uses a steady-state approach, where a portion of the population is replaced in each iteration. The algorithm starts with a random population and iteratively applies selection, crossover and mutation operators to generate new population. The algorithm stops when a maximum number of generations is reached.

## Credits

[@StaticOwl](https://www.github.com/StaticOwl)

## Current Status

The algorithm is currently able to solve the Traveling Salesman Problem for a given set of cities. The algorithm uses a diversified elitism selection method, ordered crossover and adaptive mutation rate. The algorithm is able to plot the best distances over the generations and the final best path.

## Sample Command

```bash
python main.py --noout --mutation_rate=0.01 --parents_percent=20 --input_size=2000 --pop_size=100
```