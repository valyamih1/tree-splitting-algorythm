import tree_RACH
import matplotlib.pyplot as plt
import sys
import DTS_RACH
import numpy as np
import standard_random_access as sra
import tree_RACH


def tree_rach_graphs():
    sys.setrecursionlimit(1000000)
    # K = [1000, 5000, 10000, 20000, 30000]  # число пользователей
    # K = [1, 6, 11, 16, 21, 26, 31, 36, 41, 46, 51, 56, 61, 66, 71, 76, 81, 86, 91, 96, 101]
    K = np.arange(5000, 50001, 5000)
    q_ary = [6, 9, 18]
    preamb = 54
    delay = []
    # with open('delay with 1 to 20000 devices, step 50.txt') as f:
    #     lines = f.read()
    # delay = lines.split(', ')
    # delays = []
    # for i in delay:
    #     delays.append(float(i))
    # K = []
    # for i in range(1, 2502, 5):
    #     K.append(i)
    # print(K)
    # for i in K:
    #     print(i)
    #     mean_delay = 0
    #     for j in range(500):
    #         mean_delay += tree_RACH.tree_splitting(i, q_ary, preamb)
    #     delay.append(48*mean_delay/500)
    tree_RACH.tree_splitting(K, q_ary, preamb)
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
    # plt.plot(K, delays, label='TRAO, q = 6', marker=".", linewidth=2, markersize=7, linestyle='-.')
    # plt.plot(K, total_trao_9, label='TRAO, q = 9', marker=".", linewidth=2, markersize=7, linestyle=':')
    # plt.plot(K, total_trao_18, label='TRAO, q = 18', marker=".", linewidth=2, markersize=7, linestyle='--')
    plt.xlabel('Number of devices')
    plt.ylabel('Number of TRAO')
    plt.grid(True)
    plt.legend()
    plt.show()


def dts_rach_graphs(kmax):
    K = np.arange(5000, 50007, 5000)
    throughputs = []
    delays = []
    rates = []
    transms = []
    sra_rates = []
    sra_delays = []
    sra_transm = []
    sra_thrs = []
    # throughputs_100 = []
    # delays_100 = []
    # rates_100 = []
    # transms_100 = []
    # sra_rates_100 = []
    # sra_delays_100 = []
    # sra_transm_100 = []
    # m = 50
    # for j in range(len(K)):
    #     throughputs_100.append(0)
    #     delays_100.append(0)
    #     rates_100.append(0)
    #     transms_100.append(0)
    #     sra_rates_100.append(0)
    #     sra_delays_100.append(0)
    #     sra_transm_100.append(0)
    # for j in range(m):

    for i in K:
        th, delay, rate, transm, sra_rate, sra_delay, sra_tr, sra_thr = DTS_RACH.dynamic_tree_splitting(i,kmax)
        throughputs.append(th)
        delays.append(delay)
        rates.append(rate)
        transms.append(transm)
        sra_rates.append(sra_rate)
        sra_delays.append(sra_delay)
        sra_transm.append(sra_tr)
        sra_thrs.append(sra_thr)
        # for i in range(len(K)):
        #     throughputs_100[i] += throughputs[i] / m
        #     delays_100[i] += delays[i] / m
        #     rates_100[i] += rates[i] / m
        #     transms_100[i] += transms[i] / m
        #     sra_delays_100[i] += sra_delays[i] / m
        #     sra_transm_100[i] += sra_transm[i] / m
        #     sra_rates_100[i] += sra_rates[i] / m

    plt.figure(1)
    # plt.ylim(0, 0.4)
    # plt.xlim(5000, 50000)
    plt.plot(K, throughputs, label='DTS Mean Throughput', marker=".", linewidth=2, markersize=7)
    plt.plot(K, sra_thrs, label='SRA Mean Throughput', marker=".", linewidth=2, markersize=7, linestyle='--')
    plt.xlabel('Number of devices')
    plt.ylabel('Mean Throughput')
    plt.grid(True)
    plt.legend()
    plt.show()

    plt.figure(2)
    # plt.ylim(0, 1600)
    # plt.xlim(5000, 50000)
    plt.plot(K, delays, label='DTS Mean delay', marker=".", linewidth=2, markersize=7)
    plt.plot(K, sra_delays, label='SRA Mean delay', marker=".", linewidth=2, markersize=7, linestyle='--')
    plt.xlabel('Number of devices')
    plt.ylabel('Mean delay')
    plt.grid(True)
    plt.legend()
    plt.show()

    plt.figure(3)
    # plt.ylim(0, 1)
    # plt.xlim(5000, 50000)
    plt.plot(K, rates, label='DTS Success rate', marker=".", linewidth=2, markersize=7)
    plt.plot(K, sra_rates, label='SRA Success rate', marker=".", linewidth=2, markersize=7, linestyle='--')
    plt.xlabel('Number of devices')
    plt.ylabel('Success rate')
    plt.grid(True)
    plt.legend()
    plt.show()

    plt.figure(4)
    # plt.ylim(0, 10)
    # plt.xlim(5000, 50000)
    plt.plot(K, transms, label='DTS Mean number of transmissions', marker=".", linewidth=2, markersize=7)
    plt.plot(K, sra_transm, label='SRA Mean number of transmissions', marker=".", linewidth=2, markersize=7, linestyle='--')
    plt.xlabel('Number of devices')
    plt.ylabel('Transmissions')
    plt.grid(True)
    plt.legend()
    plt.show()

if __name__ == "__main__":
    dts_rach_graphs(8)
    # th, delay, rate, transm = DTS_RACH.dynamic_tree_splitting(50000, 8)

    # sra.graphs()