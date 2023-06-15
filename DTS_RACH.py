import math
import random
# from scipy import integrate
# from scipy.stats import beta as bt


def g_t(i):
    alpha = 3
    beta = 4
    time_of_burst_arrivals = 50
    return (pow(i, 2) * pow(time_of_burst_arrivals - i, 3))/(pow(time_of_burst_arrivals, 6) * random.betavariate(alpha, beta))


def integration(a, b, n):
    h = (b - a) / n
    sum = 0.5 * (g_t(a) + g_t(b))

    for i in range(1, n):
        x = a + i * h
        sum += g_t(x)

    return h * sum


def get_distribution(time_of_burst_arrivals, N):
    distribution = []
    for t in range(time_of_burst_arrivals):
        v = integration(t, t+1, 5000)
        # v, err = integrate.quad(g_t, a=t - 1, number_of_branumber_of_collided_requesthes=t, limit=100000)
        distribution.append(round(v*20*N))
    total_devices = sum(distribution)
    # print(distribution)
    print(total_devices)
    return distribution, total_devices


def first_access_attempt(time_of_burst_arrivals, N, max_rao, total_preambles_in_system):
    distribution_n_i, new_N = get_distribution(time_of_burst_arrivals, N)
    exact_devices = []
    for i in range(new_N):
        exact_devices.append((-1,-1))
    dev_total = 0
    for index, slot in enumerate(distribution_n_i):
        # if slot != 0:
        #
        for j in range(slot):
            exact_devices[dev_total] = (j+1, index, 1)
            dev_total += 1

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
        success_probability[i].append((distribution_n_i[i] / total_preambles_in_system) * pow(1 - (1 / total_preambles_in_system), distribution_n_i[i] - 1))
        idle_probability[i].append(pow(1 - (1 / total_preambles_in_system), distribution_n_i[i]))
        collision_probability[i].append(1 - success_probability[i][0] - idle_probability[i][0])
        successful_requests[i].append(math.ceil(total_preambles_in_system * success_probability[i][0]))
        collided_requests[i].append((distribution_n_i[i] - successful_requests[i][0], time_of_burst_arrivals))
        for j in range(len(exact_devices)):
            if exact_devices[j][1] == i:
                if successful_requests[i][0] < exact_devices[j][0]:
                    exact_devices[j] =(exact_devices[j][0],exact_devices[j][1], 1 + exact_devices[j][2])
                else:
                    exact_devices[j] =(exact_devices[j][0],exact_devices[j][1], 0 - exact_devices[j][2])

        if collided_requests[i][0][0] > 0:
            collided_preambles[i].append(
                (math.ceil(total_preambles_in_system * collision_probability[i][0]), time_of_burst_arrivals))
        else:
            collided_preambles[i].append(
                (math.floor(total_preambles_in_system * collision_probability[i][0]), time_of_burst_arrivals))
    return collided_preambles, collided_requests, successful_requests, new_N, exact_devices


def dynamic_tree_splitting(old_N, kmax, sic):
    max_rao = 50
    k_max = kmax - 1
    collision_coefficient = []
    total_preambles_in_system = 54
    number_of_branches = []
    throughput = []
    time_of_burst_arrivals = 50
    delay_in_every_subtree = []
    sra_preamb, sra_collisons, sra_success, sra_N, sra_exact_devices = my_sra(1000000, time_of_burst_arrivals, old_N, max_rao, total_preambles_in_system)
    number_of_collided_preambles, number_of_collided_request, successful_devices, N, exact_devices = first_access_attempt(time_of_burst_arrivals, old_N, max_rao,total_preambles_in_system)
    for i in range(max_rao):
        throughput.append(0)
        collision_coefficient.append([])
        number_of_branches.append([])
        if number_of_collided_request[i][0][0] == 0:
            delay_in_every_subtree.append(0)
        else:
            delay_in_every_subtree.append(time_of_burst_arrivals)
        for k in range(k_max):
            collision_coefficient[i].append(-1)
            number_of_branches[i].append(0)
            number_of_collided_preambles[i].append((0, 0))
            number_of_collided_request[i].append((0, 0))
    for i in range(max_rao):
        countr = 0
        for k in range(k_max):
            if number_of_collided_preambles[i][k][0] == 0:
                break
            else:
                if number_of_collided_preambles[i][k][0] >= 1:
                    collision_coefficient[i][k] = math.ceil(number_of_collided_request[i][k][0] / number_of_collided_preambles[i][k][0])
                else:
                    collision_coefficient[i][k] = 0
                if collision_coefficient[i][k] == 0:
                    break
                countr += 1
                if total_preambles_in_system % collision_coefficient[i][k] == 0:
                    number_of_branches[i][k] = math.floor(collision_coefficient[i][k])
                elif total_preambles_in_system % collision_coefficient[i][k] > 0:
                    while total_preambles_in_system % collision_coefficient[i][k] > 0:
                        collision_coefficient[i][k] += 1
                    number_of_branches[i][k] = math.floor(collision_coefficient[i][k])
                else:
                    number_of_branches[i][k] = 0

                total_preambles_for_each_step = number_of_collided_preambles[i][k][0] * number_of_branches[i][k]
                delay_in_every_subtree[i] += 22 * (total_preambles_for_each_step/total_preambles_in_system)
                length_of_level_k = math.ceil(total_preambles_for_each_step/total_preambles_in_system)
                throughput[i] += number_of_collided_request[i][k][0] / length_of_level_k
                if sic > 0:
                    secondary_success_probability = k/9 +(number_of_collided_request[i][k][0] / total_preambles_for_each_step) * pow(1 - 1 / total_preambles_for_each_step, number_of_collided_request[i][k][0] - 1)
                else:
                    secondary_success_probability = (number_of_collided_request[i][k][0] / total_preambles_for_each_step) * pow(
                        1 - 1 / total_preambles_for_each_step, number_of_collided_request[i][k][0] - 1)
                secondary_idle_probability = pow(1 - 1 / total_preambles_for_each_step, number_of_collided_request[i][k][0])
                secondary_collision_probability = 1 - secondary_success_probability - secondary_idle_probability
                if sic > 0 and k == sic-1:
                    secondary_success_probability = 1
                    secondary_idle_probability = 0
                    secondary_collision_probability = 0
                # elif sic > 0 and k > 0:

                secondary_successful_devices = math.ceil(total_preambles_for_each_step * secondary_success_probability)
                secondary_collided_preambles = math.floor(total_preambles_for_each_step * secondary_collision_probability)
                successful_devices[i].append(secondary_successful_devices)
                for j in range(len(exact_devices)):
                    if exact_devices[j][1] == i and exact_devices[j][2] > 0:
                        step_for_devices = j
                        break
                for j in range(len(exact_devices)):
                    if exact_devices[j][1] == i and exact_devices[j][2] > 0:
                        if secondary_successful_devices + step_for_devices < j:
                            exact_devices[j] = (exact_devices[j][0], exact_devices[j][1], 1 + exact_devices[j][2])
                        else:
                            exact_devices[j] = (exact_devices[j][0], exact_devices[j][1], 0 - exact_devices[j][2])
                if secondary_collided_preambles > 0:
                    secondary_collided_devices = number_of_collided_request[i][k][0] - secondary_successful_devices
                else:
                    secondary_collided_devices = 0
                    if sic > 0 and k == sic - 1:
                        number_of_collided_preambles[i + 1][0] = (number_of_collided_preambles[i + 1][0][0], number_of_collided_preambles[i][k][1] + 1)
                        number_of_collided_request[i + 1][0] = (number_of_collided_request[i + 1][0][0], number_of_collided_request[i][k][1] + 1)
                    else:
                        number_of_collided_preambles[i + 1][0] = (number_of_collided_preambles[i + 1][0][0], number_of_collided_preambles[i][k][1] + length_of_level_k)
                        number_of_collided_request[i + 1][0] = (number_of_collided_request[i + 1][0][0], number_of_collided_request[i][k][1] + length_of_level_k)
                number_of_collided_preambles[i][k + 1] = (secondary_collided_preambles, number_of_collided_preambles[i][k][1] + length_of_level_k)
                number_of_collided_request[i][k + 1] = (secondary_collided_devices, number_of_collided_request[i][k][1] + length_of_level_k)
            if k == k_max -1:
                number_of_collided_preambles[i + 1][0] = (number_of_collided_preambles[i + 1][0][0], number_of_collided_preambles[i][k][1] + length_of_level_k + 1)
                number_of_collided_request[i + 1][0] = (number_of_collided_request[i + 1][0][0], number_of_collided_request[i][k][1] + length_of_level_k + 1)

        if countr > 0:
            throughput[i] = throughput[i]/countr

    outage_devices = 0
    maximal_rao = 0
    total_delay = 0

    sum_of_successful_devices = 0
    transmissions = 0
    thr = 0
    for i in range(len(number_of_collided_request)):
        thr += throughput[i]
        outage_devices += number_of_collided_request[i][len(number_of_collided_request[i])-1][0]
        maximal_rao = max(number_of_collided_request[i][0][1], maximal_rao)
        total_delay += delay_in_every_subtree[i]
        sum_of_successful_devices += sum(successful_devices[i])
    for i in range(len(exact_devices)):
        if exact_devices[i][2] < 0:
            transmissions += abs(exact_devices[i][2])
        if exact_devices[i][2] < -kmax:
            print(exact_devices[i])
    if total_delay == 0:
        total_delay = 1

    print(thr/maximal_rao)
    mean_transmissions = transmissions/sum_of_successful_devices
    mean_delay = total_delay/time_of_burst_arrivals
    mean_throughput = 20*(N - outage_devices)/(total_preambles_in_system*total_delay)
    success_rate = round(1 - (outage_devices / N), 5)
    sra_outage_devices = 0
    sra_delay = 0
    sra_transm = 0
    sra_counter = 0
    for i in range(len(sra_exact_devices)):
        if sra_exact_devices[i][3] == -15:
            sra_outage_devices += 1
        else:
            sra_counter += 1
            sra_delay += 10 * sra_exact_devices[i][0]
        sra_transm += abs(sra_exact_devices[i][2])
    sra_throughput = len(sra_exact_devices)/(total_preambles_in_system * (sra_delay/10))
    sra_mean_transm = sra_transm/len(sra_exact_devices)
    sra_success_rate = round(1-(sra_outage_devices/len(sra_exact_devices)), 5)
    sra_mean_delay = sra_delay/len(sra_exact_devices)

    print(outage_devices, sra_outage_devices, mean_delay, mean_throughput, maximal_rao, success_rate, mean_transmissions, sra_success_rate, sra_mean_delay, sra_mean_transm, sra_throughput)
    return mean_throughput, mean_delay, success_rate, mean_transmissions, sra_success_rate, sra_mean_delay, sra_mean_transm, sra_throughput


def my_sra(max_time, time_of_burst_arrivals, N, max_rao, total_preambles_in_system):
    distribution_n_i, new_N = get_distribution(time_of_burst_arrivals, N)
    exact_devices = []
    for i in range(new_N):
        exact_devices.append((-1, -1))
    dev_total = 0
    for index, slot in enumerate(distribution_n_i):
        for j in range(slot):
            exact_devices[dev_total] = (j + 1, index, 1, 0)
            dev_total += 1

    success_probability = []
    idle_probability = []
    collision_probability = []
    successful_requests = []
    collided_requests = []
    collided_preambles = []
    for i in range(max_time):
        distribution_n_i.append(0)
        success_probability.append(0)
        idle_probability.append(0)
        collision_probability.append(0)
        successful_requests.append(0)
        collided_preambles.append(0)
        collided_requests.append(0)
    for i in range(max_time):
        success_probability[i] =(distribution_n_i[i] / total_preambles_in_system) * pow(1 - (1 / total_preambles_in_system),
                                                                    distribution_n_i[i] - 1)
        idle_probability[i] = pow(1 - (1 / total_preambles_in_system), distribution_n_i[i])
        collision_probability[i] = 1 - success_probability[i] - idle_probability[i]
        successful_requests[i] = math.ceil(total_preambles_in_system * success_probability[i])
        collided_requests[i] = (distribution_n_i[i] - successful_requests[i], time_of_burst_arrivals)
        samples = random.sample(range(1, distribution_n_i[i]+1),successful_requests[i])
        counter = 0
        for j in range(len(exact_devices)):
            if exact_devices[j][1] == i and exact_devices[j][3] >= 0:
                counter += 1
                if exact_devices[j][0] in samples:
                    exact_devices[j] = (exact_devices[j][0], exact_devices[j][1], 0 - exact_devices[j][2], -1)
                else:
                    backoff = random.randint(1, 4)
                    if exact_devices[j][2]+1 > 8:
                        exact_devices[j] = (exact_devices[j][0], exact_devices[j][1], exact_devices[j][2], -15)
                    else:
                        exact_devices[j] = (distribution_n_i[i + backoff] + 1, exact_devices[j][1] + backoff, 1 + exact_devices[j][2], backoff)
                        distribution_n_i[i + backoff] += 1
            if counter >= distribution_n_i[i]:
                break

        if collided_requests[i][0] > 0:
            collided_preambles[i] = (math.ceil(total_preambles_in_system * collision_probability[i]), time_of_burst_arrivals)
        else:
            collided_preambles[i] = (math.floor(total_preambles_in_system * collision_probability[i]), time_of_burst_arrivals)
    return collided_preambles, collided_requests, successful_requests, new_N, exact_devices

