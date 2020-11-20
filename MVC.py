# system
import os
import time
import argparse
# libs
import numpy as np
import math as math
import networkx as nx
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from collections import OrderedDict
import json
# modules
from BnB import BnB
from LS1 import LS1
from LS2 import LS2
from Approx import Approx
# precision control
np.set_printoptions(precision=20)

def parseArguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', help = 'name of the data file', type = str)
    parser.add_argument('alg', help = 'alg method to use', choices=['BnB', 'Approx', 'LS1', 'LS2'], type = str)
    parser.add_argument('time', help= 'cut-off time in seconds', type = float)
    parser.add_argument('seed', help = 'random seed applicable to randomized methods only', type = int)
    args = parser.parse_args()
    return args

def getGraph(filename):
    G = nx.Graph()
    vertex_ind = 0
    IndependentNodes = set()
    with open(filename, 'r') as file:
        for line in file:
            edge_data = list(map(lambda x: int(x), line.split()))
            if not edge_data:
                IndependentNodes.add(vertex_ind)
            if vertex_ind == 0:
                vertex_num = edge_data[0]
                edge_num = edge_data[1]
                G.add_nodes_from(range(1, vertex_ind + 1))
            else:
                for v in edge_data:
                    G.add_edge(vertex_ind, v)
            vertex_ind = vertex_ind + 1

        assert len(IndependentNodes) + G.number_of_nodes() == vertex_num
        assert edge_num == G.number_of_edges()
    return G

def write_out(vertex_cover_set, trace_history, filename, alg, time, seed):
        if not os.path.exists('./output'):
            os.makedirs('./output')
        solution = open('./output/' + os.path.splitext(os.path.basename(filename))[0] +
                '_' + alg + 
                '_' + str(time) + 
                '_' + str(seed) + 
                '.sol', 'w')
        solution.write(str(len(vertex_cover_set)) + '\n')
        solution.write(','.join(map(str, list(vertex_cover_set))))
        solution.close()
        trace = open('./output/' + os.path.splitext(os.path.basename(filename))[0] +
                '_' + alg + 
                '_' + str(time) + 
                '_' + str(seed) + 
                '.trace', 'w')
        for history in trace_history:
            trace.write(history + '\n')
        trace.close()


def main(filename, alg, time, seed):
    graph = getGraph(filename)
    if alg == 'BnB':
        vertex_cover_set, trace_history = BnB(graph, time)
        write_out(vertex_cover_set, trace_history, filename, alg, time, seed)
    elif alg == 'LS1':
        vertex_cover_set, trace_history = LS1(graph, time, seed)
        write_out(vertex_cover_set, trace_history, filename, alg, time, seed)

    elif alg == 'LS2':
        vertex_cover_set, trace_history = LS2(graph, time, seed)
        write_out(vertex_cover_set, trace_history, filename, alg, time, seed)
    else:
        vertex_cover_set, trace_history = Approx(graph, time, seed)
        write_out(vertex_cover_set, trace_history, filename, alg, time, seed)

    print('...done!')

if __name__ == '__main__':
    args = parseArguments()
    main(args.filename, args.alg, args.time, args.seed)

