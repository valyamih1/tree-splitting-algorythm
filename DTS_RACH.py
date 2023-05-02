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
        collided_preambles[i].append((round(M * collision_probability[i][0]), i))
        collided_requests[i].append((round(distibution_n_i[i] - successful_requests[i][0]), i))
    return collided_preambles, collided_requests



def dynamic_tree_splitting():
    mc, nc = first_access_attempt()
    for i in range(max_rao):
        cc.append([])
        b.append([])
        T.append([])
        g.append([])
        G.append([])
        for k in range(k_max):
            cc[i].append(-1)
            b[i].append(0)
            T[i].append(0)
            g[i].append(0)
            G[i].append(0)
            mc[i].append((0, 0))
            nc[i].append((0, 0))
    print(mc)
    for i in range(max_rao):
        for k in range(k_max):
            if mc[i][k][0] == 0:
                break
            else:
                if mc[i][k][0] >= 1:
                    cc[i][k] = math.floor(nc[i][k][0] / mc[i][k][0])
                else:
                    cc[i][k] = 0
                if cc[i][k] == 0:
                    break
                if M % cc[i][k] == 0:
                    b[i][k] = math.floor(cc[i][k])
                elif M % cc[i][k] > 0:
                    b[i][k] = math.floor(cc[i][k] - 1)
                else:
                    b[i][k] = 0

                M_i_k = mc[i][k][0] * b[i][k]
                L_i_k = math.ceil(M_i_k/M)
                secondary_success_probability = (nc[i][k][0] / M_i_k) * pow(1 - 1 / M_i_k, nc[i][k][0] - 1)
                secondary_idle_probability = pow(1 - 1 / M_i_k, nc[i][k][0])
                secondary_collision_probability = 1 - secondary_success_probability - secondary_idle_probability
                secondary_successful_devices = M_i_k * secondary_success_probability
                secondary_collided_preambles = M_i_k * secondary_collision_probability
                secondary_collided_devices = nc[i][k][0] - secondary_successful_devices
                G[i][k + 1] = M/b[i][k]
                for m in range(mc[i][k][0]):
                    if i <= T_a:
                        T[i][k] = i + T_a
                    else:
                        T[i][k] = i + 1
                    # for r in G[i][k]:
                    #     if len(r) < 1:
                    #         g[m] = r
