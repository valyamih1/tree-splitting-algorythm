import graphics as graph
import systems as sys
import generators as gen


K = 5000  # число пользователей
# time = 10000  # количество окон
# L = 0.375
alpha = 0.5
q_ary = 18
preamb = 54

sys.tree_splitting(K, q_ary, preamb)
# graph.graphics_tree_splitting(K, time)
