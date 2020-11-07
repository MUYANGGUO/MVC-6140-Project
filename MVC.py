# system
import os
import time
import argparse
# libs
import numpy as np
import math as math
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

def main(filename, alg, time, seed):
    BnB()
    LS1()
    LS2()
    Approx()
    print('...done!')

if __name__ == '__main__':
    args = parseArguments()
    main(args.filename, args.alg, args.time, args.seed)

