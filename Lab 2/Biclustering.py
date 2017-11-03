from collections import Counter
from random import sample

from numpy.matlib import rand, random


class BiCl:
    __slots__ = ["m", "p", "matrix", "machines", "parts", "max_cluster", "ones_all", "ones", "zeros"]

    def __init__(self, m, p, matrix=list(), ones_n=0):
        self.m = m
        self.p = p
        self.matrix = matrix  # boolean matrix. It allow us to get fast access to element
        self.machines = list()
        self.parts = list()
        self.ones_all = ones_n
        self.ones = ones_n
        self.zeros = ones_n

    def parse_file(self, filename):
        with open(filename, "r") as f:
            lines = f.readlines()
        self.ones_all = 0
        self.m, self.p = int(lines[0].split()[0]), int(lines[0].split()[1])
        self.matrix = [[0] * self.p for i in range(self.m)]
        for i in range(1, len(lines) - 1):
            self.ones_all += len(lines[i].split()[1:])
            for j in lines[i].split()[1:]:
                self.matrix[i][int(j) - 1] = 1
        return self.matrix

    def objective_function(self):
        one_in = 0
        zero_in = 0
        for cluster in range(self.max_cluster):
            for mach in range(self.m):
                if self.machines[mach] == cluster:
                    for part in range(self.p):
                        if self.parts[part] == cluster:
                            if self.matrix[mach].count(part) != 0:
                                one_in += 1
                            else:
                                zero_in += 1
        return one_in / (self.ones_n + zero_in)

    def delta_col(self, index, cluster):
        """
        Calculate impact on objective function if machines with index 'index' will be moved to cluster 'cluster'  
        :param index: index of machine
        :param cluster: new cluster for this machine
        :return: difference in 'ones in cluster' and 'zeroes out cluster' 
        """
        current = self.machines[index]
        summ = 0
        zeroes = 0
        for pindx in range(self.p):
            if self.parts[pindx] == cluster:
                summ += self.matrix[index][pindx]
                zeroes += not self.matrix[index][pindx]
            if self.parts[pindx] == current:
                summ -= self.matrix[index][pindx]
                zeroes -= not self.matrix[index][pindx]
        return summ, zeroes

    def delta_row(self, index, cluster):
        '''
        Calculate impact on objective function if part with index 'index' will be moved to cluster 'cluster'  
        :param index: index of part
        :param cluster: new cluster for this part
        :return: difference in 'ones in cluster' and 'zeroes out cluster' 
        '''
        current = self.parts[index]
        summ = 0
        zeroes = 0
        for mindx in range(self.m):
            if self.machines[mindx] == cluster:
                summ += self.matrix[mindx][index]
                zeroes += not self.matrix[mindx][index]
            if self.parts[mindx] == current:
                summ += self.matrix[mindx][index]
                zeroes += not self.matrix[mindx][index]
        return summ, zeroes

    def row_add(self):
        for i in range(self.m):
            for j in range(self.p):
                return
        return

    ############################################
    ############NEIGHBOURHOOD SECTION###########
    ############################################

    def devide_cluster(self, candidate):
        '''
        devides cluster into 2 separate clusters
        :param candidate: cluster to devide
        :return:
        '''
        m_indices, p_indices = self.get_cluster_indices(candidate)
        m_l = int(len(m_indices) / 2)
        for i in m_indices[:m_l]:
            self.machines = max(self.machines) + 1
        p_l = int(len(p_indices) / 2)
        for i in p_indices[:p_l]:
            self.parts = max(self.parts) + 1

    def get_cluster_indices(self, candidate):
        """
        :param candidate:
        :return: cluster indices
        """
        m_indices = [i for i, x in enumerate(self.machines) if x == candidate]
        p_indices = [i for i, x in enumerate(self.machines) if x == candidate]
        return m_indices, p_indices

    def division_neighbourhood(self):
        '''
        neigborhood of cluster division
        :return:
        '''
        m_c = Counter(self.machines)
        p_c = Counter(self.parts)
        clusters = list[m_c.keys()]
        candidates = []
        for i in clusters:
            if m_c[i] > 1 and p_c[i] > 1:
                candidates.append(i)
        if len(candidates) != 0:
            candidate = sample(candidates, 1)
            self.devide_cluster(candidate)

    def calculate_cluster(self):
        """
        clculates the number of ones and zeros in each cluster
        :return: dict, where key - cluster number and value - [x,y], where x - number of zeros and y - number of ones
        """
        max_impact_cluster = 0
        cluster_dict = dict.fromkeys(set(self.machines),[0,0])
        for candidate in cluster_dict.keys():
            m_indices, p_indices = self.get_cluster_indices(candidate)
            for i in m_indices:
                for j in p_indices:
                if self.matrix[i,j] == 0:
                    cluster_dict[candidate][0] += 1
                else:
                    cluster_dict[candidate][1] += 1
        return cluster_dict
        """
        maxd = 0
        for cl in cluster_dict.keys():
            maxd = cluster_dict[cl][1]/cluster_dict[cl][1]
            if
        """


    def pertrubation_neighbourhood(self):
        pass











    ############################################
    ############NEIGHBOURHOOD SECTION###########
    ############################################

    def cluster_check(self):
        for cluster in set(self.parts + self.machines):
            if cluster not in self.machines:
                # find parts that allocated on "cluster"
                for i in [j for j, x in enumerate(self.parts) if x == cluster]:
                    # try to move this part into other cluster
                    diff = float('inf')
                    for cl in set(self.machines):
                        ones, zeros = self.delta_row(i, cl)
                        if float(zeros) < float(ones) / self.function:
                            self.function = float(ones) / float(self.ones_n + zeros)
                            # TODO: think about objective function

        return

    def move_row(self):
        """
        Find row and best cluster for this row in current solution
        
        :return: (index of row, best cluster number, number of ones in clusters in new solution, number of zeros in 
        clusters in new solution)
        """
        objective = self.ones / (self.ones_all + self.zeros)
        result = ()
        for cluster in set(self.machines):
            for machine in range(self.m):
                if self.machines[machine] != cluster:
                    ones, zeros = self.delta_col(machine, cluster)
                    new = self.ones+ones / (self.ones_all + self.zeros + zeros)
                    if new > objective:
                        objective = new
                        result = (machine, cluster, self.ones + ones, self.zeros + zeros)

        return result

    def swap_row(self):
        """
        Find two rows which cluster swap get max impact on objective function

        :return: (index of fist row, index of second row, number of ones in clusters in new solution, number of zeros in 
        clusters in new solution)
        """
        objective = self.ones / (self.ones_all + self.zeros)
        result = ()
        for cluster in set(self.machines):
            for machine in range(self.m):
                fones, fzeros = self.delta_col(machine, cluster)
                for oponent in range(self.m):
                    if self.machines[oponent] != cluster and machine != oponent:
                        opones, opzeros = self.delta_col(oponent, cluster)
                        new = self.ones + fones + opones
                        new /= self.ones_all + self.zeros + fzeros + opzeros
                        if new > objective:
                            objective = new
                            result = (machine, oponent, self.ones + fones + opones, self.zeros+fzeros+opzeros)
        return result

    def move_col(self):
        """
        Find column and best cluster for him in current solution
        
        :return: (index of column, best cluster number, number of ones in clusters in new solution, number of zeros in 
        clusters in new solution)
        """
        objective = self.ones / (self.ones_all + self.zeros)
        result = ()
        for cluster in set(self.parts):
            for part in range(self.p):
                if self.parts[part] != cluster:
                    ones, zeros = self.delta_row(part, cluster)
                    new = self.ones + ones / (self.ones_all + self.zeros + zeros)
                    if new > objective:
                        objective = new
                        result = (part, cluster, self.ones + ones, self.zeros + zeros)
        return result

    def swap_col(self):
        """
        Find two columns which clusters swap get max impact on objective function
        
        :return: (index of fist column, index of second column, number of ones in clusters in new solution, 
        number of zeros in clusters in new solution) 
        """
        objective = self.ones / (self.ones_all + self.zeros)
        result = ()
        for cluster in set(self.parts):
            for part in range(self.p):
                fones, fzeros = self.delta_row(part, cluster)
                for oponent in range(self.m):
                    if self.machines[oponent] != cluster and part != oponent
                        opones, opzeros = self.delta_row(oponent, cluster)
                    new = self.ones + fones + opones
                    new /= self.ones_all + self.zeros + fzeros + opzeros
                    if new > objective:
                        objective = new
                        result = (part, oponent, self.ones+fones+opones, self.zeros+fzeros+opzeros)
        return result





bicl = BiCl(0, 0)
print(bicl.parse_file("instances/testinstance"))
