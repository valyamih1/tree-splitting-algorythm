import math
import random
from scipy import integrate
# from scipy.stats import beta as bt

max_rao = 5000
k_max = 10
mc = []
cc = []
nc = []
M = 54
b = []
T = []
G = []
g = []
N = 5000
T_a = 50


def g_t(i):
    alpha = 3
    beta = 4
    return (pow(i, alpha - 1) * pow(T_a - i, beta - 1))/(pow(T_a, alpha+beta-2) * random.betavariate(alpha, beta))


def get_distribution(T_a):
    distribution = []
    for t in range(T_a + 1):
        v, _ = integrate.quad(g_t, a=t - 1, b=t)
        distribution.append(math.floor(N * v))
    total_devices = sum(distribution)
    return distribution

def first_access_attempt():
    distibution_n_i = get_distribution(T_a)
    success_probability = []
    idle_probability = []
    collision_probability = []
    successful_requests = []
    collided_requests = []
    collided_preambles = []
    for i in range(max_rao):
        success_probability.append([])
        idle_probability.append([])
        collision_probability.append([])
        successful_requests.append([])
        collided_preambles.append([])
        collided_requests.append([])
    for i in range(T_a):
        success_probability[i].append((distibution_n_i[i] / M) * pow(1 - 1 / M, distibution_n_i[i] - 1))
        idle_probability[i].append(pow(1 - 1 / M, distibution_n_i[i]))
        collision_probability[i].append(1 - success_probability[i][0] - idle_probability[i][0])
        successful_requests[i].append(M * success_probability[i][0])
        collided_preambles[i].append((round(M * collision_probability[i][0]), 1))
        collided_requests[i].append((round(distibution_n_i[i] - successful_requests[i][0]), 1))
    return collided_preambles, collided_requests



def dynamic_tree_splitting():
    for i in range(max_rao):
        cc.append([])
        b.append([])
        T.append([])
        g.append([])
        G.append([])
        for k in range(k_max):
            cc[i].append(-1)
            b[i].append(-1)
            T[i].append(-1)
            g[i].append(-1)
            G[i].append(-1)
    mc, nc = first_access_attempt()
    for i in range(max_rao):
        for k in range(k_max):
            if mc[i][k] == 0:
                break
            else:
                if mc[i][k][0] >= 1:
                    cc[i][k] = math.floor(nc[i][k][0]/mc[i][k][0])
                else:
                    cc[i][k] = 0

                if M % cc[i][k] == 0:
                    b[i][k] = math.floor(cc[i][k])
                elif M % cc[i][k] > 0:
                    b[i][k] = math.floor(cc[i][k] - 1)
                else:
                    b[i][k] = 0

                G[i][k] = M/b[i][k-1]
                for m in range(mc[i][k]):
                    if i <= T_a:
                        T[i][k] = i + T_a
                    else:
                        T[i][k] = i + 1
                    for r in G[i][k]:
                        if len(r) < 1:
                            g[m] = r
