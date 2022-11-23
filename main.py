import dts
import matplotlib.pyplot as plt
import sys


sys.setrecursionlimit(1000000)
K = [1000, 5000, 10000, 20000, 30000]  # число пользователей
q_ary = [6, 9, 18]
preamb = 54
# for i in K:
#     for j in q_ary:
#         dts.tree_splitting(i, j, preamb)

# dts.tree_splitting(K, q_ary, preamb)

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
plt.plot(K, total_trao_6, label='TRAO, q = 6', marker=("."), linewidth=2, markersize=7)
plt.plot(K, total_trao_9, label='TRAO, q = 9', marker=("."), linewidth=2, markersize=7)
plt.plot(K, total_trao_18, label='TRAO, q = 18', marker=("."), linewidth=2, markersize=7)
plt.xlabel('Количество абонентов')
plt.ylabel('Количество TRAO')
plt.grid(True)
plt.legend()
plt.show()
