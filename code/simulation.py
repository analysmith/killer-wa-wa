from interface import generatePlot
from environments import Environment
from agents import Community

class Simulation():
    def __init__(self, rows=100, cols=100, num_orcas=10, num_prey=100, mammal_prey=False):
        self.env = Environment()
        self.community = Community(self.env, size=num_orcas)
        generatePlot(self.env)

if __name__ == "__main__":
    sim = Simulation()