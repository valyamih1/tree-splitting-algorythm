import matplotlib.pyplot as plt
import systems as sys
import generators as gen
import  DTS_RACH as dts
import tree_RACH as tree


def grahpics_for_tree_rach():
    # K = [1000, 5000, 10000, 20000, 30000]  # число пользователей
    ### hardcoded values from working script in PyPy, just to make plots in CPython ###
    transm_6 = [3.417, 4.3392, 4.7341, 5.1317, 5.3583]
    transm_9 = [3.112, 3.8168, 4.1402, 4.4556, 4.6156]
    transm_18 = [2.68, 3.253, 3.4693, 3.7474, 3.91016]
    transm_rao = [3, 9.1, 10, 10, 10]
    total_trao_6 = [128, 625, 1293, 2559, 3898]
    total_trao_9 = [143, 636, 1336, 2594, 3717]
    total_trao_18 = [143, 735, 1391, 2988, 4761]
    plt.figure(1)

    # plt.plot(K, transm_rao, label='10 RAO', marker=("."), linewidth=2, markersize=7)
    # plt.plot(K, total_trao_6, label='TRAO, q = 6', marker=".", linewidth=2, markersize=7, linestyle='-.')
    # plt.plot(K, total_trao_9, label='TRAO, q = 9', marker=".", linewidth=2, markersize=7, linestyle=':')
    # plt.plot(K, total_trao_18, label='TRAO, q = 18', marker=".", linewidth=2, markersize=7, linestyle='--')
    plt.xlabel('Number of devices')
    plt.ylabel('Number of TRAO')
    plt.grid(True)
    plt.legend()
    plt.show()


def graphics_tree_splitting(K, time):
    values_out_pr = []
    values_d_pr = []
    alpha = 0.5
    # array_range = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]
    array_range = [0.1, 0.2, 0.3, 0.32, 0.34, 0.35, 0.36, 0.37, 0.375, 0.376, 0.377, 0.378, 0.379, 0.38, 0.39, 0.4, 0.5]
    delay_range = [5, 10, 20, 50, 100, 200, 500]
    users_range = [10, 20, 50, 100, 200, 500]
    for l in array_range:
        values_users_pr = []
        print('lambda = ' + str(l))
        [u_pr, d_pr, out_pr] = sys.tree_splitting(l, time, gen.generator(l), K, alpha)
        values_users_pr.append(u_pr)
        values_d_pr.append(d_pr)
        values_out_pr.append(out_pr)


    plt.figure(1)
    # for i in range(len(delay_range)):
    plt.plot(array_range, values_out_pr, label='Улучшенный древовидный алгоритм', marker=("."), linewidth=2, markersize=7)
    plt.plot(array_range,array_range, label='Линия 45 градусов', marker=("."), linewidth=2, markersize=7)
    plt.xlabel('Входная интенсивность')
    plt.ylabel('Выходная интенсивность')
    plt.grid(True)
    plt.legend()
    plt.show()
    # plt.title('aloha: average out')
    # plt.show()
