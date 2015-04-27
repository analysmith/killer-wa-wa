import numpy as np
import random
from utils import *
from sklearn.gaussian_process import GaussianProcess as GP

# prob of success. index corresponds to action. index 0 = sound
attack_success_no_sound = [(1, 0.5), (1, 1), (1, 2), (2, 1)]
attack_success_sound =  [(.5, 0.5), (.5, 1), (0, 2), (3, 1)] # 
attack_success_soundnfish = [(1, 0.5), (1.5, 1), (1.25, 2), (.5, 1)]

class ActionPlanner():
    def __init__(self):
        self.prev_action_index = -1
        self.gp = GP()
        self.training_model = None
        self.action_x_train = []
        self.action_y_train = []
        
        self.event_count = 0
        
    
    def get_random_action_success(self):
        action_index = random.randint(0, len(attack_success_no_sound)-1)
        success_mean, success_var = attack_success_no_sound[action_index]
        success = np.random.normal(success_mean, success_var) >= 2
        return success, action_index
    
    def get_planned_action_success(self, prey):
        success = False
        action_index = 0
        # If we don't have any past data, just try random stuff
        if len(self.action_x_train) < 10:
            print("Thinking")
            success, action_index = self.get_random_action_success()
            self.event_count = (self.event_count + 1) % 50
            
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
            
            opinions = []
            for i in range(0, len(attack_success_no_sound)):
                #o = self.trained_model.score(np.array((len(prevs) + 1, self.prev_action_index, i)),np.array([True]))
                #import pdb;pdb.set_trace()
                o, err = self.trained_model.predict(np.array((len(prevs) + 1, self.prev_action_index, i)), eval_MSE=True)
                opinions.append((o,err[0]))
               
            # choose min error successful action 
            opinion_vec = []
            for o, err in opinions:
                if not o:
                    opinion_vec.append(.1)
                else:
                    opinion_vec.append(1/err+.1)
            total = sum(opinion_vec)
            opinions = [a/float(total) for a in opinion_vec]
            #opinions = np.array(opinion_vec)/np.sum(opinion_vec)
            print "OPS:",opinions
            
            
            # Randomly select option (better options have higher probabilites)
            #if opinions.shape[0] != 1:
            action_index = np.nonzero(np.random.multinomial(1, np.array(opinions)))[0]
            print action_index
            # Execute action
            
            success_mean, success_var = None, None
            if self.prev_action_index != 0:
                success_mean, success_var = attack_success_no_sound[action_index]
            else:
                if prey.type == AgentType.fish:
                    success_mean, success_var = attack_success_soundnfish[action_index]
                else:
                    success_mean, success_var = attack_success_sound[action_index]
            success = np.random.normal(success_mean, success_var) >= 2
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
            #print "This is an opinion:", o
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
            
        