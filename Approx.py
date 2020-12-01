import time
import sys
sys.setrecursionlimit(100000)


def Approx(graph, cutoff_time, seed):
    start = time.time()
    print('Approximation method\n')
    visited = set()
    num_vertex = len(graph.nodes)
    non_leaf = set()

    for i in range(1, num_vertex + 1):
        if i not in visited:
            dfs(i, visited, num_vertex, graph, non_leaf)

    runtime = time.time() - start
    trace = [str(runtime) + ',' + str(len(non_leaf))]
    if cutoff_time < runtime:
        return set(), []
    else:
        return non_leaf, trace


def dfs(i, visited: set, number_vertex: int, graph, non_leaf):
    visited.add(i)
    for neighbor in list(graph[i]):
        if neighbor not in visited:
            visited.add(neighbor)
            non_leaf.add(i)
            dfs(neighbor, visited, number_vertex, graph, non_leaf)
