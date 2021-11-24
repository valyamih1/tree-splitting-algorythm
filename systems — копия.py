import random
import generators as gen
import numpy as np
import math


def binary_tree(alpha, num_user_msg_to_send, time, to_send_tree):
    down_ancestor = []
    # if len(num_user_msg_to_send) == 4:
    #     print(1)
    up_ancestor = []
    down_ancestor.clear()
    up_ancestor.clear()
    resolution_time = 0
    for i in range(len(num_user_msg_to_send)):
        p = random.random()
        if p < alpha:
            down_ancestor.append(num_user_msg_to_send[i])
        else:
            up_ancestor.append(num_user_msg_to_send[i])
    if len(up_ancestor) > 1:
        resolution_time = time + 1
        resolution_time, to_send_tree = binary_tree(alpha, up_ancestor, resolution_time, to_send_tree)
        if len(down_ancestor) == 0:
            resolution_time = resolution_time + 1
        if len(down_ancestor) == 1:
            resolution_time = resolution_time + 1
            to_send_tree.append([resolution_time, down_ancestor[0][0], down_ancestor[0][1]])
        if len(down_ancestor) > 1:
            resolution_time = resolution_time + 1
            resolution_time, to_send_tree = binary_tree(alpha, down_ancestor, resolution_time, to_send_tree)
    if len(up_ancestor) == 1:
        resolution_time = time + 1
        to_send_tree.append([resolution_time, up_ancestor[0][0], up_ancestor[0][1]])
        if len(down_ancestor) == 1:
            resolution_time = resolution_time + 1
            to_send_tree.append([resolution_time, down_ancestor[0][0], down_ancestor[0][1]])
        else:
            resolution_time = resolution_time + 1
            resolution_time, to_send_tree = binary_tree(alpha, down_ancestor, resolution_time, to_send_tree)
    if len(up_ancestor) == 0:
        resolution_time = time + 1
        up_ancestor = down_ancestor
        down_ancestor = []
        resolution_time, to_send_tree = binary_tree(alpha, up_ancestor, resolution_time, to_send_tree)

    return resolution_time, to_send_tree

def tree_splitting(lambda_in, N, cube, K, B, alpha):  # alpha = 1
    time = 0
    user_buffers = []
    msg_come = 0
    sum_msg = 0
    sum_msg_out = 0
    user_packets = []
    user_out = []
    user_out_tree = []

    lambda_g = 0
    tree_splitting_time = []
    resolution_time = 0
    multiplicity =[]
    for i in range(K):
        tree_splitting_time.append(0)
        multiplicity.append(0)
        user_packets.append(0)
        user_buffers.append([])
        user_out.append(0)
        user_out_tree.append(0)
    come_and_out = []
    while time != N:
        if time % 10000 == 0:
            print(str(time))
        num_user_msg_to_send = []
        # if len(user_buffers) > 3:
        for i in range(len(user_buffers)):
            if len(user_buffers[i]) != 0:
                for j in range(len(user_buffers[i])):
                    if math.floor(user_buffers[i][j][1]) == time - 1: # new packet
                        if time > resolution_time:
                            to_send = [i, j]
                            num_user_msg_to_send.append(to_send)
                        else:
                            user_buffers[i][j][2] = -1
                            user_buffers[i][j][3] = resolution_time - time
                    else:
                        if user_buffers[i][0][3] - user_buffers[i][0][2] == 0:  # если один и истек
                            if time > resolution_time:
                                to_send = [i, j]
                                num_user_msg_to_send.append(to_send)
                            # else:
                            #     user_buffers[i][j][2] = -1
                            #     user_buffers[i][j][3] = resolution_time - time

        if len(num_user_msg_to_send) == 1:
            sum_msg_out = sum_msg_out + 1
            come_and_out.append([user_buffers[num_user_msg_to_send[0][0]][num_user_msg_to_send[0][1]][1], time])
            user_buffers[num_user_msg_to_send[0][0]].pop(num_user_msg_to_send[0][1])
        to_send_tree = []
        for i in range(K):
            user_out_tree[i] = 0
        number_of_packet_from_same_user = []
        if len(num_user_msg_to_send) > 1:
            resolution_time, to_send_tree = binary_tree(alpha, num_user_msg_to_send, time, to_send_tree)
            # print(len(to_send_tree))
            tree_splitting_time[len(to_send_tree)-2] += resolution_time - time
            multiplicity[len(to_send_tree)-2] += 1
        if_zero_wasnt_first = []
        if_zero_was_first = []
        for i in range(len(to_send_tree)):
            sum_msg_out = sum_msg_out + 1
            come_and_out.append([user_buffers[to_send_tree[i][1]][to_send_tree[i][2]][1], to_send_tree[i][0]])
            user_out_tree[to_send_tree[i][1]] += 1
            if user_out_tree[to_send_tree[i][1]] > 1:
                number_of_packet_from_same_user.append(to_send_tree[i])
                if_zero_wasnt_first.append(0)
                if_zero_was_first.append(0)
        for i in range(len(to_send_tree)):
            if len(number_of_packet_from_same_user) > 0:
                for j in range(len(number_of_packet_from_same_user)):
                    if to_send_tree[i][1] == number_of_packet_from_same_user[j][1] and to_send_tree[i][2] > 0:
                        user_buffers[to_send_tree[i][1]].pop(to_send_tree[i][2])
                        if_zero_wasnt_first[j] = 1
                    if to_send_tree[i][1] == number_of_packet_from_same_user[j][1] and to_send_tree[i][2] == 0:
                        if if_zero_wasnt_first[j] == 1:
                            user_buffers[to_send_tree[i][1]].pop(0)
                        else:
                            if_zero_was_first[j] = 1
                            break
                    if if_zero_was_first[j] == 1 and to_send_tree[i][1] == number_of_packet_from_same_user[j][1]:
                        user_buffers[to_send_tree[i][1]].pop(0)
            else:
                user_buffers[to_send_tree[i][1]].pop(to_send_tree[i][2])

        # print("ap_buffer : " + str(ap_buffer))
        p = random.random()
        cur_msg = gen.generate_msg(p, cube)
        time_arr = gen.get_time_array(cur_msg)
        msg_come = msg_come + cur_msg
        msg_in_system = 0
        for i in range(len(user_buffers)):
            msg_in_system = msg_in_system + len(user_buffers[i])
        if K != 0:
            sum_msg = sum_msg + msg_in_system + cur_msg
        # print("cur_msg: " + str(cur_msg))
        user_msg = []
        if cur_msg <= K:
            user_msg = random.sample(range(0, K), cur_msg)
        else:
            while cur_msg > K:
                user_msg = random.sample(range(0, K), K)
                cur_msg = cur_msg - K
            user_msg = user_msg + random.sample(range(0, K), cur_msg)
        # print("msg is appeared from: " + str(user_msg))
        t = 0
        for i in range(len(user_msg)):
            user_packets[user_msg[i]] = user_packets[user_msg[i]] + 1
            user_buffers[user_msg[i]].append([1, round(time + time_arr[t], 3), -1, 1, user_packets[user_msg[i]]]) # 1 - есть сообщение, time - номер слота возникновения, b = -1 - задержка
            t = t + 1
        for i in range(len(user_buffers)):
            for j in range(len(user_buffers[i])):
                if user_buffers[i][j][3] - user_buffers[i][j][2] < 0:
                    b = random.randint(1, B)
                    user_buffers[i][j][2] = -1
                    user_buffers[i][j][3] = b
                user_buffers[i][j][2] = user_buffers[i][j][2] + 1
        # print("user_buffers: " + str(user_buffers))
        # print("-------------------------------------")
        time = time + 1
    sum_d = 0
    for i in range(len(come_and_out)):
        sum_d = sum_d + come_and_out[i][1] - come_and_out[i][0] + 1
    # if (len(user_buffers) != 0):
    #     for k in range(len)
    if (len(come_and_out)) == 0:
        average_delay = 0
    else:
        average_delay = sum_d / len(come_and_out)
    # average_delay = sum_d/(len(come_and_out))
    # if len(come_and_out) != 0:
    #     print("average delay = " + str(average_delay))
    lambda_out = len(come_and_out) / time
    lambda_pr = msg_come / N
    average_msg = sum_msg / N
    ti = 0
    out = 0
    for i in range(len(user_out)):
        out = out + user_out[i]
        ti = ti + (user_out[i]/N)
        lambda_g = lambda_g + (user_packets[i] / N)
    # resol_mult_time = tree_splitting_time[0]/multiplicity[0]
    print("--------------------------")
    # print("cube = " + str(cube))
    print("lambda = " + str(lambda_in))
    print("lambda practice = " + str(lambda_pr))
    print("lambda_out = " + str(lambda_out))
    print("average delay = " + str(average_delay))
    print("average msg = " + str(average_msg))
    # print("user packets = " + str(user_packets))
    print("tree_splitting_time = " + str(tree_splitting_time))
    print("multiplicity = " + str(multiplicity))
    # print("out packets 1= " + str(len(come_and_out)))
    for i in range(len(multiplicity)):
        if multiplicity[i] > 10:
            print("resolution time for " + str(i+2) +" collisions = " + str(tree_splitting_time[i] / multiplicity[i]))
    # print("come and out = " + str(come_and_out))
    return average_msg, average_delay, lambda_out


