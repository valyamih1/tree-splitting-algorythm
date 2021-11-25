import graphics as graph
import systems as sys
import generators as gen


K = 10000  # число пользователей
time = 100000  # количество окон
L = 0.375
alpha = 0.5

# [x, y, z] = sys.tree_splitting(L, time, gen.generator(L), K, alpha)
graph.graphics_tree_splitting(K, time)
