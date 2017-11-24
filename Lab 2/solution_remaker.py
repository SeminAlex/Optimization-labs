import re

import os


def remake_solution(filename):
    reg = re.compile('\w*_', re.DOTALL)

    with open(filename, "r") as f:
        lines = f.readlines()

    for i in range(len(lines)):
        lines[i] = re.sub(reg, '', lines[i])

    return lines



def renew():
    for solution in os.listdir("theverybest"):
        new_sol = remake_solution("theverybest/{}".format(solution))
        with open("remastered_theverybest/{}".format(solution), 'w') as f:
            for i in new_sol:
                f.write(i)


renew()
