__author__ = 'blackfish'

from Tkinter import Label
from Tkinter import Tk
from Tkinter import mainloop
from environments import Environment


def generateGui(env):
    master = Tk()
    print env.grid
    for i in range(0, env.y):
        for j in range(0, env.x):

            Label(master, text=str(env.grid[i][j])).grid(row=i, column=j)

    mainloop()

if __name__=="__main__":
    e = Environment(x=20, y=20)
    print "Environment created..."
    generateGui(e)