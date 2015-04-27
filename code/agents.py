__author__ = 'blackfish'

import random
import itertools
import numpy as np
from utils import *
from action import *

START_FAT = 100
FISH_COUNT = 100
FISH_ENERGY = 0.01
COMMUNITY_DIST = 10
ORCA_DETECT_RANGE = 10

class Community():
    def __init__(self, env, size=10):
        self.env = env
        self.size = size
        self.pod = []
        center_pos = (env.y/2, env.x/2)
        pod_bounds = center_pos[0]-size, center_pos[0]+size, center_pos[1]-size, center_pos[1]+size 
        free_spaces = np.nonzero(self.empty_space_grid()[pod_bounds[0]:pod_bounds[1], pod_bounds[2]:pod_bounds[3]])
        print(free_spaces)
        index_tuples = np.array(random.sample(zip(free_spaces[0], free_spaces[1]), size))
        openy, openx = np.split(index_tuples, 2, axis=1)
        for i in range(0, size):
            willie = Orca(env, self, openy[i]+center_pos[0], openx[i]+center_pos[1])
            self.pod.append(willie)
            self.env.add_animal(willie)
            #self.env.orca_grid[openy, openx] = 1
        '''
        spaces = itertools.product(range(0, COMMUNITY_DIST), range(0,COMMUNITY_DIST))
        free_spaces = filter(lambda x: self.free_space(x), spaces)
        chosen_spaces = random.sample(free_spaces, size)
        for space in chosen_spaces:
            bob = Orca(env, self, space[1]+center_pos[1], space[0]+center_pos[0])
            self.pod.append(bob)
            env.add_animal(bob)
        '''
        
        
    def free_space(self, pos):
        cell = self.env.grid[pos[0]][pos[1]]
        return cell.resident == None and cell.type != CellType.beach and cell.type != CellType.icefloe
    
    def empty_space_grid(self):
        return np.equal(self.env.ground_grid, 0)

class Animal(object):
    def __init__(self, env, community, y, x):
        self.memory = []
        self.env = env
        self.community = community
        self.fat = START_FAT
        self.brain = None # some classifier here
        self.locx = x
        self.locy = y
        self.type = None
        self.manhattan_dist = lambda sucker: np.abs(sucker.locy - self.locy) + np.abs(sucker.locx-self.locx)
    
    def swim(self):
        '''
        Changes the orca's position according to the happiness function
        after detecting environmental values.
        :return:
        '''
        newlocx = random.randint(-1, 1) + self.locx
        newlocy = random.randint(-1, 1) + self.locy
        if newlocx > 0 and newlocx < self.env.x:
            self.locx = newlocx
        if newlocy > 0 and newlocy < self.env.y:
            self.locy = newlocy
        
        self.locy, self.locx = self.calc_pref_locs()
    
    def get_nearest(self, animals):
        '''
        :returns: the nearest animal in the given list using manhattan distance
        '''
        if len(animals) == 0:
            return None, -1
        
        closest = animals[0]
        min_dist = self.manhattan_dist(animals[0])
        for animal in animals:
            dist = self.manhattan_dist(animal)
            if min_dist > dist:
                closest = animal
                min_dist = dist
        return closest, min_dist
    
    def drift(self, animal, towards=True):
        '''
        Adjusts coordinates so that they are closer to given animal.
        :param animal: Target to which this is moving closer towards.
        '''
        dir = 1
        if not towards:
            dir = -1
        newlocx = self.locx + np.sign(animal.locx - self.locx) * dir
        newlocy = self.locy + np.sign(animal.locy - self.locy) * dir
        if self.env.cell_empty(newlocy, newlocx):
            self.locx, self.locy = newlocx, newlocy
        elif self.env.cell_empty(newlocy, self.locx):
            self.locy = newlocy
        elif self.env.cell_empty(self.locy, newlocx):
            self.locx = newlocx    

class Orca(Animal):
    def __init__(self, env, community, y, x):
        super(Orca, self).__init__(env, community, y, x)
        self.type = AgentType.orca
        self.brain = ActionPlanner()

    def communicate(self):
        '''

        :return:
        '''
		
        return 

    def attack(self):
        '''
        Causes the orca to attack a particular cell.
        :param x: x position of cell under attack
        :param y: y position of cell under attack
        :return:
        '''
        
        prey_animals = [a for a in self.env.animals if a.type != AgentType.orca]
        prey, prey_dist = self.get_nearest(prey_animals)
        if prey and prey_dist < 3:
            attack_success, action_index = self.brain.get_planned_action_success(prey)
            if attack_success:
                prey.fat -= 1
                if prey.fat == 0:
                    self.env.animals.remove(prey)
                    self.env.animal_grid[prey.locy, prey.locx] = 0
            
            
        
    
    def detect_env(self):
        '''
        Ignore this for now; it is built on the smell diffusion model.
        '''
        y = self.locy
        x = self.locx
        grid = self.env.grid
        pref_matrix = [[0.0] * ORCA_DETECT_RANGE] * ORCA_DETECT_RANGE
        bounds = min(y-ORCA_DETECT_RANGE/2, 0), min(x-ORCA_DETECT_RANGE/2, 0), \
            max(y+ORCA_DETECT_RANGE/2, env.y), max(x+ORCA_DETECT_RANGE/2, env.x)
        detected_region = grid[bounds[0]:bounds[2]][bounds[1]:bounds[3]] # TODO: bounds checking...
        #detected_region =
        num_smells = len(detected_region[0][0].smells)
        smell_grids = [None] * num_smells
        '''
        for i in range(0, num_smells):
            smell_grid = [[0.0] * ORCA_DETECT_RANGE] * ORCA_DETECT_RANGE
            for j in range(0, len(detected_region)):
                for k in range(0, len(detected_region[0])):
                    smell_grid[j][k] = detected_region[j][k].smells[i]
                smell_grids[i] = smell_grid
        '''
        for i in range(0, len(detected_region)):
            for j in range(0, len(detected_region[0])):
                pref_matrix[i][j] = detected_region[i][j].dot(self.prefs)
        offset = np.unravel_index(np.argmax(pref_matrix), pref_matrix.shape)
        happy_place = (y+offset[0], x+offset[1])
        # need to have smell diffusion
        return pref_matrix, happy_place
    
    def calc_pref_locs(self):
        '''
        Ignore this for now; built on the smell diffusion model
        :returns: the index of the most preferable cell to where the orca can move
        '''
        candidate_grid = self.get_available()
        miny, minx, maxy, maxx = self.get_bounds()
        print("bounds", miny, minx, maxy, maxx)
        fish_detect = self.env.fish_grid[miny:maxy, minx:maxx]
        print("fish detect",self.env.fish_grid)
        happy_matrix = fish_detect * candidate_grid # available locations that smell like fish
        prefy,prefx = np.unravel_index(np.argmax(happy_matrix), happy_matrix.shape)
        if happy_matrix[prefy, prefx] == 0:
            prefy, prefx = self.locy, self.locx
        return prefy-happy_matrix.shape[0]/2+self.locy, prefx-happy_matrix.shape[1]/2 + self.locx
    
    def get_bounds(self):
        '''
        Ignore for now; built on the smell diffusion model
        :returns: valid indices 
        '''
        y, x = self.locy, self.locx
        miny, minx, maxy, maxx = max(y-ORCA_DETECT_RANGE/2, 0), max(x-ORCA_DETECT_RANGE/2, 0), \
            min(y+ORCA_DETECT_RANGE/2, self.env.y), min(x+ORCA_DETECT_RANGE/2, self.env.x)
        return miny, minx, maxy, maxx
    
    def get_available(self):
        '''
        :returns: the indices to where the orca may potentially move.
        '''
        miny, minx, maxy, maxx = self.get_bounds()
        grid = self.env.ground_grid[miny:maxy,minx:maxx] + self.env.animal_grid[miny:maxy, minx:maxx]
        candidate_grid = np.equal(grid, 0)
        return candidate_grid
    
    def swim(self):
        '''
        Moves the orca closer to prey, closer to other orcas, or just randomly.
        '''
        prey_list = [a for a in self.env.animals if a.type != AgentType.orca] # TODO: Add prey list
        self.env.animal_grid[self.locy, self.locx] = 0 # vacate old spot
        closest_sucker, min_prey_dist = self.get_nearest(prey_list)  
        closest_orca, min_orca_dist = self.get_nearest(self.community.pod)        
        if closest_sucker and min_prey_dist < 50 and random.randint(0, int(np.log(min_prey_dist + 2))) == 0: # arbitrary bound on detection range. necessary?
            self.drift(closest_sucker)
        elif min_orca_dist > 10: # find other orcas if no fish nearby
            self.drift(closest_orca)
        else: # note we may choose optimal randomly. we may also choose unavailable spot also.
            xoffset, yoffset = random.randint(-1,1), random.randint(-1,1)
            if self.env.cell_empty(self.locy + yoffset, self.locx + xoffset):
                nx = self.locx + xoffset
                ny = self.locy + yoffset
                if nx >= 0 and nx < self.env.x:
                    self.locx = nx
                if ny >= 0 and ny < self.env.y:
                    self.locy = ny   
        self.env.animal_grid[self.locy, self.locx] = 1  # update animal grid    
        #self.attack()
    
    def get_happy(self):
        return sum([o.fat for o in self.community.orcas]) + self.fat/2.0

class Seal(Animal):

    def __init__(self, env, y, x):
        self.fat = START_FAT
        self.brain = None # some classifier
        self.locx = x
        self.locy = y
        self.fat_loss = 1.0
        self.env = env
        self.type = AgentType.seal

    def swim(self):
        orca_list = [a for a in self.env.animals if a.type == AgentType.orca] # TODO: Add prey list
        self.env.animal_grid[self.locy, self.locx] = 0 # vacate old spot  
        closest_orca, min_orca_dist = self.get_nearest(orca_list) 
        if min_orca_dist < 5: # DANGER to fish
            self.drift(closest_orca, False)
        else: # note we may choose optimal randomly. we may also choose unavailable spot also.
            xoffset, yoffset = random.randint(-1,1), random.randint(-1,1)
            if self.env.cell_empty(self.locy + yoffset, self.locx + xoffset):
                nx = self.locx + xoffset
                ny = self.locy + yoffset
                if nx >= 0 and nx < self.env.x:
                    self.locx = nx
                if ny >= 0 and ny < self.env.y:
                    self.locy = ny  
        self.env.animal_grid[self.locy, self.locx] = 1  # update animal grid 

    def get_happy(self):
        return self.fat

class FishSchool(Animal):

    def __init__(self, env, community, y, x):
        '''
        self.count = FISH_COUNT
        self.fat = FISH_ENERGY
        self.locx = x
        self.locy = y
        self.fat_loss = 0.10
        self.env = env
        '''
        super(FishSchool, self).__init__(env, community, y, x)
        self.type = AgentType.fish
    
    def swim(self):
        orca_list = [a for a in self.env.animals if a.type == AgentType.orca] # TODO: Add prey list
        self.env.animal_grid[self.locy, self.locx] = 0 # vacate old spot  
        closest_orca, min_orca_dist = self.get_nearest(orca_list) 
        if min_orca_dist < 5: # DANGER to fish
            self.drift(closest_orca, False)
        else: # note we may choose optimal randomly. we may also choose unavailable spot also.
            xoffset, yoffset = random.randint(-1,1), random.randint(-1,1)
            if self.env.cell_empty(self.locy + yoffset, self.locx + xoffset):
                nx = self.locx + xoffset
                ny = self.locy + yoffset
                if nx >= 0 and nx < self.env.x:
                    self.locx = nx
                if ny >= 0 and ny < self.env.y:
                    self.locy = ny    
        self.env.animal_grid[self.locy, self.locx] = 1  # update animal grid 
        

    def get_happy(self):
        return self.fat
