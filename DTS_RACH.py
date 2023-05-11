import math
import random
from scipy import integrate
# from scipy.stats import beta as bt

max_rao = 52
k_max = 7
mc = []
cc = []
nc = []
M = 54
b = []
T = []
G = []
g = []
N = 50000
T_a = 50


def g_t(i):
    alpha = 3
    beta = 4
    return (pow(i, 2) * pow(T_a - i, 3))/(pow(T_a, 6) * random.betavariate(alpha, beta))


def integration(a, b, n):
    h = (b - a) / n
    sum = 0.5 * (g_t(a) + g_t(b))

    for i in range(1, n):
        x = a + i * h
        sum += g_t(x)

    return h * sum


def get_distribution(T_a):
    distribution = []
    for t in range(T_a):
        v = integration(t, t+1, 5000)
        # v, err = integrate.quad(g_t, a=t - 1, b=t, limit=100000)
        distribution.append(round(v*20*N))
    total_devices = sum(distribution)
    print(distribution)
    print(total_devices)
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
        successful_requests[i].append(math.ceil(M * success_probability[i][0]))
        collided_preambles[i].append((round(M * collision_probability[i][0]), i))
        collided_requests[i].append((distibution_n_i[i] - successful_requests[i][0], i))
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
    # print(mc)
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
                secondary_successful_devices = math.ceil(M_i_k * secondary_success_probability)
                secondary_collided_preambles = math.floor(M_i_k * secondary_collision_probability)
                if secondary_collided_preambles > 0:
                    secondary_collided_devices = nc[i][k][0] - secondary_successful_devices
                else:
                    secondary_collided_devices = 0
                    mc[i + 1][0] = (mc[i + 1][0][0], mc[i][k][1] + L_i_k)
                    nc[i + 1][0] = (nc[i + 1][0][0], nc[i][k][1] + L_i_k)
                # G[i][k + 1] = M/b[i][k]
                mc[i][k + 1] = (secondary_collided_preambles, mc[i][k][1] + L_i_k)
                nc[i][k + 1] = (secondary_collided_devices, nc[i][k][1] + L_i_k)
                # for m in range(mc[i][k][0]):
                #     if i <= T_a:
                #         T[i][k] = i + T_a
                #     else:
                #         T[i][k] = i + 1
                    # for r in G[i][k]:
                    #     if len(r) < 1:
                    #         g[m] = r
    print(mc)
    print(nc)
    outage_devices = 0
    maximal_rao = 0
    for i in range(len(nc)):
        outage_devices = outage_devices + nc[i][len(nc[i])-1][0]
        maximal_rao = max(nc[i][0][1], maximal_rao)
    print(outage_devices, maximal_rao)
