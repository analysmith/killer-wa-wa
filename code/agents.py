__author__ = 'blackfish'

START_FAT = 0.75
FISH_COUNT = 100
FISH_ENERGY = 0.01

class Orca():

    def __init__(self, env, community):
        self.memory = []
        self.env = env
        self.community = community
        self.fat = START_FAT
        self.brain = None # some classifier here

    def swim(self):
        '''
        Changes the orca's position according to the happiness function
        after detecting environmental values.
        :return:
        '''
        sensory_matrix = self.detect()


    def communicate(self):
        '''

        :return:
        '''
        pass

    def attack(self):
        pass

    def detect(self):
        pass

    def get_happy(self):
        pass

class Seal():

    def __init__(self):
        self.fat = START_FAT
        self.brain = None # some classifier

    def swim(self):
        pass

    def escape(self):
        pass

    def detect(self):
        pass

    def get_happy(self):
        pass

class FishSchool():

    def __init__(self):
        self.count = FISH_COUNT
        self.fat = FISH_ENERGY

    def swim(self):
        '''
        Moves the school of fish around at random.
        :return:
        '''

    def get_happy(self):
        pass
