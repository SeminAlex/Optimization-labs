from collections import Counter
from copy import deepcopy as cp
from random import sample, choice, shuffle


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
        self.matrix = [[0] * self.p for _ in range(self.m)]
        for i in range(1, len(lines) - 1):
            self.ones_all += len(lines[i].split()[1:])
            for j in lines[i].split()[1:]:
                self.matrix[i][int(j) - 1] = 1
        return self.matrix

    def objective_function(self):
        one_in = 0
        zero_in = 0
        for machine in range(self.m):
            for part in range(self.p):
                if self.machines[machine] == self.parts[part]:
                    one_in += self.matrix[machine][part]
                    zero_in += not self.matrix[machine][part]
        return one_in / (self.ones_all + zero_in), one_in, zero_in

    def delta_col(self, index, cluster):
        """
        Calculate impact on objective function if machines with index 'index' will be moved to cluster 'cluster'
        :param index: index of machine
        :param cluster: new cluster for this machine
        :return: difference in 'ones in cluster' and 'zeroes in cluster'
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
        """
        Calculate impact on objective function if part with index 'index' will be moved to cluster 'cluster'
        :param index: index of part
        :param cluster: new cluster for this part
        :return: difference in 'ones in cluster' and 'zeroes in cluster'
        """
        current = self.parts[index]
        summ = 0
        zeroes = 0
        for mindx in range(self.m):
            if self.machines[mindx] == cluster:
                summ += self.matrix[mindx][index]
                zeroes += not self.matrix[mindx][index]
            if self.machines[mindx] == current:
                summ -= self.matrix[mindx][index]
                zeroes -= not self.matrix[mindx][index]
        return summ, zeroes

    def random_solution(self):
        max_cluster = min(self.m, self.p)
        available_clusters = list(range(max_cluster))
        self.machines = [choice(available_clusters) for _ in range(self.m)]
        self.parts = [choice(available_clusters) for _ in range(self.p)]
        _, self.ones, self.zeros = self.objective_function()
        self.cluster_check()
        return

    def write_to_file(self, filename):
        with open(filename, "w") as f:
            for cl in set(self.machines):
                for i in range(self.m):
                    if self.machines[i] == cl:
                        f.write(str(i) + ";;")
                        f.write(str(self.matrix[i]).replace("[","").replace("]","").replace(",",";") + "\n")




    #        ###########################################
    #        ########## NEIGHBORHOOD SECTION ###########
    #        ###########################################

    def neighbors(self, name=str()):
        name = name.lower()
        if name == "division":
            self.division_neighborhood()
            return
        elif name == "shuffle":
            self.shuffle_neighborhood()
            return
        elif name == "merge":
            self.merge_neighborhood()
            return
        elif name == "move_row":
            result = self.move_row()
            if result:
                index, cluster, self.ones, self.zeros = result
                self.machines[index] = cluster
                self.cluster_check()
            return
        elif name == "move_col":
            result = self.move_col()
            if result:
                index, cluster, self.ones, self.zeros = result
                self.parts[index] = cluster
                self.cluster_check()
            return
        elif name == "swap_row":
            result = self.swap_row()
            if result:
                fidx, sidx, self.ones, self.zeros = result
                self.machines[sidx], self.machines[fidx] = self.machines[fidx], self.machines[sidx]
            return
        elif name == "swap_col":
            result = self.swap_col()
            if result:
                fidx, sidx, self.ones, self.zeros = self.swap_col()
                self.parts[fidx], self.parts[sidx] = self.parts[sidx], self.parts[fidx]
            return
        else:
            raise "Error: There is no neighborhood with name '" + str(name) + "'\n"

    def divide_cluster(self, candidate):
        """
        Divides cluster into 2 separate clusters
        :param candidate: cluster to divide
        :return:
        """
        m_indices, p_indices = self.get_cluster_indices(candidate)
        m_l = int(len(m_indices) / 2)
        for _ in m_indices[:m_l]:
            self.machines = max(self.machines) + 1
        p_l = int(len(p_indices) / 2)
        for _ in p_indices[:p_l]:
            self.parts = max(self.parts) + 1
        return

    def get_cluster_indices(self, candidate):
        """
        :param candidate:
        :return: cluster indices
        """
        m_indices = [i for i, x in enumerate(self.machines) if x == candidate]
        p_indices = [i for i, x in enumerate(self.parts) if x == candidate]
        return m_indices, p_indices

    def division_neighborhood(self):
        """
        neigborhood of cluster division
        :return:
        """
        m_c = Counter(self.machines)
        p_c = Counter(self.parts)
        clusters = list(m_c.keys())
        candidates = []
        for i in clusters:
            if m_c[i] > 1 and p_c[i] > 1:
                candidates.append(i)
        if len(candidates) != 0:
            candidate = sample(candidates, 1)
            self.divide_cluster(candidate)
        self.calculate_neighbour_impact()
        return

    def calculate_cluster(self):
        """
        calculates the number of ones and zeros in each cluster
        :return: dict, where key - cluster number and value - [x,y], where x - number of zeros and y - number of ones
        """
        # cluster_dict = dict.fromkeys(set(self.machines), [[0, 0]]*self.m)
        cluster_dict = dict()
        for candidate in set(self.machines):
            cluster_dict[candidate] = [0, 0]
            m_indices, p_indices = self.get_cluster_indices(candidate)
            for i in m_indices:
                for j in p_indices:
                    if self.matrix[i][j] == 0:
                        cluster_dict[candidate][0] += 1
                    else:
                        cluster_dict[candidate][1] += 1
        return cluster_dict

    def get_max_impact_cluster(self):
        """
        get cluster with the maximum ones to zeros ratio
        :return: max impact cluster
        """
        cluster_dict = self.calculate_cluster()
        for key, value in cluster_dict.items():
            if value[0] != 0:
                cluster_dict[key] = value[1] / value[0]
            else:
                cluster_dict[key] = value[1]*2
        max_impact_cluster = max(cluster_dict.items())[0]
        return max_impact_cluster

    def shuffle_neighborhood(self):
        """
        take cluster with max impact, fix it and shuffle the others
        :return:
        """
        fixed_cluster = self.get_max_impact_cluster()
        # store fixed cluster indices
        m_indices, p_indices = self.get_cluster_indices(fixed_cluster)

        shuffle(self.machines)
        shuffle(self.parts)
        # get new indices after shuffling
        new_m_indices, new_p_indices = self.get_cluster_indices(fixed_cluster)

        # swap fixed cluster elements back to their original position
        for i in range(len(m_indices)):
            self.machines[m_indices[i]], self.machines[new_m_indices[i]] = self.machines[new_m_indices[i]], \
                                                                           self.machines[m_indices[i]]

        for i in range(len(p_indices)):
            self.parts[p_indices[i]], self.parts[new_p_indices[i]] = self.parts[new_p_indices[i]], \
                                                                           self.parts[p_indices[i]]
        self.calculate_neighbour_impact()
        return

    def calculate_neighbour_impact(self):
        """
        calculates number of ones and zeros fo current solution
        suggest to call it after performing global neighborhoods
        :return:
        """
        zero_one_n = [sum(x) for x in zip(*self.calculate_cluster().values())]
        self.ones = zero_one_n[1]
        self.zeros = zero_one_n[0]

    def merge_neighborhood(self):
        """
        Merge two random clusters neigborhood
        :return:
        """
        if len(set(self.machines)) > 1:
            candidate_clusters = sample(set(self.machines), 2)
            candidate_clusters.sort()
            for i in range(self.m):
                if self.machines[i] == candidate_clusters[1]:
                    self.machines[i] = candidate_clusters[0]
            for i in range(self.p):
                if self.parts[i] == candidate_clusters[1]:
                    self.parts[i] = candidate_clusters[0]
        self.calculate_neighbour_impact()
        return

    def cluster_check(self):
        objective = self.ones / (self.ones_all + self.zeros)
        available = set(self.machines).intersection(self.parts)
        for cluster in set(self.parts + self.machines):
            if cluster not in self.machines:
                # find parts that allocated on "cluster"
                for i in [j for j, x in enumerate(self.parts) if x == cluster]:
                    # try to move this part into other cluster
                    cl = choice(list(available))
                    ones, zeros = self.delta_row(i, cl)
                    # new = (self.ones + ones) / (self.ones_all + self.zeros + zeros)
                    # objective = new
                    self.ones += ones
                    self.zeros += zeros
                    self.parts[i] = cl

            if cluster not in self.parts:
                # find machines that allocated on "cluster"
                for i in [j for j, x in enumerate(self.machines) if x == cluster]:
                    # try to move this machine into other cluster
                    cl = choice(list(available))
                    ones, zeros = self.delta_col(i, cl)
                    # new = (self.ones + ones) / (self.ones_all + self.zeros + zeros)
                    # objective = new
                    self.ones += ones
                    self.zeros += zeros
                    self.machines[i] = cl
        _, self.ones, self.zeros = self.objective_function()
        return

    # neighborhoods  for VND

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
                    new = (self.ones + ones) / (self.ones_all + self.zeros + zeros)
                    if new > objective:
                        objective = new
                        result = (machine, cluster, self.ones + ones, self.zeros + zeros)

        return result

    def swap_row(self):
        """
        Find two rows which clusters swap get max impact on objective function
        :return: (index of fist row, index of second row, number of ones in clusters in new solution, number of zeros in
        clusters in new solution)
        """
        objective = self.ones / (self.ones_all + self.zeros)
        result = ()
        for machine in range(self.m):
            for oponent in range(self.m):
                if oponent != machine:
                    fones, fzeros = self.delta_col(machine, self.machines[oponent])
                    opones, opzeros = self.delta_col(oponent, self.machines[machine])
                    new = self.ones + fones + opones
                    new /= self.ones_all + self.zeros + fzeros + opzeros

                    if new > objective:
                        objective = new
                        result = (machine, oponent, self.ones + fones + opones, self.zeros + fzeros + opzeros)

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
                    new = (self.ones + ones) / (self.ones_all + self.zeros + zeros)
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
        for part in range(self.p):
            for oponent in range(self.p):
                if oponent != part:
                    fones, fzeros = self.delta_row(part, self.parts[oponent])
                    opones, opzeros = self.delta_row(oponent, self.parts[part])
                    new = self.ones + fones + opones
                    new /= self.ones_all + self.zeros + fzeros + opzeros

                    if new > objective:
                        objective = new
                        result = (part, oponent, self.ones + fones + opones, self.zeros + fzeros + opzeros)

        return result

    def general_vns(self, iteration):
        neigbor = ["division", "shuffle", "merge",  "swap_row", "swap_col", "move_row", "move_col" ]
        k_max = 3
        l_max = 7
        k = 0
        # generate random solution
        self.random_solution()
        best = (cp(self.machines), cp(self.parts), cp(self.ones), cp(self.zeros))
        best_in = (cp(self.machines), cp(self.parts), cp(self.ones), cp(self.zeros))
        objective = self.ones / (self.ones_all + self.zeros)

        while(k < k_max):
            # shaking phase
            self.neighbors(neigbor[k])

            # local search by VND
            l = k_max
            while(l < l_max):
                self.neighbors(neigbor[l])
                if best_in[2] != self.ones or best_in[3] != self.zeros:

                    best_in = (self.machines, self.parts, self.ones, self.zeros)
                    l = k_max
                else:
                    l += 1


            new = self.ones/ (self.ones_all + self.zeros)
            if new > objective:
                best = cp(best_in)
                objective = new
                k = 1
                print("best_obh = ", objective, "\n", best_in, "\n")
            else:
                k += 1

        return best

bicl = BiCl(0, 0)
bicl.parse_file("instances/37x53.txt")
print(bicl.general_vns(10))



