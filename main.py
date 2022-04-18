import graphics as graph
import systems as sys
import generators as gen
# import random
# import matplotlib.pyplot as plt
#
# N = 500
# x = range(N)
# y = [random.randint(0, 18) for i in x]
# plt.plot(x, y, 'o')
# plt.show()
# plt.hist(y, 1)
# plt.show()

K = 50  # число пользователей
# time = 10000  # количество окон
# L = 0.375
# alpha = 0.5
q_ary = 4
preamb = 8

sys.tree_splitting(K, q_ary, preamb)
# graph.graphics_tree_splitting(K, time)
