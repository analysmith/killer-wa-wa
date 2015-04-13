__author__ = 'blackfish'

import random
import itertools

START_FAT = 0.75
FISH_COUNT = 100
FISH_ENERGY = 0.01

def enum(*sequential, **named):
    enums = dict(zip(sequential, range(len(sequential))), **named)
    return type('Enum', (), enums)

CellType = enum("beach", "sea", "icefloe")

class Community():
	def __init__(self, env, size=10):
		self.env = env
		self.size = size
		center_pos = (env.y/2, env.x / 2)
		radius = 10
		spaces = itertools.product(range(0, radius), range(0,radius))
		free_spaces = filter(lambda x: self.free_space(x), spaces)
		chosen_spaces = random.sample(free_spaces, size)
		for space in chosen_spaces:
			bob = Orca(env, self, space[1], space[0])
			env.add_animal(bob)
	
	def free_space(self, pos):
		cell = self.env.grid[pos[0]][pos[1]]
		return cell.resident == None and cell.type != CellType.beach and cell.teyp != CellType.icefloe

class Orca():

    def __init__(self, env, community, x=0, y=0):
        self.memory = []
        self.env = env
        self.community = community
        self.fat = START_FAT
        self.brain = None # some classifier here
        self.locx = x
        self.locy = y

    def swim(self):
        '''
        Changes the orca's position according to the happiness function
        after detecting environmental values.
        :return:
        '''

        # sensory_matrix = self.detect()
        # random and stupid at this point, just can't fall off edge of earth
        newlocx = random.randint(0, 2) + self.locx
        newlocy = random.randint(0, 2) + self.locy
        if newlocx > 0 and newlocx < self.env.x:
            self.locx = newlocx
        if newlocy > 0 and newlocy < self.env.y:
            self.locy = newlocy


    def communicate(self):
        '''

        :return:
        '''
		
        return 

    def attack(self, x, y):
        '''
        Causes the orca to attack a particular cell.
        :param x: x position of cell under attack
        :param y: y position of cell under attack
        :return:
        '''
        target = self.env.cell[y][x].resident
        if random.randint(0, 10) == 0 and target :
            self.fat += max(target.fat_loss, 1)
            target.fat -= target.fat_loss

    def get_happy(self):
        return sum([o.fat for o in self.community.orcas]) + self.fat/2.0

class Seal():

    def __init__(self, env, x, y ):
        self.fat = START_FAT
        self.brain = None # some classifier
        self.locx = x
        self.locy = y
        self.fat_loss = 1.0
        self.env = env

    def swim(self):
        '''
        Moves the seal around at random.
        :return:
        '''
        newlocx = random.randint(0, 2) + self.locx
        newlocy = random.randint(0, 2) + self.locy
        if newlocx > 0 and newlocx < self.env.x:
            self.locx = newlocx
        if newlocy > 0 and newlocy < self.env.y:
            self.locy = newlocy

    def escape(self):
        return random.randint(0, 100) < 25

    def detect(self):
        pass

    def get_happy(self):
        return self.fat

class FishSchool():

    def __init__(self, env, x, y):
        self.count = FISH_COUNT
        self.fat = FISH_ENERGY
        self.locx = x
        self.locy = y
        self.fat_loss = 0.10
        self.env = env

    def swim(self):
        '''
        Moves the school of fish around at random.
        :return:
        '''
        newlocx = random.randint(0, 2) + self.locx
        newlocy = random.randint(0, 2) + self.locy
        if newlocx > 0 and newlocx < self.env.x:
            self.locx = newlocx
        if newlocy > 0 and newlocy < self.env.y:
            self.locy = newlocy

    def get_happy(self):
        return self.fat
