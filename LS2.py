import numpy as np
import timeit
def LS2(graph, cut_time, seed):
    print('LS2 local search Simulated Annealing method\n')
    # initialization
    trace = []
    np.random.seed(seed)
    vertex_set = set(graph.nodes)
    T = 1.0
    alpha = 0.90
    start_time = timeit.default_timer()
    while timeit.default_timer() - start_time < cut_time:
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
            is_valid = True
            for u, v in graph.edges():
                if (u not in temp_set and v not in temp_set):
                    is_valid = False
                    break
            if is_valid:
                break
        old_cost = len(vertex_set)
        new_cost = len(temp_set)
        acceptance_probability = np.exp(np.array((old_cost - new_cost) / T, dtype=np.float128))
        if acceptance_probability > np.random.random():
            vertex_set= temp_set
            if new_cost < old_cost:
                trace.append(str(timeit.default_timer() - start_time) + ',' + str(new_cost))
        T = T * alpha
    return trace

