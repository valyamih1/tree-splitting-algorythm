import random
import generators as gen
import numpy as np
import math
import statistics
import pprint
import cProfile
import pstats


def binary_tree(resolved_users, rao, preamb, q, level, outage):
    G = int(len(preamb) / q)
    trao = []
    num_of_used_preamb = 0
    is_resolved = False
    new_rao = []
    # if level == 0:
    for i in range(len(rao)):
        if len(rao[i]) != 0:
            trao.append([])
            for q_1 in range(q):
                trao[i].append([])
        for j in range(len(rao[i])):
            num_of_used_preamb += 1
            if num_of_used_preamb <= G*q:
                rao[i][j][2] += 1
            else:
                rao[i][j][2] += 1 + num_of_used_preamb % (G*q)
            rao[i][j][3] += 1
            p = int(10*random.uniform(0, (q/10)))
            trao[i][p].append((rao[i][j]))
# else:
    #     for i in range(len(rao)):
    #         trao.append([])
    #         for j in range(len(rao[i])):
    #             if len(rao[i][j]) > 1:
    #                 for q_1 in range(q):
    #                     trao[i].append([])
    #                 for k in range(len(rao[i][j])):
    #                     if rao[i][j][k][3] > 10:
    #                         outage.append(rao[i][j][k])
    #                         # rao[i][j].pop(k)
    #                         break
    #                     rao[i][j][k][3] += 1
    #                     num_of_used_preamb += 1
    #                     if num_of_used_preamb <= G*q:
    #                         rao[i][j][k][2] += 1
    #                     else:
    #                         rao[i][j][k][2] += 1 + num_of_used_preamb % (G*q)
    #                     p = int(10*random.uniform(0, (q/10)))
    #                     trao[i][p].append((rao[i][j][k]))
    num_of_levels = 0
    for i in range(len(trao)):
        for j in range(len(trao[i])):
            if len(trao[i][j]) == 1:
                is_resolved = True
                resolved_users.append(trao[i][j])
            elif len(trao[i][j]) > 1:
                num_of_levels += 1
                is_resolved = False
                new_rao.append(trao[i][j])
    if is_resolved:
        # pprint.pprint(trao, width=30)
        return trao, outage, resolved_users
    else:
        if (math.ceil(num_of_levels / (G*q))) > 1:
            for i in range(math.ceil(num_of_levels / (G*q))):
                trao, outage, resolved_users = binary_tree(resolved_users, new_rao[0:(G*q)], preamb, q, level + 1, outage)
                del new_rao[0:(G*q)]
        else:
            trao, outage, resolved_users = binary_tree(resolved_users, new_rao, preamb, q, level + 1, outage)
        return trao, outage, resolved_users


def theory(N, q, M, G):
    Ps = []
    Pl = []
    C = []
    R = 1
    for m in range(1, 11):
        Ps.append((1-(1/(G*q**m)))**(N-1))
        if m > 1:
            Pl.append(Ps[m-1] - Ps[m-2])
        C.append(((G*q**m)*(1-(1-(1/(G*q**m)))**N)) - (N*((1-(1/(G*q**m)))**(N-1))))
        R += math.ceil(C[m-1]/G)
    print(Ps)
    print(Pl)
    Po = 1 - np.sum(Pl)
    print(Po)
    print(C)
    print(R)


def tree_splitting(K, q, m):
    time = 0
    user_buffers = []
    preamb = []
    G = int(m / q)
    num_pr_transmissions = 0
    rao = []
    trao = []
    outage = []
    resolved_users = []
    # r = []
    # for i in range(K):
    #     r.append(int(10*random.uniform(0, (q/10))))
    theory(K, q, m, G)
    for i in range(m):
        preamb.append(0)
        rao.append([])
    for i in range(K):
        b = random.randint(0, m - 1)
        preamb[b] += 1
        user_buffers.append([i, b, time, num_pr_transmissions])
    pr_counter = -1
    print(preamb)
    for i in range(len(preamb)):
        if preamb[i] > 1:
            pr_counter += 1
            for j in range(len(user_buffers)):
                if user_buffers[j][1] == i:
                    rao[pr_counter].append(user_buffers[j])
        elif preamb[i] == 1:
            for j in range(len(user_buffers)):
                if user_buffers[j][1] == i:
                    resolved_users.append(user_buffers[j])
    # with cProfile.Profile() as pr:
    trao, outage, resolved_users = binary_tree(resolved_users, rao, preamb, q, 0, outage)
    # stats = pstats.Stats(pr)
    # stats.sort_stats(pstats.SortKey.TIME)
    # stats.print_stats()
    # print(resolved_users)
    users = [i[0][2] for i in resolved_users]
    print(len(resolved_users))
    print(statistics.mean(users))
    # for i in range(len(trao)):
    #     for j in range(len(trao[i])):
    #         if len(trao[i][j]) != 0:
    #             print(trao[i][j])
