# source file with all necessary functions for repeated and iterated local search
from random import sample
from copy import copy


def random_solution(dimension):
    rsolution = range(dimension)
    return sample(rsolution)


def perturbation(current_solution, dim, percent):
    """
    randomly pertrubate current solution
    :param current_solution: list with current solution
    :param dim: dimension of our solution
    :param percent: per cent of shaked elements
    :return: new_solution - new perturbated solution
    """

    if percent > 1:
        percent = 1
    if percent < 0:
        percent = 0

    sample_len = dim*percent
    if sample_len % 2 != 0:
        sample_len -= 1

    new_solution = copy(current_solution)
    samp = sample(range(sample_len), sample_len)
    for i in range(0, sample_len, 2):
        new_solution[samp[i]], new_solution[samp[i + 1]] = new_solution[samp[i + 1]], new_solution[samp[i]]
    return new_solution


def two_opt(current_solution):
    return


def local_search(start_solution, mdest, mflow):
    return


def iterated_local_search(dim, mdest, mflow):
    return


def repeated_local_search(dim, mdest, mflow):
    return
