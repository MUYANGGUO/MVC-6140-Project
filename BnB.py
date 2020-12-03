import time
import sys
sys.setrecursionlimit(25000)

def BnB(graph,timelim):
    print('Exact BnB method, DFS\n')
    # start_time = time.time()



    global startTime
    startTime = time.time()
    global trace
    trace=[]
    V = len(graph.nodes)

    # create dictionaries to map sorted numbers onto graph node numbers (unsorted and missing some numbers)
    C = list(range(1, V + 1))
    global dict1
    global dict2
    dict1 = dict(zip(C, list(graph.nodes)))
    dict2 = dict(zip(list(graph.nodes), C))

    M = V # minimum cover size, initialize as |V|
    covered=[] # stores covered nodes
    uncovered=[] # stores uncovered nodes
    free = list(graph.nodes) # stores free nodes, initialize as all nodes
    best = [] # best solution (don't have one yet)
    ct=0
    uncovE=list(graph.edges)
    d=[0]*max(list(graph.nodes))
    for v in free:
        d[v-1]=len(graph.adj[v])
    min, Cover = minCover(graph, M, covered, uncovered, free, best,V,ct,uncovE,d,timelim)
    #print('time spent: %f s\n' %(time.time() - startTime))
    if len(Cover)==0:
        Cover=list(graph.nodes)
    CoverSet=set(Cover)
    return CoverSet, trace


def minCover(graph,M,covered,uncovered,free,best,V,ct,uncovE,d,timelim):
    currentTime=time.time()-startTime
    if currentTime>=timelim:
        return M, best
    if len(covered)>=M: # return if number covered is already bigger than best solution
        return M, best
    if len(uncovE)==0: # all edges covered, a solution is reached
        if len(covered)<M: # if size of the new solution smaller than size of existing solution
            best=covered[:] # new solution becomes best solution
            M=len(best) # global LB becomes length of new solution
            #print('new best solution: ', M)
            #print('time: ', time.time() - startTime)
            trace.append(str(time.time() - startTime) + ',' + str(M))
        return M, best

    # if there's no free node anymore, return
    if len(free)==0:
        return M,best
    # otherwise, proceed to evaluate LB
    Mlocal = len(covered)+len(free)
    dfree=[]
    for i in range(0,len(free)):
        dfree.append(d[free[i]-1])
    freeSorted=[x for _, x in sorted(zip(dfree, free), reverse=True)] # sort free nodes by descending degree
    sum = 0
    for i in range(0, len(freeSorted)): # LB is minimum VC size given current partial solution
        sum = sum + d[freeSorted[i]-1]
        if sum >= len(uncovE):
            Mlocal = len(covered) + i+1
            break
    if Mlocal>=M: # if local LB >= global LB, exit
        return M, best

    free1=free[:]
    covered1=covered[:]
    uncovered1=uncovered[:]
    # pick the free node with largest degree and decide whether it's covered or uncovered
    nxt=freeSorted[0]
    free1.remove(nxt)
    covered1.append(nxt)
    d1=d[:]
    uncovE1=uncovE[:]
    for v in list(graph.adj[nxt]):
        d1[v-1]=d1[v-1]-1
        try:
            uncovE1.remove((v,nxt))
        except ValueError:
            pass
        try:
            uncovE1.remove((nxt,v))
        except ValueError:
            pass
    uncovered1.append(nxt)

    # branch 1: mark nxt as covered
    M1, best1 = minCover(graph, M, covered1, uncovered, free1,best,V,ct,uncovE1,d1,timelim)

    # branch 2: mark nxt as uncovered
    M2, best2 = minCover(graph,M1,covered,uncovered1,free1,best1,V,ct,uncovE,d,timelim)

    # return
    return M2, best2



