import math
import random

def generator(lambda_in):
    res = []
    value = 1
    i = 0
    cube = []
    while value > pow(10, -8):
        value = pow(lambda_in, i) * math.exp(-lambda_in)/math.factorial(i)
        res.append(value)
        # print(str(i) + " " + str(value))
        if i == 0:
            cube.append(value)
        else:
            cube.append(cube[len(cube) - 1] + value)
        i += 1
    return cube

def generate_msg(p, cube):
    for i in range(len(cube)):
        if p >= cube[i - 1] and p < cube[i]:
            return i
    return 0

def get_time_array(msg):
    res = []
    for i in range(msg):
        p = random.random()
        res.append(p)
    res.sort()
    return res
