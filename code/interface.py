__author__ = 'blackfish'

from Tkinter import Label
from Tkinter import Tk
from Tkinter import mainloop
from environments import Environment
from agents import *
from utils import *
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.artist import setp

def generateGui(env):
    master = Tk()
    print env.grid
    for i in range(0, env.y):
        for j in range(0, env.x):

            Label(master, text=str(env.grid[i][j])).grid(row=i, column=j)

    mainloop()
   
def generatePlot(env):
    
    def get_color(type):
        if type >= 1:
            return "y"
        elif type == 0: #CellType.sea:
            return "b"
        elif type < 1 and type > 0: #CellType.icefloe:
            return "w"
    
    def get_animal_color(animal):
        if animal.type == AgentType.orca:
            return "k"
        elif animal.type == AgentType.seal:
            return "r"
        elif animal.type == AgentType.fish:
            return "g"
    
    animal_color = [get_animal_color(x) for x in env.animals]
    #fig, ax = plt.subplots()
    fig = plt.figure()
    for i in range(0, env.y):
        colors = [get_color(x) for x in env.ground_grid[i]]
        plt.scatter(range(0, env.x), [i] * env.x, c=colors,s=[5]*env.x, alpha=0.5)
        
    scatter = plt.scatter([], [], animated=True) #, c=animal_color, s=[10]*env.x)
    def update_animals(num):
        env.update()
        for a in env.animals:
            a.swim()
        animalsx = [x.locx for x in env.animals]
        animalsy = [x.locy for x in env.animals]
        scatter = plt.scatter(animalsx, animalsy, c=animal_color, animated=True)
        return scatter,
    ani = animation.FuncAnimation(fig, update_animals, 100, interval=50, blit=True)    
    plt.ylim = (0, env.y)
    plt.xlim = (0, env.x)
    plt.show()
    
if __name__=="__main__":
    e = Environment(x=100, y=100)
    comm = Community(e)
    e.add_animal(FishSchool(e, None, 60,60))
    print "Environment created..."
    generatePlot(e)