import math
import random
import copy


def theory(N, q, M, G):
    Ps = []
    Pl = []
    C = []
    R = 1
    T = []
    for m in range(1, 11):
        Ps.append((1-(1/(G*q**m)))**(N-1))
        if m > 1:
            Pl.append(Ps[m-1] - Ps[m-2])

        C.append(((G*q**m)*(1-(1-(1/(G*q**m)))**N)) - (N*((1-(1/(G*q**m)))**(N-1))))
        R += math.ceil(C[m-1]/G)

    print(f'Ps = {Ps}')
    print(f'Pl = {Pl}')
    Po = 1 - math.fsum(Pl)
    T.append(1 + math.log((N - 1) / G, M) - (0.5 + (0.5772 / math.log(M))) + (1 / (2 * N * math.log(M))))
    print(f'Po = {Po}')
    print(f'C = {C}')
    print(f'R = {R}')
    print(f'T = {T}')


def tree_realisation(future_contentions, q_ary, G, num_of_used_preambs, trao, num_of_trao, resolved_users, new_num_of_trao):
    new_resolve = []
    new_trao = []
    is_there_big_gaps = True
    minimal_gap = 10000000
    for i in range(G):
        new_trao.append([])
        for j in range(q_ary):
            new_trao[i].append([])
    for i in range(len(future_contentions)):
        for j in range(len(future_contentions[i])):
            if future_contentions[i][j][2] == num_of_trao:
                trao[(future_contentions[i][j][3]) % G][random.randint(0, q_ary-1)].append(future_contentions[i][j])
                is_there_big_gaps = False

    if is_there_big_gaps:
        for i in range(len(future_contentions)):
            for j in range(len(future_contentions[i])):
                if (future_contentions[i][j][2] - num_of_trao) <= minimal_gap:
                    minimal_gap = future_contentions[i][j][2] - num_of_trao
        num_of_trao += minimal_gap
        new_num_of_trao += 1
    else:
        num_of_trao += 1
        new_num_of_trao += 1
    for i in range(len(trao)):
        for j in range(len(trao[i])):
            if len(trao[i][j]) == 1:
                trao[i][j][0][1] += 1
                new_resolve = copy.deepcopy(trao[i][j])
                resolved_users.append(new_resolve)
                trao[i][j][0].append(-1)
                new_resolve = []

            elif len(trao[i][j]) >= 2:
                num_of_used_preambs += 1
                for k in range(len(trao[i][j])):
                    trao[i][j][k][1] += 1
                    trao[i][j][k][2] += int(num_of_used_preambs/G)
                    trao[i][j][k][3] = num_of_used_preambs
    for i in range(len(future_contentions))[::-1]:
        if len(future_contentions[i]) == 0:
            del future_contentions[i]
            continue
        for j in range(len(future_contentions[i]))[::-1]:
            if len(future_contentions[i][j]) > 4:
                del future_contentions[i][j]
    for i in future_contentions:
        for j in i:
            if len(j) != 0:
                resolved_users, new_num_of_trao = tree_realisation(future_contentions, q_ary, G, num_of_used_preambs, new_trao, num_of_trao, resolved_users, new_num_of_trao)

    return resolved_users, new_num_of_trao


def tree_splitting(total_users, q_ary, total_preambs):
    G = int(total_preambs / q_ary)
    # theory(total_users, q_ary, total_preambs, G)
    initial_rao = []
    future_contentions = []
    resolved_users = []
    num_of_used_preambs = 0
    for i in range(total_preambs):
        initial_rao.append([])
    for i in range(total_users):
        initial_rao[random.randint(0, total_preambs-1)].append([i, 1, 0, 0])
    # print(f'initial_rao = {initial_rao}')
    for i in initial_rao:
        if len(i) >= 2:
            future_contentions.append(i)
        elif len(i) == 1:
            resolved_users.append(i)
    initial_trao = []
    counter = 0
    for i in range(G):
        initial_trao.append([])
        for j in range(q_ary):
            initial_trao[i].append([])
    # print(f'future contentions = {future_contentions}')
    for i in range(len(future_contentions)):
        for j in range(len(future_contentions[i])):
            future_contentions[i][j][2] = int(counter/G)
            future_contentions[i][j][3] = counter
        counter += 1
    num_of_used_preambs = len(future_contentions)
    num_of_trao = 0
    new_num_of_trao = 0
    resolved_users, num_of_trao = tree_realisation(future_contentions, q_ary, G, num_of_used_preambs, initial_trao, num_of_trao, resolved_users, new_num_of_trao)
    # print(f'resolved users = {resolved_users}')
    mean_time = 0
    max_time = 0
    for i in range(len(resolved_users)):
        mean_time += resolved_users[i][0][1]
        if resolved_users[i][0][1] >= max_time:
            max_time = resolved_users[i][0][1]

    print(f'\ntotal users = {total_users} \nq-ary = {q_ary} \ntotal number of TRAO = {num_of_trao} \n'
          f'mean number of transmission = {mean_time / total_users} \nmax transmissions = {max_time} \n---------------')

