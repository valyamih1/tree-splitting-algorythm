import random
import generators as gen
import numpy as np
import math


def binary_tree(time, rao, preamb, q, level):
    G = int(len(preamb) / q)
    trao = []
    num_of_used_preamb = 0
    is_resolved = False
    if level == 0:
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
                    rao[i][j][2] += 2
                rao[i][j][3] += 1
                p = random.randint(0, q - 1)
                trao[i][p].append((rao[i][j]))
    else:
        for i in range(len(rao)):
            trao.append([])
            for j in range(len(rao[i])):
                if len(rao[i][j]) > 1:
                    for q_1 in range(q):
                        trao[i].append([])
                    for k in range(len(rao[i][j])):
                        num_of_used_preamb += 1
                        if num_of_used_preamb <= G*q:
                            rao[i][j][k][2] += 1
                        else:
                            rao[i][j][k][2] += num_of_used_preamb % (G*q)
                        rao[i][j][k][3] += 1
                        p = random.randint(0, q - 1)
                        trao[i][p].append((rao[i][j][k]))
    for i in range(len(trao)):
        for j in range(len(trao[i])):
            if len(trao[i][j]) > 1:
                is_resolved = False
                binary_tree(time, trao, preamb, q, level+1)
            else:
                is_resolved = True
    if is_resolved:
        return trao


def tree_splitting(K, q, m):
    time = 0
    user_buffers = []
    preamb = []
    G = int(m / q)
    num_pr_transmissions = 0
    rao = []
    trao = []
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
    trao = binary_tree(time, rao, preamb, q, 0)
    for i in range(len(trao)):
        for j in range(len(trao[i])):
            if len(trao[i][j]) != 0:
                print(trao[i][j])
