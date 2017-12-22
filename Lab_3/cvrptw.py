from random import randint, sample


class Customer:
    __slots__ = ["x", "y", "demand", "ready", "due", "service"]

    def __init__(self, x=0, y=0, demand=0, ready=0, due=0, service=0):
        self.x = x
        self.y = y
        self.demand = demand
        self.ready = ready
        self.due = due
        self.service = service

    def distance(self, second):
        x = (self.x - second.x) ** 2
        y = (self.y - second.y) ** 2
        return (x + y) ** 0.5


def parse_file(filename):
    with open(filename, "r") as f:
        text = f.readlines()

    vehicles, capacity = [int(i) for i in text[4].split()]
    customers = list()
    for i in range(9, len(text)):
        tmp = [int(j) for j in text[i].split()]
        customers.append(Customer(*tmp[1:]))
    return vehicles, capacity, customers


class CVRPTW:
    __slots__ = ["vehicles", "capacity", "customers", "routes", "times", "distance", ]

    def __init__(self, vehicles, capacity, customers):
        self.vehicles = vehicles
        self.capacity = capacity
        self.customers = customers
        self.routes = list()
        self.times = list()
        self.distance = list()
        self.__calculate_distance()

    def __calculate_distance(self):
        self.distance = [[0] * len(self.customers) for _ in range(len(self.customers))]
        for i in range(len(self.customers)):
            for j in range(i, len(self.customers)):
                self.distance[i][j] = self.distance[j][i] = self.customers[i].distance(self.customers[j])
        return

    def to_file(self, filename):
        with open(filename, "w") as f:
            for i in range(len(self.routes)):
                for j in range(len(self.routes[i])):
                    f.write(str(self.routes[i][j]) + " " + str(self.times[i][j]))
                f.write("\n")
        return

    def is_available(self, first, second, current_time, current_capasity):
        """
        Check if customer is available for vehicle and vehicle has enough goods 
        :return: 
        """
        total_time = current_time + self.distance[first][second] + self.customers[second].service
        if total_time + self.distance[second][0] <= self.customers[0].due and \
                current_capasity - self.customers[second].demand >= 0:
            return True
        return False

    def init_chromosome(self, p):
        t = list(range(len(self.customers)))
        for i in range(len(self.customers) * p):
            x, y = sample(t, 2)
            t[x], t[y] = t[y], t[x]
        return t

    def mutation(self, t):
        x = len(self.customers)
        a, b = sample(range(x), 2)
        t[a], t[b] = t[b], t[a]
        c = list(range(x))
        for i in range(x):
            c[i] = t[i]
        return c

    def crossover(self, ch_first, ch_second):
        i, j = sample(range(1, len(self.customers)), 2)
        if i>j:
            i,j = j,i

        child1 = [0]*len(self.customers)
        child2 = [0]*len(self.customers)
        # copy some gens to childs
        child1[i:j] = ch_first[i:j]
        child2[i:j] = ch_second[i:j]
        index = ch_second.index(child1[j]) + 1
        x = j + 1

        while True:
            while True:
                if ch_first[index] not in child1 and index < len(self.customers):
                    child1[x] = ch_second[index]
                    break
                elif index < len(self.customers):
                    index += 1
                else:
                    index = 1
            if x >= len(self.customers) - 1:
                x = 0
            if x == i - 1:
                break
            x += 1

            index = ch_first.index(child2[j]) + 1
            x = j + 1

            while True:
                while True:
                    if ch_second[index] not in child2 and index < len(self.customers):
                        child2[x] = ch_first[index]
                        break
                    elif index < len(self.customers):
                        index += 1
                    else:
                        index = 1
                if x >= len(self.customers) - 1:
                    x = 0
                if x == i - 1:
                    break
                x += 1

        return child1, child2

parse_file("instanes/C104.txt")
