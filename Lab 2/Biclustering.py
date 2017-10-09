

m = parse_file("instances/testInstance")
print(m)


class BiCl:
    __slots__ = ["matrix","objective"]

    def __init__(self, matrix=list()):
        self.matrix = matrix
        self.machines
        self.parts

    def parse_file(self, filename):
        with open(filename, "r") as f:
            lines = f.readlines()
        dimension = (int(lines[0].split()[0]), int(lines[0].split()[1]))
        self.matrix = [[]] * dimension[0]
        for i in range(1, len(lines)):
            self.matrix[i - 1] = [int(i) - 1 for i in lines[i].split()[1:]]
        return self.matrix

    def objective_function(self):
        objective = self.matrix[]
