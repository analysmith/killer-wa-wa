__author__ = 'blackfish'

from Tkinter import Label
from Tkinter import Tk
from Tkinter import mainloop
from environments import Environment
from agents import *
import matplotlib.pyplot as plt

def enum(*sequential, **named):
    enums = dict(zip(sequential, range(len(sequential))), **named)
    return type('Enum', (), enums)

CellType = enum("beach", "sea", "icefloe")


def generateGui(env):
    master = Tk()
    print env.grid
    for i in range(0, env.y):
        for j in range(0, env.x):

            Label(master, text=str(env.grid[i][j])).grid(row=i, column=j)

    mainloop()
   
def generatePlot(env):
	spot_grid = []
	def get_color(type):
		if type == CellType.beach:
			return "y"
		elif type == CellType.sea:
			return "b"
		elif type == CellType.icefloe:
			return "w"
	
	
	for i in range(0, env.y):
		colors = [get_color(x.type) for x in env.grid[i]]
		animals = [x.resident for x in env.grid[i] if x.resident]
		plt.scatter(range(0, env.x), [i] * env.x, c=colors,s=[75]*env.x, alpha=0.5)
	plt.ylim = (0, env.y)
	plt.xlim = (0, env.x)
	plt.show()
	

if __name__=="__main__":
    e = Environment(x=100, y=100)
	comm = Community(e)
	e.add_animal(Orca)
    print "Environment created..."
    generatePlot(e)