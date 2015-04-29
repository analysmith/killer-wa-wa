__author__ = 'blackfish'

import random
import numpy as np
from utils import *
BEACH_Y = 10
BEACH_PROB = 0.001
FLOE_PROB = 0.005

class Environment():

    def __init__(self, y=1000, x=1000, floe_prob=FLOE_PROB, num_iter=200):
        if y < 10 or x < 10:
            assert False, "C'mon. The environment should be a wee bit larger than "+\
                str(y) +" by "+ str(x) +". This isn't SeaWorld."
        self.grid = []
        self.x = x
        self.y = y
        self.num_floes = int(x * FLOE_PROB)
        self.num_beach = int(x * BEACH_PROB)
        self.animals = []
        self.ground_grid = np.zeros(shape=(self.y, self.x))
        self.animal_grid = np.zeros(shape=(self.y, self.x))
        self.seal_grid = np.zeros(shape=(self.y, self.x))
        self.fish_grid = np.zeros(shape=(self.y, self.x))
        self.sound_grid = np.zeros(shape=(self.y, self.x))
        self.generate_grid()
        self.num_iter = num_iter
        self.curr_iter = 0

    def add_animal(self, animal):
        x = animal.locx
        y = animal.locy
        #cell = self.grid[y][x]
        #cell.resident = animal
        self.animals.append(animal)
        self.animal_grid[y, x] = 1 # should change to animal type
       
    def generate_grid(self):
        self.grid = np.array([[EnvCell()] * self.x] * self.y)
        
        # create beach with some parts jutting out further than others
        self.ground_grid[:BEACH_Y-2, :] = 1
        x_indices = random.sample(range(0, self.x), 10)
        self.ground_grid[BEACH_Y-1][x_indices] = 1
        
        # Ice floes will be indicated by fractional value (represents lack of safety for seals)
        # Add ice floes
        for i in range(BEACH_Y, self.y):
            x_indices = random.sample(range(0, self.x), 1)
            self.ground_grid[i, x_indices] = 0.75
        
    def propagate(self, grid, prop_frac=0.5, min_threshold=0.01):
        up = np.roll(grid, 1, axis=0) * prop_frac
        up[0][:] = 0
        down = np.roll(grid, -1, axis=0) * prop_frac
        down[grid.shape[0]-1][:] = 0
        right = np.roll(grid, 1, axis=1) * prop_frac
        right[0][:] = 0
        left = np.roll(grid, -1, axis=1) * prop_frac
        left[grid.shape[1]-1][:] = 0
        prop_mat = grid + up + down + right + left
        prop_mat = prop_mat * np.greater(prop_mat, min_threshold)
        return prop_mat
    
    def update(self):
        for a in self.animals:
            a.swim
        orcas = [a for a in filter(lambda m: m.type == AgentType.orca, self.animals)]
        dead_orcas = []
        for a in orcas:
            a.attack()
            if a.fat <=0:
                dead_orcas.append(a)
        for poor_willie in dead_orcas:
            self.animals.remove(poor_willie)
            poor_willie.community.pod.remove(poor_willie)
            
        self.curr_iter += 1
        print "current iteration:", self.curr_iter, "/",self.num_iter
        if self.curr_iter >= self.num_iter:
            return False
        return True
            
    def cell_empty(self, locy, locx, land_ok=False):
        if locy < 0 or locy >= self.y or locx < 0 or locx >= self.x:
            return False
        
        #wait for this. don't want to introduce too many vars.
        '''
        if land_ok:
            return self.animal_grid[locy, locx] == 0
        '''
        return self.animal_grid[locy, locx] == 0 and self.ground_grid[locy, locx] == 0

class EnvCell():
    def __init__ (self, type=CellType.sea, resident=None, pos=(0,0)):
        '''
        Represents one cell in the environment. An agent
        may occupy only one cell at a time.
        :param type: The type of the cell (beach, ice floe, etc.)
        :param resident: An agent occupying this cell.
        :param pos: The (row,col) position of the cell in the environment grid
        :return:
        '''
        self.type = type
        self.resident = resident
        self.pos = pos
        # right now, only 3 types of smells: orca, seals, and fish
        self.smells = np.array([0.0] * 3) # TODO: fig out enum len #len(AgentType))