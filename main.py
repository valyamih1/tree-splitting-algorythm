import tree_RACH
import matplotlib.pyplot as plt
import sys
import DTS_RACH
import numpy as np

sys.setrecursionlimit(1000000)
# K = [1000, 5000, 10000, 20000, 30000]  # число пользователей
# K = [1, 6, 11, 16, 21, 26, 31, 36, 41, 46, 51, 56, 61, 66, 71, 76, 81, 86, 91, 96, 101]
K = np.arange(1, 20007, 50)
q_ary = 18
    # , 9, 18]
preamb = 54
delay = []
with open('delay with 1 to 20000 devices, step 50.txt') as f:
    lines = f.read()
delay = lines.split(', ')
delays = []
for i in delay:
    delays.append(float(i))
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

# tree_RACH.tree_splitting(K, q_ary, preamb)
DTS_RACH.dynamic_tree_splitting()
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
plt.plot(K, delays, label='TRAO, q = 6', marker=".", linewidth=2, markersize=7, linestyle='-.')
# plt.plot(K, total_trao_9, label='TRAO, q = 9', marker=".", linewidth=2, markersize=7, linestyle=':')
# plt.plot(K, total_trao_18, label='TRAO, q = 18', marker=".", linewidth=2, markersize=7, linestyle='--')
plt.xlabel('Number of devices')
plt.ylabel('Number of TRAO')
plt.grid(True)
plt.legend()
plt.show()
