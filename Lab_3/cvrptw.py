from random import randint, sample
from time import clock
from math import floor

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

    def mutation(self, t, c):
        x = len(self.customers)
        a, b = sample(range(x), 2)
        t[a], t[b] = t[b], t[a]
#        c = list(range(x))
        for i in range(x):
            c[i] = t[i]
        return t, c

    def crossover(self, ch_first, ch_second):
        i, j = sample(range(1, len(self.customers)), 2)
        if i > j:
            i, j = j, i

        child1 = [0] * len(self.customers)
        child2 = [0] * len(self.customers)
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

    def culc_cost(self, tab, capacity):
        cost = 0
        actual_time = 0
        actual_capacity = capacity
        actual_place = 0
        destination = tab[1]
        executed = 1
        vehicle = 0

        while executed != len(self.customers):
            if self.is_available(actual_place, destination, actual_time, actual_capacity):
                if self.distance[actual_place][destination] + actual_time > self.customers[destination].ready:
                    actual_time += self.distance[actual_place][destination] + self.customers[destination].ready
                else:
                    actual_time = self.customers[destination].ready + self.customers[destination].service
                actual_capacity -= self.customers[destination].demand
                actual_place = destination
            else:
                cost += actual_time + self.distance[actual_place][0]
                actual_time = 0
                actual_capacity = capacity
                vehicle += 1
                destination = 0
                actual_place = 0
            if destination != 0:
                executed += 1
            destination = tab[executed]

        cost += actual_time + self.distance[actual_place][0]
        vehicle += 1
        return cost

    def show_results(self, tab, capacity):
        cost = 0
        actual_time = 0
        actual_capacity = capacity
        actual_place = 0
        destination = tab[1]
        executed = 1
        vehicle = 0
        results = list()
        size = 0

        file = open("out.txt", "w")
        while executed != len(self.customers):
            if self.is_available(actual_place, destination, actual_time, actual_capacity):
                if self.distance[actual_place][destination] + actual_time > self.customers[destination].ready:
                    actual_time += self.distance[actual_place][destination] + self.customers[destination].ready
                else:
                    actual_time = self.customers[destination].ready + self.customers[destination].service
                actual_capacity -= self.customers[destination].demand
                actual_place = destination
                results.append(destination)
                size += 1
            else:
                cost += actual_time + self.distance[actual_place][0]
                actual_time = 0
                actual_capacity = capacity
                vehicle += 1
                destination = 0
                actual_place = 0
                results.append(0)
                size += 1
            if destination != 0:
                executed += 1
            destination = tab[executed]

        cost += actual_time + self.distance[actual_place][0]
        vehicle += 1

        file.write(str(vehicle) + " " + str(cost) + "\n")
        for i in range(size):
            if results[i] == 0:
                file.write("\n")
            else:
                file.write(str(results[i]) + " ")

        file.close()


vehicles, capacity, customers = parse_file("instanes/C104.txt")


##########################
P = 3
POPSIZE = 8
GEN = 13
M = 1
CLOCKS_PER_SEC = 10000

pojemnosc=0
straznik=1
cvrptw = CVRPTW(vehicles, capacity, customers)

for i in range(1,len(customers)):
    if not cvrptw.is_available(0, i, 0, pojemnosc):
        straznik=0
        break

    if straznik:
        population =list()
        for i in range(POPSIZE+GEN+2):
            population.append([0]*len(customers))

        i = 360/POPSIZE
        j = 360/POPSIZE
        a=360/POPSIZE
        rl = 0
        s = 0
        t = 0
        the_best_cost = float('inf')
        the_best_population = [0]*len(customers)
        nothing=0

        for i in range(POPSIZE):
            cvrptw.init_chromosome(population[i])

        generation=1
        start=clock()
        while clock()<start+18*CLOCKS_PER_SEC:
            generation += 1
            for i in range(POPSIZE,POPSIZE+M):
                rl=randint()%360
                for j in range(1, POPSIZE):
                    if floor(rl/a)==j-1:
                        s=j-1
                        population[s], population[i] = cvrptw.mutation(population[s],population[i])


            for i in range(POPSIZE+M, POPSIZE+GEN):
                while True:
                    rl=randint()%360
                    for j in range(1,POPSIZE):
                        if floor(rl/a)==j-1:
                            s=j-1

                    rl=randint()%360
                    for j in range(1,POPSIZE):
                        if floor(rl/a)==j-1:
                            t=j-1
                    if s != t:
                        break
                population[i], population[i+1] = cvrptw.crossover(population[s],population[t])


            best_cost= cvrptw.culc_cost(population[0],pojemnosc)
            best=0

            for i in range(POPSIZE):
                for j in range(i,POPSIZE+GEN):
                    if cvrptw.culc_cost(population[j],pojemnosc)<best_cost:
                        best=j
                        best_cost=cvrptw.culc_cost(population[j],pojemnosc)
                for x in range(len(customers)):
                    population[i][x],population[best][x] = population[best][x], population[i][x]


            if generation==2:
                the_best_cost=cvrptw.culc_cost(population[0],pojemnosc)
                for y in range(len(customers)):
                    the_best_population[y]=population[0][y]

            if the_best_cost>cvrptw.culc_cost(population[0],pojemnosc):
                the_best_cost=cvrptw.culc_cost(population[0],pojemnosc)
                for y in range(len(customers)):
                    the_best_population[y]=population[0][y]

                print("new best CHILD " + str(the_best_cost) +" iteration without changes: " +
                      str(nothing)+" generacja: " +str(generation) + "\n")

                nothing=0
            else:
                nothing+=1


            if nothing==100:
                break


        cvrptw.show_results(the_best_population,pojemnosc)



