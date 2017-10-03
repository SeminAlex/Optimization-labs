# Main file


def parse_file(filename):
    with open(filename, "r") as f:
        lines = f.readlines()
    dimension = int(lines[0])
    flow_matrix = [[]] * dimension
    distance = [[]]*dimension
    for i in range(dimension):
        distance[i] = [int(dist) for dist in lines[i+1].split()]
        flow_matrix[i] = [int(flow) for flow in lines[i+dimension+2].split()]
    return dimension, distance, flow_matrix


#main
def main():
   # print(parse_file("instances/tai100a"))
    print("main")


if "__main__":
    main()
