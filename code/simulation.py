from interface import generatePlot
from environments import Environment
from agents import Community, FishSchool, Seal
from getopt import getopt
import sys
import random
import numpy as np

def get_args():
    opts, args = getopt(sys.argv[1:], "o:p:d:i:m", ["orcas=", "prey=","dim=", "num_iter=","mammal"])
    num_orcas = 10
    num_prey = 5
    dim = 100
    mammal = False
    num_iter = 200
    
    for o,a in opts:
        if o == "-o" or o == "--orcas":
            num_orcas = int(a)
        elif o == "-p" or o == "--prey":
            num_prey = int(a)
        elif o == "-d" or o == "--dim":
            dim = int(a)
        elif o == "-i" or o == "--num_iter":
            num_iter = int(a)
        elif o == "-m" or o == "--mammal":
            mammal = True
    return num_orcas, num_prey, dim, num_iter, mammal
        
    
if __name__ == "__main__":
    
    norca, nprey, d, niter, use_mammal = get_args()
    e = Environment(x=d, y=d, num_iter=niter)
    comm = Community(e, norca)
    animal_class = FishSchool
    if use_mammal:
        animal_class = Seal
    for i in range(0, nprey):
        x, y = random.randint(0, d-1), random.randint(0, d-12) #np.unravel_index(random.sample(range(0, (d-10)*d), 1), (d-10,d))
        e.add_animal(animal_class(e, None, y+11, x))
    print "Environment created..."
    generatePlot(e)