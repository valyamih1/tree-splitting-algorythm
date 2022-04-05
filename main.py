import graphics as graph
import systems as sys
import generators as gen


K = 100  # число пользователей
time = 10000  # количество окон
L = 0.375
alpha = 0.5
q_ary = 2
preamb = 4

[x, y, z] = sys.tree_splitting(L, time, gen.generator(L), K, alpha, q_ary, preamb)
# graph.graphics_tree_splitting(K, time)
