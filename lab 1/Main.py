# Main file
import RILS as rils

#lolkek
def parse_file(filename):
    with open(filename, "r") as f:
        lines = f.readlines()
    dimension = int(lines[0])
    flow_matrix = [[]] * dimension
    distance = [[]] * dimension
    for i in range(dimension):
        distance[i] = [int(dist) for dist in lines[i + 1].split()]
        flow_matrix[i] = [int(flow) for flow in lines[i + dimension + 2].split()]
    return dimension, distance, flow_matrix

def to_file(filename, solution):
    with open(filename, "w") as f:
        tmp = str(solution).replace("[", "")
        tmp = tmp.replace("]", "").replace(",", " ")
        f.write(tmp)



# main
def main():
    qap=rils.QAP()
    qap.parse_file("instances/tai20a")
    o, s = qap.iterated_local_search(10)
    to_file("tai20a.sol", s)



if "__main__":
    main()
