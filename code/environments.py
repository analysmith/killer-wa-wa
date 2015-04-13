__author__ = 'blackfish'

import random
import numpy as np
BEACH_Y = 5
BEACH_PROB = 0.001
FLOE_PROB = 0.005

def enum(*sequential, **named):
    enums = dict(zip(sequential, range(len(sequential))), **named)
    return type('Enum', (), enums)

CellType = enum("beach", "sea", "icefloe")

class Environment():

    def __init__(self, x=1000, y=1000, num_floes=10, num_beach=100):
        self.grid = []
        self.x = x
        self.y = y
        self.num_floes = num_floes
        self.num_beach = num_beach
        self.generate_grid()

    def generate_grid(self):
        self.grid = np.array([[EnvCell()] * self.x] * self.y)
        # create beach with some parts jutting out further than others
        for i in range(0, BEACH_Y):
            for j in range(0, self.x):
                if i < BEACH_Y - 2:
                    self.grid[i][j] = EnvCell(type=CellType.beach)
                elif i == BEACH_Y-1 and random.randint(0, 10) == 0:
                    self.grid[i][j] = EnvCell(type=CellType.beach)
                else:
                    self.grid[i][j] = EnvCell()

        # create ice floes with small prob
        for i in range(BEACH_Y, self.y-3):
            for j in range(0, self.x):
                probe = random.randint(0, 20) == 0
                if probe:
                    self.grid[i][j] = EnvCell(type=CellType.icefloe)
                else:
                    self.grid[i][j] = EnvCell()

	def add_animal(animal):
		x = animal.locx
		y = animal.locy
		cell = self.grid[y][x]
		cell.resident = animal
		
    def propagate(self):
        pass

    def show_up(self):
        pass

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
        self.smells = np.array([0.0] * 3)