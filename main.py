import matplotlib.pyplot as plt
import sys
import DTS_RACH
import numpy as np
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
    throughputssic = []
    delayssic = []
    ratessic = []
    transmssic = []
    sra_rates = []
    sra_delays = []
    sra_transm = []
    sra_thrs = []
    sra_thrs_paper = [0.08, 0.065, 0.055, 0.049, 0.0482, 0.048, 0.0479, 0.0478, 0.04775, 0.0477]
    TA_6_delay = [243.80212084833934, 478.2779223378703, 728.3368680805655, 982.8626489138052, 1235.6117481956696, 1495.2888146911519, 1750.5122530775836, 1991.0830911823648, 2205.412817023934, 2444.9148632914444]
    TA_9_delay = [243.196, 528.5485097019404, 785.4534542544678, 994.4384, 1224.7169373549884, 1445.1145, 1681.3753000342897, 1919.7270704140828, 2190.578725106686, 2485.599207778178]
    TA_18_delay = [298.6214, 517.1087, 805.2345333333334, 1198.5119, 1588.99976, 2030.4319666666668, 2432.1525428571426, 2809.2278, 3186.4480222222223, 3498.74298]
    TA_6_transm = [4.348339335734294, 4.722077662129704, 4.957316259837269, 5.118280108118931, 5.242662389735365, 5.347946577629382, 5.434411680503865, 5.5069138276553105, 5.559969663848676, 5.62259605733328]
    TA_9_transm = [3.8254, 4.1562312462492494, 4.3352894105094695, 4.44585, 4.547563805104408, 4.626966666666666, 4.6973082638015775, 4.754650930186037, 4.813611308677098, 4.870883847477294]
    TA_18_transm = [3.2622, 3.4707, 3.615666666666667, 3.74605, 3.83568, 3.9158333333333335, 3.9757714285714285, 4.022175, 4.064755555555555, 4.09624]
    TA_6_thr = [0.14445022245334257, 0.1457840819542947, 0.14373440798311266, 0.14229119461901302, 0.14250462677359654, 0.14397414812891313, 0.14599852788651344, 0.14368871886864495, 0.14671057790323846, 0.14655420864726884]
    TA_9_thr = [0.14627581768182085, 0.13351491361585088, 0.13937670736466523, 0.14381877022653722, 0.1474404340646379, 0.14595862283723554, 0.14614388909766587, 0.14634057096021136, 0.1452236618699927, 0.14293802758904672]
    TA_18_thr = [0.12072045970351056, 0.13284446569955896, 0.1321492758219685, 0.1231284475965327, 0.1182234328301744, 0.11405369648030293, 0.1145947928126146, 0.11283179600011284, 0.11239996403201151, 0.11194848578478128]
    ta_6_rate = [0.9996, 0.9992, 0.99933, 0.9989, 0.9984, 0.99853, 0.99794, 0.99715, 0.99693, 0.9964]
    ta_9_rate = [1, 1, 1, 1, 0.99992, 0.99993, 0.99994, 0.9999, 0.99978, 0.99976]
    ta_18_rate = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
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
    ta_18_delays = []
    for i in K:
        th, delay, rate, transm, sra_rate, sra_delay, sra_tr, sra_thr = DTS_RACH.dynamic_tree_splitting(i,kmax, 0)
        thsic, delaysic, ratesic, transmsic, sra_rate, sra_delay, sra_tr, sra_thr = DTS_RACH.dynamic_tree_splitting(i, kmax, 8)
        throughputs.append(th)
        delays.append(delay)
        rates.append(rate)
        transms.append(transm)
        throughputssic.append(thsic)
        delayssic.append(delaysic)
        ratessic.append(ratesic)
        transmssic.append(transmsic)
        sra_rates.append(sra_rate)
        sra_delays.append(sra_delay)
        sra_transm.append(sra_tr)
        sra_thrs.append(sra_thr)

    plt.figure(1)
    plt.ylim(0, 0.4)
    plt.xlim(5000, 50000)
    plt.plot(K, throughputssic, label='DTS+SIC Throughput', marker=".", linewidth=2, markersize=7)
    plt.plot(K, throughputs, label='DTS Throughput', marker=".", linewidth=2, markersize=7)
    plt.plot(K, sra_thrs_paper, label='SRA Throughput', marker=".", linewidth=2, markersize=7, linestyle='--')
    plt.plot(K, TA_6_thr, label='Throughput, q=6', marker=".", linewidth=2, markersize=7)
    plt.plot(K, TA_9_thr, label='Throughput, q=9', marker=".", linewidth=2, markersize=7)
    plt.plot(K, TA_18_thr, label='Throughput, q=18', marker=".", linewidth=2, markersize=7)
    # plt.plot(K, ta_18_delays, label='q-ary, q=18 theory', marker=".", linewidth=2, markersize=7)
    plt.xlabel('Number of devices')
    plt.ylabel('Mean Throughput')
    plt.grid(True)
    plt.legend()
    plt.show()

    plt.figure(2)
    # plt.ylim(0, 1600)
    # plt.xlim(5000, 50000)
    plt.plot(K, delayssic, label='DTS+SIC delay', marker=".", linewidth=2, markersize=7)
    plt.plot(K, delays, label='DTS delay', marker=".", linewidth=2, markersize=7)
    plt.plot(K, sra_delays, label='SRA delay', marker=".", linewidth=2, markersize=7, linestyle='--')
    plt.plot(K, TA_6_delay, label='Delay, q=6', marker=".", linewidth=2, markersize=7)
    plt.plot(K, TA_9_delay, label='Delay, q=9', marker=".", linewidth=2, markersize=7)
    plt.plot(K, TA_18_delay, label='Delay, q=18', marker=".", linewidth=2, markersize=7)

    plt.xlabel('Number of devices')
    plt.ylabel('Mean delay')
    plt.grid(True)
    plt.legend()
    plt.show()

    plt.figure(3)
    # plt.ylim(0, 1)
    # plt.xlim(5000, 50000)
    plt.plot(K, ratessic, label='DTS+SIC Success rate', marker=".", linewidth=2, markersize=7)
    plt.plot(K, rates, label='DTS Success rate', marker=".", linewidth=2, markersize=7)
    # plt.plot(K, sra_rates, label='SRA Success rate', marker=".", linewidth=2, markersize=7, linestyle='--')
    plt.plot(K, ta_6_rate, label='Success rate, q=6', marker=".", linewidth=2, markersize=7)
    plt.plot(K, ta_9_rate, label='Success rate, q=9', marker=".", linewidth=2, markersize=7)
    plt.plot(K, ta_18_rate, label='Success rate, q=18', marker=".", linewidth=2, markersize=7)
    plt.xlabel('Number of devices')
    plt.ylabel('Success rate')
    plt.grid(True)
    plt.legend()
    plt.show()

    plt.figure(4)
    plt.ylim(0, 10)
    plt.xlim(5000, 50000)
    plt.plot(K, transmssic, label='DTS+SIC transmissions', marker=".", linewidth=2, markersize=7)
    plt.plot(K, transms, label='DTS transmissions', marker=".", linewidth=2, markersize=7)
    plt.plot(K, sra_transm, label='SRA transmissions', marker=".", linewidth=2, markersize=7, linestyle='--')
    plt.plot(K, TA_6_transm, label='Transmissions, q=6', marker=".", linewidth=2, markersize=7)
    plt.plot(K, TA_9_transm, label='Transmissions, q=9', marker=".", linewidth=2, markersize=7)
    plt.plot(K, TA_18_transm, label='Transmissions, q=18', marker=".", linewidth=2, markersize=7)
    plt.xlabel('Number of devices')
    plt.ylabel('Transmissions')
    plt.grid(True)
    plt.legend()
    plt.show()


if __name__ == "__main__":
    dts_rach_graphs(8)

