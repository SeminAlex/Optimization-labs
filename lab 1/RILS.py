# source file with all necessary functions for repeated and iterated local search
from random import sample, random
from copy import copy
import numpy as np


class Feature:
    __slots__ = ["city", "fabric", "penalty"]

    def __init__(self, city=0, fabric=0, penalty=0, utility=0, exists=False, cost=0):
        self.city = city
        self.fabric = fabric
        self.penalty = penalty
        self.utility = utility
        self.exists = exists
        self.cost = cost


class QAP:
    __slots__ = ["dimension", "mdist", "mflow", "best", "best_objective", "current"]

    def __init__(self, dimension=0, mdist=list(), mflow=list()):
        self.dimension = dimension
        self.mdist = mdist
        self.mflow = mflow
        self.best = list()
        self.current = list()
        self.best_objective = float("inf")
        return

    def objective_function(self, solution, penalties=None, lamb=None):
        """
        Calculate value of objective function for given solution solution
        :return: 
        """
        summ = 0
        for i in range(self.dimension):
            for j in range(self.dimension):
                summ += self.mdist[i][j] * self.mflow[solution[i]][solution[j]]
                if penalties is not None:
                    if solution[i] == j:
                        summ += lamb * penalties[i][j]
        return summ

    def random_solution(self):
        """
        Generate random solution
        :return: 
        """
        rsolution = range(self.dimension)
        return sample(rsolution, self.dimension)

    def perturbation(self, solution, percent=0.2):
        """
        randomly pertrubate given solution
        :param solution: list with current solution
        :param percent: per cent of shaked elements
        :return: new_solution - list with new perturbated solution
        """

        if percent > 1.:
            percent = 1.
        if percent < 0.:
            percent = 0.

        sample_len = int(self.dimension * percent)
        if sample_len % 2 != 0:
            sample_len -= 1

        new_solution = copy(solution)
        samp = [int(random() * self.dimension) for i in range(sample_len)]

        for i in range(0, sample_len, 2):
            new_solution[samp[i]], new_solution[samp[i + 1]] = new_solution[samp[i + 1]], new_solution[samp[i]]
        return new_solution

    def calculate_importance(self, location):
        """
        Calculate impact in objective function fabric located in 'location'
        :param location: number of location which importance will be calculated
        :return: 
        """
        summ = 0
        for i in range(self.dimension):
            if i != location:
                summ += self.mdist[location][i] * self.mflow[self.current[location]][self.current[i]]
                summ += self.mdist[i][location] * self.mflow[self.current[i]][self.current[location]]
        return summ

    def two_opt(self, solution):
        """
        Find by 2-opt strategy first food impacted move for current solution
        :param solution: given current solution
        :return: 2 params: first - new value of objective function
                           second - move to achieve new solution 
        """
        initial = self.objective_function(solution)
        for i in range(self.dimension):
            for j in range(self.dimension):
                solution[i], solution[j] = solution[j], solution[i]
                objective = self.objective_function()
                if objective < initial:
                    solution[i], solution[j] = solution[j], solution[i]
                    return objective, [i, j]
        return initial, []

    def parse_file(self, filename):
        with open(filename, "r") as f:
            lines = f.readlines()
        self.dimension = int(lines[0])
        self.mflow = [[]] * self.dimension
        self.mdist = [[]] * self.dimension
        for i in range(self.dimension):
            self.mdist[i] = [int(dist) for dist in lines[i + 1].split()]
            self.mflow[i] = [int(flow) for flow in lines[i + self.dimension + 2].split()]
        return self.dimension, self.mdist, self.mflow

    def two_opt_max(self, solution, penalties=None, lamb=None):
        """
        Find maximum impacted move according to 2opt neighbourhood strategy
        :return best: best impact on objective function
        :return move: move that has been achieved
        """
        best = self.objective_function(solution, penalties, lamb)
        move = list()

        for i in range(self.dimension):
            for j in range(i + 1, self.dimension):
                # make move
                solution[i], solution[j] = solution[j], solution[i]
                objective = self.objective_function(solution, penalties, lamb)
                if objective < best:
                    best = objective
                    move = [i, j]
                # return solution to the previous state
                solution[i], solution[j] = solution[j], solution[i]

        return best, move

    def local_search(self, initial_sol, penalties=None, lamb=None):
        """
        Local search heuristic for self.CURRENT initial solution
        :return: 
        """
        best_sol = copy(initial_sol)
        best_obj = self.objective_function(best_sol, penalties, lamb)

        while True:
            current_obj, move = self.two_opt_max(initial_sol, penalties, lamb)
            if current_obj >= best_obj:
                return best_obj, best_sol

            # make move and store the result
            initial_sol[move[0]], initial_sol[move[1]] = \
                initial_sol[move[1]], initial_sol[move[0]]
            best_obj = current_obj
            best_sol = copy(initial_sol)

        return  # unreachable part of code, but I need understand where function is over :)

    def iterated_local_search(self, iteration):
        current = self.random_solution()
        best = self.objective_function(copy(current))
        persent = 0.2
        count = 0
        for i in range(iteration):
            current = self.perturbation(current, persent)
            objective, solution = self.local_search(current)
            if objective < best:
                best = objective
                self.best = copy(solution)
                self.best_objective = best
                count = 0
                print("Iterated Local Search:")
                print("Iteration: ", i)
                print("Best objective: ", objective)
            else:
                count += 1
                if count > iteration * 0.4:
                    persent += 0.2
                    print("Persent is increased", persent)
        return self.best_objective, self.best

    def repeated_local_search(self, iteration):
        for i in range(iteration):
            current = self.random_solution()
            objective, solution = self.local_search(current)
            if objective < self.best_objective:
                self.best_objective = objective
                self.best = copy(solution)
                print("Repeated Local Search:")
                print("Iteration: ", i)
                print("Best objective: ", objective)

        return self.best_objective, self.best

    def calculate_feature_cost(self, city, fabric, solution):
        cost = 0
        for j in range(len(solution)):
            cost += self.mflow[fabric][solution[j]] * self.mdist[city][j]
            cost += self.mflow[solution[j]][fabric] * self.mdist[j][city]
        return cost

    def calculate_utility(self, penalties, solution):
        utility = [[0] * self.dimension for i in range(self.dimension)]
        for i in range(self.dimension):
            for j in range(self.dimension):
                utility[i][j] = self.calculate_feature_cost(i, j, solution) / (1 + penalties[i][j])
        return utility

    def update_penalty(self, utility, penalties):
        indices = (np.argwhere(np.amax(utility) == utility))
        for i in (indices):
            penalties[i[0]][i[1]] += 1
        return penalties

    def guided_local_search(self, iterations, lamb):
        penalties = [[0] * self.dimension for i in range(self.dimension)]
        current_solution = self.random_solution()
        current_best_obj = self.objective_function(current_solution)
        new_solution = copy(current_solution)
        for i in range(iterations):
            new_obj, new_solution = self.local_search(new_solution, penalties, lamb)
            current_obj = self.objective_function(new_solution)
            if current_obj < current_best_obj:
                current_solution = copy(new_solution)
                current_best_obj = current_obj
            penalties = self.update_penalty(self.calculate_utility(penalties, new_solution), penalties)

        return current_best_obj, current_solution


qap = QAP()
qap.parse_file("instances/tai20a")
# print (qap.objective_function([5, 8, 11, 6, 10, 0, 4, 12, 7, 9, 3, 18, 15, 2, 13, 1, 17, 19, 16, 14]))
ob, sol = qap.guided_local_search(1000, 100)
print("objective function: ", ob)
print("solution:")
print(sol)
print("\n\n")
