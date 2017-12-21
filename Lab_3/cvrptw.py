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
        x = (self.x - second.x)**2
        y = (self.y - second.y)**2
        return (x + y)**0.5


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
        self.distance = [[0]*len(self.customers)]*len(self.customers)
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

    def is_available(self, first, second, current_time):
        """
        Check if customer is available for vehicle and vehicle has enough goods 
        :return: 
        """
        total_time = current_time + self.distance[first][second]

    def init_chromosome(self, P):

        t = list(range(len(self.customers)))

        for i in range(len(self.customers)*P):
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





parse_file("instanes/C104.txt")
