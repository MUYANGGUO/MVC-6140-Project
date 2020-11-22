import time
import sys
sys.setrecursionlimit(100000)

def Approx(graph, cutoff_time, seed):
    print('Approximate method\n')

    success, runtime, vertex_cov, vc_size = dfsMVC(graph, cutoff_time)
    if not success:
        print("No enough cutoff time to produce a result.\n")
        return set(), []
    else:
        trace = []
        vertex_cover = set()
        for i in range(1, vc_size):
            vertex_cover.add(vertex_cov[i])
        trace.append(str(runtime) + ',' + str(vc_size))
        return vertex_cover, trace


def dfsMVC(graph, cutoff_time):
    start = time.time()
    vertex_cov = []
    visited = set()
    visited.add(0)
    num_vertex = len(graph.nodes)
    vc_size = 0
    success = True
    for i in range(1, num_vertex):
        vc_size = dfs(i, visited, graph, vertex_cov, num_vertex, vc_size, start, cutoff_time)
        if time.time() - start > cutoff_time:
            success = False
            break
    if success:
        end = time.time()
        runtime = end-start
        return success, runtime, vertex_cov, vc_size
    else:
        return success, 0, vertex_cov, vc_size


def dfs(i, visited: set, graph, vertex_cov: list, num_vertex: int, vc_size: int, start, cutoff_time) -> int:
    counter = 1
    visited.add(i)
    is_leaf = True
    while counter < num_vertex + 1 and is_leaf:
        if counter not in visited and graph.has_edge(i, counter):
            is_leaf = False
        counter += 1

    if not is_leaf:
        vc_size += 1
        vertex_cov.append(i)

    for k in range(num_vertex + 1):
        if time.time() - start > cutoff_time:
            break
        if graph.has_edge(i, k) and k not in visited:
            vc_size = dfs(k, visited, graph, vertex_cov, num_vertex, vc_size, start, cutoff_time)

    return vc_size