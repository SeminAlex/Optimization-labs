import RILS as rils
class Feature:
    __slots__ = ["city","fabric","penalty"]

    def __init__(self, city = 0, fabric = 0, penalty = 0, utility =0,exists = false):
        self.city = city
        self.fabric = fabric
        self.penalty = penalty
        self.utility = utility
        self.exists = exists

def populate_features(self, features, solution):
    for i in range(features.length):
        features[i] = Feature();
    for i in range(solution.length):
        position = solution[i] * solution.length + i
        features[position].plant = solution[i]
        features[position].city = i
        features[position].exists = True


def guided_local_search(self):
    # indicator = [[0]*self.dimension**2]*self.dimension**2
    features = []
    lamb = 0.4
    condition = True
    initial_solution = self.random_solution()
    p = [0] * self.dimension ** 2
    while (condition):
        new_cost, new_solution = self.local_search(initial_solution, penalty)

    return 0  ##self.best_objective, self.best