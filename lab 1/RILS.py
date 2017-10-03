# source file with all necessary functions for repeated and iterated local search
from random import sample
from copy import copy


class QAP:
    __slots__ = ["dimension", "mdist", "mflow", "best", "best_objective", "current"]

    def __init__(self, dimension=0, mdist=list(), mflow=list()):
        self.dimension = dimension
        self.mdist = mdist
        self.mflow = mflow
        self.best = list()
        self.current = list()
        self.best_objective = 9
        return

    def objective_function(self):
        """
        Calculate value of objective function for CURRENT solution
        :return: 
        """
        summ = 0
        for i in range(self.dimension):
            summ += self.calculate_importance(i)
        return summ

    def random_solution(self):
        """
        Generate random solution
        :return: 
        """
        rsolution = range(self.dimension)
        return sample(rsolution)

    def perturbation(self, percent):
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

        sample_len = self.dimension * percent
        if sample_len % 2 != 0:
            sample_len -= 1

        new_solution = copy(self.current)
        samp = sample(range(sample_len), sample_len)
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
                summ += self.mdist[location][i] * self.mflow[self.current[i]][self.current[location]]
        return summ

    def two_opt(self, first, second):
        return

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

    def two_opt_max(self):
        """
        Find maximum impacted move according to 2opt neighbourhood
        :return best: best impact on objective function
        :return move: move that achieve
        """
        best = 1
        move = list()
        for i in range(self.dimension):
            impact_i = -self.calculate_importance(i)
            for j in range(self.dimension):
                impact_j = self.calculate_importance(j)

                self.current[i], self.current[j] = self.current[j], self.current[i]
                impact_i += self.calculate_importance(j)
                impact_j += self.calculate_importance(i)
                impact = impact_i + impact_j
                if impact < best:
                    best = impact
                    move = [i, j]

                self.current[i], self.current[j] = self.current[j], self.current[i]

        return best, move

    def local_search(self):
        best_obj = self.objective_function()
        current_obj = best_obj

        while True:
            imp, move = self.two_opt_max()
            if imp >= 0:
                self.best_objective = current_obj
                self.best = self.current
                return
            self.current[move[0]], self.current[move[1]] = \
                self.current[move[1]], self.current[move[0]]

        return

    def iterated_local_search(self):
        return

    def repeated_local_search(self):
        return
