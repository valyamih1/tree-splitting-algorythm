import numpy
import matplotlib.pyplot as plt
import systems as sys
import generators as gen


def graphics_tree_splitting(K, time):
    values_out_pr = []
    values_d_pr = []
    alpha = 0.5
    # array_range = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]
    array_range = [0.1, 0.2, 0.3, 0.32, 0.34, 0.35, 0.36, 0.365, 0.367, 0.37, 0.375, 0.376, 0.377, 0.378, 0.379, 0.38, 0.39, 0.4]
    delay_range = [5, 10, 20, 50, 100, 200, 500]
    users_range = [10, 20, 50, 100, 200, 500]
    for l in array_range:
        values_users_pr = []
        print('lambda = ' + str(l))
        [u_pr, d_pr, out_pr] = sys.tree_splitting(l, time, gen.generator(l), K, alpha)
        values_users_pr.append(u_pr)
        values_d_pr.append(d_pr)
        values_out_pr.append(out_pr)
    # plt.figure(1)
    # plt.plot(array_range, values_users_pr, label=('Реализация алгоритма из [1]'), marker=("."), linewidth=2, markersize=7)
    # plt.xlabel('Входная интенсивность')
    # plt.ylabel('Среднее кол-во сообщений')
    # plt.grid(True)
    # plt.legend()
    # # plt.title('aloha: average msg')
    # plt.show()
    #
    # plt.figure(2)

    # for i in range(len(users_range)):
    # plt.plot(delay_range, values_d_pr, label='Реализация алгоритма из [1]', marker=("."), linewidth=2, markersize=7)
    #
    # plt.xlabel('Значение интервала отсрочки')
    # plt.ylabel('Средняя задержка')
    # plt.grid(True)
    # plt.legend()
    # # plt.title('aloha: average d0')
    # plt.show()

    plt.figure(1)
    # for i in range(len(delay_range)):
    plt.plot(values_d_pr, values_out_pr, label='Улучшенный древовидный алгоритм', marker=("."), linewidth=2, markersize=7)
    plt.plot(values_d_pr,values_d_pr, label='Линия 45 градусов', marker=("."), linewidth=2, markersize=7)
    plt.xlabel('Входная интенсивность')
    plt.ylabel('Выходная интенсивность')
    plt.grid(True)
    plt.legend()
    # plt.title('aloha: average out')
    plt.show()

    # plt.show()
