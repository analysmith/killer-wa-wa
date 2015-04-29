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
import matplotlib.patches as mpatches
import sys
from action import *
from collections import defaultdict
   
def get_color(type):
    '''
    Returns the color of the enviroment object.
    '''
    if type >= 1: # Beach
        return "y"
    elif type == 0: # Ocean
        return "b"
    elif type < 1 and type > 0: # Ice floe
        return ".95"   
    return "c" # Shallow sea?

def get_animal_color(animal):
    '''
    Returns the color of the animal.
    
    '''
    if animal.type == AgentType.orca:
        return "k"
    elif animal.type == AgentType.seal:
        return "r"
    elif animal.type == AgentType.fish:
        return "g"
    return "m"

def save_prefs(env, fname="action_prefs.txt"):
    '''
    Writes the action probabilities of every (surviving) orca to a file.
    :param env: The environment of the orcas.
    :param fname: The name of the file to write to.
    '''
    with open(fname, "w") as f:
        vectors = []
        experiences = []
        # prolly should use panda to write csv file
        f.write("noise_pref,noise_boosted1,noise_boosted2,noise_averse,experience,successes\n")
        strategy_map = defaultdict(lambda : [])
        for a in sorted(filter(lambda b:b.type == AgentType.orca, env.animals),key=lambda b:b.experience):
            if a.brain.evaluation_vector != None and a.brain.evaluation_vector.shape[0] > 0: # some whales never learn anything
                vectors.append(a.brain.evaluation_vector)
                best_two = np.argsort(a.brain.evaluation_vector)[-2:]
                strategy_map[tuple(sorted([best_two[0], best_two[1]]))].append(a.brain.evaluation_vector)
                experiences.append(a.experience)
                f.write(",".join([str(c) for c in a.brain.evaluation_vector]) + ","+str(a.experience) +str(a.success_count)+"\n")
                
            else:
                f.write("\n")
        if len(vectors) > 0:
            print [str(a[0]) + str(len(a[1])) for a in strategy_map.iteritems()]
            #best_stra
            mean_values= np.mean(np.array(vectors),axis=0)
            weighted_mean_values = np.average(np.array(vectors),axis=0, weights=experiences)
            std_devs = np.std(np.array(vectors), axis=0)
            plt.figure()
            fig, ax = plt.subplots()
            plt.bar(np.array(range(0, len(mean_values)))+.25,mean_values, .5, color="g", yerr=std_devs) 
            plt.suptitle("Mean Strategy Preferences",size=18)
            plt.xlabel("Action", size=15)
            ax.set_xticks(np.array(range(0, len(mean_values)))+.5)
            ax.set_xticklabels([str(k) for k in range(0, len(mean_values))])
            plt.ylabel("Probability of Action Being Chosen", size=15)
            plt.axis((0, len(mean_values),0, 1))
            plt.savefig("mean-strategies")
            
            f.write("Mean:"+",".join([str(c) for c in mean_values]) + "\n")
            f.write("Std devs:"+",".join([str(c) for c in std_devs]) + "\n")
            
            top_three = sorted(strategy_map.iteritems(), key=lambda x: len(x[1]))[-3:]
            plt.figure()
            fig, ax = plt.subplots(3)
            for i, (strategy, ivectors) in enumerate(top_three):
                ax[i].set_ylim((0, .8))
                mean_values= np.mean(np.array(ivectors),axis=0)
                std_devs = np.std(np.array(ivectors), axis=0)
                ax[i].bar(np.array(range(0, len(mean_values)))+.25,mean_values, .5, color="g", yerr=std_devs) 
                ax[i].set_title("Strategy Probs for " + str(strategy) + "(orcas=" + str(len(ivectors))+")",size=18)
                if i < 2:
                    ax[i].set_xticks([])
                    ax[i].set_xticklabels([])
                else:
                    ax[i].set_xticks(np.array(range(0, len(mean_values)))+.5)
                    ax[i].set_xticklabels([str(k) for k in range(0, len(mean_values))])
                    ax[i].set_xlabel("Action", size=10)
                ax[i].set_ylabel("Prob Action Chosen", size=10)
            plt.savefig("strategies-"+str(strategy))
                
             
            
def plot_shit(env):
    # success rate vs. experience
    plt.figure()
    success = [a.success_count for a in env.animals]
    experience = [a.experience for a in env.animals]
    plt.plot(experience, success, "bo")
    plt.plot(range(0, max(experience)), range(0, max(experience)))
    plt.ylabel("Number of successful attacks",size=20)
    plt.xlabel("Number of attacks (experience)", size=20)
    plt.suptitle("Successes vs. Experience",size=25)
    plt.savefig("success_v_experience")
    
    #attack_success_no_sound = [.00000001, .25, .15, .25] # action success array after not any sound
    #attack_success_sound =  [.00000001, .05, .05, .05] # action success array after making sound around evesdropping mammals
    #attack_success_soundnfish = [.00000001, .5, .8, .05]
    
    fig = plt.figure()
    success_rate = [a.success_count/float(a.experience) for a in env.animals if a.experience > 0]
    guessing_vec = np.array([1/float(len(attack_success_no_sound))] * len(attack_success_no_sound))
    seals = .75 * np.array(attack_success_no_sound) + .25 * np.array(attack_success_sound)
    fish = .75 * np.array(attack_success_no_sound) + .25 * np.array(attack_success_soundnfish)
    exp_success_rate_seals = seals.dot(guessing_vec)
    exp_success_rate_fish = fish.dot(guessing_vec)
    plt.scatter(range(0, len(success_rate)), success_rate, c="k", s=[a.experience+10 for a in env.animals if a.experience > 0])
    plt.plot(range(0, len(success_rate)), [exp_success_rate_fish]*len(success_rate), "g")
    plt.suptitle("Orca Success Rates (Prey = Seals)")
    plt.xlabel("Orca ID")
    plt.ylabel("Success Rates")
    plt.axis((0, len(success_rate)-1,0, 1))
    plt.savefig("baselines")
    
    
    
            
def generatePlot(env):
    '''
    Generates an animation of the given environment.
    :param env: The environment that is being mapped.
    '''
    animal_color = [get_animal_color(x) for x in env.animals]
    fig = plt.figure()
    for i in range(0, env.y):
        colors = [get_color(x) for x in env.ground_grid[i]]
        plt.scatter(range(0, env.x), [i] * env.x, c=colors,s=[20]*env.x, alpha=0.5)
        
    scatter = plt.scatter([], [], animated=True) #, c=animal_color, s=[10]*env.x)
    black_patch = mpatches.Patch(color='k', label='Killer whale')
    red_patch = mpatches.Patch(color='r', label='Seal')
    green_patch = mpatches.Patch(color='g', label='Fish')
    yellow_patch = mpatches.Patch(color='y', label='Beach')
    white_patch = mpatches.Patch(color='.95', label='Ice floe')
    blue_patch = mpatches.Patch(color='b', label='Water')
    plt.legend(handles=[black_patch, red_patch, green_patch, yellow_patch, white_patch, blue_patch])
    def update_animals(num):
        # Update animal locations + continue animation goahead
        for a in env.animals:
            a.swim()
        cont_iter = env.update() 
        active_pointsx = [x.locx for x in env.animals if x.current_action > -1]
        active_pointsy = [x.locy for x in env.animals if x.current_action > -1]
        print( "Active orcas:",len(active_pointsx))
        active_colors = ["m"] * len(active_pointsx)
        active_sizes = [120] * len(active_pointsx)
        animalsx = [x.locx for x in env.animals]
        animalsy = [x.locy for x in env.animals]
        sizes = [x.fat/2 for x in env.animals] # Size is based on fat stores.
        
        scatter = plt.scatter(active_pointsx+animalsx, active_pointsy+animalsy, c=active_colors+animal_color, s=active_sizes+sizes, animated=True)
        #if env.curr_iter == 1:
        #    plt.savefig("the_hunt.png")
        print "Num iter:",env.num_iter
        print "Continue?:", cont_iter
        if not cont_iter or env.curr_iter > env.num_iter:
            #Save orca action preferences to a file
            save_prefs(env) 
            plot_shit(env)
            #plt.close()
            sys.exit(0)
        return scatter,
        
    ani = animation.FuncAnimation(fig, update_animals, 100, interval=50, blit=True,save_count=1)    
    plt.ylim = (0, env.y)
    plt.xlim = (0, env.x)
    try:
        plt.show()
    except:  
        system.exit(0)
        print "Good bye"
    
    
if __name__=="__main__":
    e = Environment(x=100, y=100)
    comm = Community(e)
    e.add_animal(FishSchool(e, None, 60,60))
    print "Environment created..."
    generatePlot(e)