import numpy as np
import time
def LS2(graph, cut_time, seed):
    print('LS2 local search Simulated Annealing method\n')
    # initialization
    np.random.seed(seed)
    vertex_set = set(graph.nodes)
    start_time = time.time()
    while time.time() - start_time < cut_time:
        pass
    pass