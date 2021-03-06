import numpy as np
import time
def LS2(graph, cut_time, seed):
    print('LS2 local search Simulated Annealing method\n')
    # initialization
    trace = []
    np.random.seed(seed)
    vertex_set = set(graph.nodes)
    T = 1.0
    alpha = 0.90
    start_time = time.time()
    while time.time() - start_time < cut_time:
        non_visited = set(graph.nodes)
        while True:
            if len(non_visited) == 0:
                return
            random_vertex = np.random.choice(list(non_visited))
            non_visited.remove(random_vertex)
            temp_set = vertex_set.copy()
            if (random_vertex in temp_set):
                temp_set.remove(random_vertex)
            else:
                temp_set.add(random_vertex)
            if isValid(temp_set, graph.edges):
                break
        old_cost = len(vertex_set)
        new_cost = len(temp_set)
        acceptance_probability = np.exp(np.array((old_cost - new_cost) / T, dtype=np.float128))
        if acceptance_probability > np.random.random():
            trace.append(str(time.time() - start_time) + ',' + str(new_cost))
            vertex_set= temp_set
        elif new_cost < old_cost:
            trace.append(str(time.time() - start_time) + ',' + str(new_cost))
            vertex_set= temp_set
        T = T * alpha
    
    return vertex_set, trace

def isValid(curSet, edges):
    for u, v in edges:
        if (u not in curSet and v not in curSet):
            return False
    return True

