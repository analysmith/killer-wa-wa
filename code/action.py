import numpy as np
import random
from utils import *
from sklearn.gaussian_process import GaussianProcess as GP
from sklearn.naive_bayes import GaussianNB as GNB
from scipy import stats

# attack_success = [(sound_mean, sound_var), ..., (act_i_mean, act_i_var),...]
# notice the act of making a sound doesn't immediately produce any success
attack_success_no_sound = [-1, .25, .25, .25] # action success array after not any sound
attack_success_sound =  [-1, .05, .05, .05] # action success array after making sound around evesdropping mammals
attack_success_soundnfish = [-1, .3, .4, .25] # action success array after making sound around fish
PHI = stats.distributions.norm().cdf

class ActionPlanner():
    def __init__(self):
        self.prev_action_index = -1
        self.gnb = GNB()
        self.training_model = None
        self.action_x_train = []
        self.action_y_train = []
        self.batch_index = 0
        self.num_evaluations = 0
        self.evaluation_vector = None
        
        
    
    def get_random_action_success(self):
        action_index = random.randint(0, len(attack_success_no_sound)-1)
        threshold = attack_success_no_sound[action_index]
        success = -1
        if np.random.uniform(0, 1) < threshold:
            success = 1
        return success, action_index
    
    def get_planned_action_success(self, prey):
        success = -1
        action_index = 0
        # If we don't have any past data, just try random stuff (burnin period)
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
            
            self.trained_model = self.gnb.fit(training_x, self.action_y_train)
            prob_opinions = []
            for i in range(0, len(attack_success_no_sound)):
                tag_probs = self.trained_model.predict_proba(np.array((len(prevs), self.prev_action_index, i)))
                print tag_probs
                print tag_probs.shape
                pos_tag_prob = None
                if tag_probs.shape[1]==1L:
                    if self.action_y_train[0] == -1:
                        #tag_probs = np.reshape(np.array((tag_probs[0,0], 1L-tag_probs[0,0])), (1L, 1L))
                        pos_tag_prob = 0
                    else:
                        #tag_probs = np.reshape(np.array((1L-tag_probs[0,0], tag_probs[0,0])), (1L, 1L))
                        pos_tag_prob
                else:
                    pos_tag_prob = tag_probs[0][1]
                
                prob_opinions.append(pos_tag_prob)
            total = sum(prob_opinions)
            amt = 1./len(prob_opinions)
            prob_opinions = [(a + amt)/(float(total)+1) for a in prob_opinions]
            if self.evaluation_vector == None:
                self.evaluation_vector = np.array(prob_opinions)
            else:
                self.evaluation_vector += np.array(prob_opinions)
                self.evaluation_vector = self.evaluation_vector / np.sum(self.evaluation_vector)
                
            print "PROBS",prob_opinions
            # Randomly select option (better options have higher probabilites)
            action_index = np.nonzero(np.random.multinomial(1, prob_opinions))[0][0]
            
            threshold = None
            if self.prev_action_index != 0:
                threshold = attack_success_no_sound[action_index]
            else:
                if prey.type == AgentType.fish:
                    threshold = attack_success_soundnfish[action_index]
                else:
                    threshold = attack_success_sound[action_index]
            if np.random.uniform(0, 1) < threshold:
                success = 1
            
            # Forget the oldest past incident and commit the new one to memory
            if len(self.action_x_train) > 25:
                self.action_x_train.remove(self.action_x_train[0])
                self.action_y_train.remove(self.action_y_train[0])
            
            self.action_x_train.append((self.prev_action_index,action_index)) # 
            self.action_y_train.append(success)
            self.prev_action_index = action_index
        return success, action_index
    
    def get_action_beliefs(self, time_index):
        opinions = [] #self.gp.reduced_likelihood_function()[1]["gamma"].tolist()
        for i in range(0, len(attack_success_no_sound)):
            print(time_index)
            o = self.trained_model.score(np.array((time_index-1, self.prev_action_index, i)),\
               np.array([True])) + 0.01
            
            opinions.append(o)
        if np.max(opinions) == 0:
            opinions = np.ones((attack_success_no_sound,))/ float(len(attack_success_no_sound))
        else:
            opinions = np.array(opinions)/float(np.sum(opinions))
        print opinions
        return opinions
            
        