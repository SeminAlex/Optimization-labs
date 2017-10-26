
class BiCl:
    __slots__ = ["m", "p", "matrix", "machines", "parts", "max_cluster", "ones_n"]

    def __init__(self, m, p, matrix=list(), ones_n=0):
        self.m = m
        self.p = p
        self.matrix = matrix                # boolean matrix. It allow us to get fast access to element
        self.machines = list()
        self.parts = list()
        self.ones_n = ones_n

    def parse_file(self, filename):
        with open(filename, "r") as f:
            lines = f.readlines()
        self.m, self.p = int(lines[0].split()[0]), int(lines[0].split()[1])
        self.matrix = [[0]*self.p for i in range(self.m)]
        for i in range(1, len(lines)-1):
            for j in lines[i].split()[1:]:
                self.matrix[i][int(j)-1] = 1
        return self.matrix
        # dimension = (int(lines[0].split()[0]), int(lines[0].split()[1]))
        # self.matrix = [[]] * dimension[0]
        # for i in range(1, len(lines)):
        #     self.matrix[i - 1] = [int(i) - 1 for i in lines[i].split()[1:]]
        # return self.matrix

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
        '''
        Calculate impact on objective function if machines with index 'index' will be moved to cluster 'cluster'  
        :param index: index of machine
        :param cluster: new cluster for this machine
        :return: difference in 'ones in cluster' and 'zeroes out cluster' 
        '''
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

    def raw_add(self):
        for i in range(self.m):
            for j in range(self.p):
                return
        return

bicl = BiCl(0, 0)
print(bicl.parse_file("instances/testinstance"))


