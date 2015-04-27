import numpy as np
import random
from utils import *
from sklearn.gaussian_process import GaussianProcess as GP
from scipy import stats

# attack_success = [(sound_mean, sound_var), ..., (act_i_mean, act_i_var),...]
# notice the act of making a sound doesn't immediately produce any success
attack_success_no_sound = [(1, 0.5), (2, 1), (1, 2), (2, 2)] # action success array after not any sound
attack_success_sound =  [(0, 0.5), (0, 1), (0, 2), (2, 2)] # action success array after making sound around evesdropping mammals
attack_success_soundnfish = [(1, 0.5), (2, 1), (1.25, 2), (1, 2)] # action success array after making sound around fish
PHI = stats.distributions.norm().cdf
SUCCESS_THRESHOLD = 3

class ActionPlanner():
    def __init__(self):
        self.prev_action_index = -1
        self.gp = GP()
        self.training_model = None
        self.action_x_train = []
        self.action_y_train = []
        self.batch_index = 0
        self.num_evaluations = 0
        self.evaluation_vector = []
        
        
    
    def get_random_action_success(self):
        action_index = random.randint(0, len(attack_success_no_sound)-1)
        success_mean, success_var = attack_success_no_sound[action_index]
        success = -1
        if np.random.normal(success_mean, success_var) >= SUCCESS_THRESHOLD:
            success = 1
        return success, action_index
    
    def get_planned_action_success(self, prey):
        success = -1
        action_index = 0
        # If we don't have any past data, just try random stuff
        if len(self.action_x_train) < 10: 
            success, action_index = self.get_random_action_success()
            self.action_x_train.append((self.prev_action_index, action_index))
            self.action_y_train.append(success)
            self.prev_action_index = action_index
            
        else:
            # Consider past actions...
            prevs = [a[0] for a in self.action_x_train]
            acts = [a[1] for a in self.action_x_train]
            action_training = zip(range(0, len(prevs)), prevs, acts)
            training_x = np.array(action_training)
            
            self.trained_model = self.gp.fit(training_x, \
                self.action_y_train)
            
            prob_opinions = []
            for i in range(0, len(attack_success_no_sound)):
                o, err = self.trained_model.predict((len(prevs), self.prev_action_index, i), eval_MSE=True)
                #print(o)
                est_prob = PHI(-max(o,np.array([0.1]))/np.sqrt(err[0])+0.1)
                prob_opinions.append(est_prob)
               
            # choose action based on expected success 
            prob_total = sum(prob_opinions)
            if prob_total == 0:
                print "Caught ya"
                amt = 1./len(prob_opinions)
                for j in range(0, len(prob_opinions)):
                    prob_opinions[j] = amt
            else:
                prob_opinions = [a/float(prob_total) for a in prob_opinions]
                prob_opinions = [a[0] for a in prob_opinions]
            print "PROBS",prob_opinions
            # Randomly select option (better options have higher probabilites)
            action_index = np.nonzero(np.random.multinomial(1, prob_opinions))[0]
            print "ACTION:",action_index
            # Execute action
            
            success_mean, success_var = None, None
            if self.prev_action_index != 0:
                success_mean, success_var = attack_success_no_sound[action_index]
            else:
                if prey.type == AgentType.fish:
                    success_mean, success_var = attack_success_soundnfish[action_index]
                else:
                    print "yeah"
                    success_mean, success_var = attack_success_sound[action_index]
            if np.random.normal(success_mean, success_var) >= SUCCESS_THRESHOLD:
                success = 1
            
            # Forget the oldest past incident and commit the new one to memory
            if len(self.action_x_train) > 25:
                self.action_x_train.remove(self.action_x_train[0])
                self.action_y_train.remove(self.action_y_train[0])
            
            self.action_x_train.append((self.prev_action_index, action_index))
            self.action_y_train.append(success)
            self.prev_action_index = action_index
            
            #with open("debug.txt", "a") as f:
            #    f.write(str(zip(self.action_x_train, self.action_y_train)) + "\n")
            
        return success, action_index
    
    def get_action_beliefs(self, time_index):
        opinions = [] #self.gp.reduced_likelihood_function()[1]["gamma"].tolist()
        for i in range(0, len(attack_success_no_sound)):
            print(time_index)
            o = self.trained_model.score(np.array((time_index-1, self.prev_action_index, i)),\
               np.array([True])) + 0.01
            
            opinions.append(o)
        '''
        
        print(opinions)
        
        print opinions.tolist()[0]
        '''
        print opinions
        if np.max(opinions) == 0:
            opinions = np.ones((attack_success_no_sound,))/ float(len(attack_success_no_sound))
        else:
            opinions = np.array(opinions)/float(np.sum(opinions))
        print opinions
        return opinions
            
        