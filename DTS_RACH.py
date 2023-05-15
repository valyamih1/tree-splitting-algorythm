import math
import random
from scipy import integrate
# from scipy.stats import beta as bt

max_rao = 50
k_max = 8
number_of_collided_preambles = []
collision_coefficient = []
number_of_collided_request = []
total_preambles_in_system = 54
number_of_branches = []
N = 50000
time_of_burst_arrivals = 50
delay_in_every_subtree = []
successful_devices = []


def g_t(i):
    alpha = 3
    beta = 4
    return (pow(i, 2) * pow(time_of_burst_arrivals - i, 3))/(pow(time_of_burst_arrivals, 6) * random.betavariate(alpha, beta))


def integration(a, b, n):
    h = (b - a) / n
    sum = 0.5 * (g_t(a) + g_t(b))

    for i in range(1, n):
        x = a + i * h
        sum += g_t(x)

    return h * sum


def get_distribution(time_of_burst_arrivals):
    distribution = []
    for t in range(time_of_burst_arrivals):
        v = integration(t, t+1, 5000)
        # v, err = integrate.quad(g_t, a=t - 1, number_of_branumber_of_collided_requesthes=t, limit=100000)
        distribution.append(round(v*20*N))
    total_devices = sum(distribution)
    print(distribution)
    print(total_devices)
    return distribution


def first_access_attempt():
    distibution_n_i = get_distribution(time_of_burst_arrivals)
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
    for i in range(time_of_burst_arrivals):
        success_probability[i].append((distibution_n_i[i] / total_preambles_in_system) * pow(1 - 1 / total_preambles_in_system, distibution_n_i[i] - 1))
        idle_probability[i].append(pow(1 - 1 / total_preambles_in_system, distibution_n_i[i]))
        collision_probability[i].append(1 - success_probability[i][0] - idle_probability[i][0])
        successful_requests[i].append(math.ceil(total_preambles_in_system * success_probability[i][0]))
        collided_preambles[i].append((round(total_preambles_in_system * collision_probability[i][0]), time_of_burst_arrivals))
        collided_requests[i].append((distibution_n_i[i] - successful_requests[i][0], time_of_burst_arrivals))
    return collided_preambles, collided_requests, successful_requests


def dynamic_tree_splitting():
    number_of_collided_preambles, number_of_collided_request, successful_devices = first_access_attempt()
    for i in range(max_rao):
        collision_coefficient.append([])
        number_of_branches.append([])
        if number_of_collided_request[i][0][0] == 0:
            delay_in_every_subtree.append(0)
        else:
            delay_in_every_subtree.append(12 * time_of_burst_arrivals)
        for k in range(k_max):
            collision_coefficient[i].append(-1)
            number_of_branches[i].append(0)
            number_of_collided_preambles[i].append((0, 0))
            number_of_collided_request[i].append((0, 0))
    # print(number_of_collided_preambles)
    for i in range(max_rao):
        for k in range(k_max):
            if number_of_collided_preambles[i][k][0] == 0:
                break
            else:
                if number_of_collided_preambles[i][k][0] >= 1:
                    collision_coefficient[i][k] = math.floor(number_of_collided_request[i][k][0] / number_of_collided_preambles[i][k][0])
                else:
                    collision_coefficient[i][k] = 0
                if collision_coefficient[i][k] == 0:
                    break
                if total_preambles_in_system % collision_coefficient[i][k] == 0:
                    number_of_branches[i][k] = math.floor(collision_coefficient[i][k])
                elif total_preambles_in_system % collision_coefficient[i][k] > 0:
                    number_of_branches[i][k] = math.floor(collision_coefficient[i][k] - 1)
                else:
                    number_of_branches[i][k] = 0

                total_preambles_for_each_step = number_of_collided_preambles[i][k][0] * number_of_branches[i][k]
                delay_in_every_subtree[i] += 12 * (total_preambles_for_each_step/total_preambles_in_system)
                length_of_level_k = math.ceil(total_preambles_for_each_step/total_preambles_in_system)
                secondary_success_probability = (number_of_collided_request[i][k][0] / total_preambles_for_each_step) * pow(1 - 1 / total_preambles_for_each_step, number_of_collided_request[i][k][0] - 1)
                secondary_idle_probability = pow(1 - 1 / total_preambles_for_each_step, number_of_collided_request[i][k][0])
                secondary_collision_probability = 1 - secondary_success_probability - secondary_idle_probability
                secondary_successful_devices = math.ceil(total_preambles_for_each_step * secondary_success_probability)
                secondary_collided_preambles = math.floor(total_preambles_for_each_step * secondary_collision_probability)
                successful_devices[i].append(secondary_successful_devices)
                if secondary_collided_preambles > 0:
                    secondary_collided_devices = number_of_collided_request[i][k][0] - secondary_successful_devices
                else:
                    secondary_collided_devices = 0
                    number_of_collided_preambles[i + 1][0] = (number_of_collided_preambles[i + 1][0][0], number_of_collided_preambles[i][k][1] + length_of_level_k)
                    number_of_collided_request[i + 1][0] = (number_of_collided_request[i + 1][0][0], number_of_collided_request[i][k][1] + length_of_level_k)
                # G[i][k + 1] = total_preambles_in_system/number_of_branumber_of_collided_requesthes[i][k]
                number_of_collided_preambles[i][k + 1] = (secondary_collided_preambles, number_of_collided_preambles[i][k][1] + length_of_level_k)
                number_of_collided_request[i][k + 1] = (secondary_collided_devices, number_of_collided_request[i][k][1] + length_of_level_k)
            number_of_collided_preambles[i + 1][0] = (number_of_collided_preambles[i + 1][0][0], number_of_collided_preambles[i][k][1] + length_of_level_k + 1)
            number_of_collided_request[i + 1][0] = (number_of_collided_request[i + 1][0][0], number_of_collided_request[i][k][1] + length_of_level_k + 1)
                # for m in range(number_of_collided_preambles[i][k][0]):
                #     if i <= time_of_burst_arrivals:
                #         T[i][k] = i + time_of_burst_arrivals
                #     else:
                #         T[i][k] = i + 1
                    # for r in G[i][k]:
                    #     if len(r) < 1:
                    #         g[m] = r
    print(number_of_collided_preambles)
    print(number_of_collided_request)
    outage_devices = 0
    maximal_rao = 0
    total_delay = 0
    print(successful_devices)
    sum_of_successful_devices = 0
    for i in range(len(number_of_collided_request)):
        outage_devices += number_of_collided_request[i][len(number_of_collided_request[i])-1][0]
        maximal_rao = max(number_of_collided_request[i][0][1], maximal_rao)
        total_delay += delay_in_every_subtree[i]
        sum_of_successful_devices += sum(successful_devices[i])
    mean_delay = total_delay/time_of_burst_arrivals
    mean_throughput = sum_of_successful_devices/(total_preambles_in_system*total_delay)
    print(outage_devices, maximal_rao)
