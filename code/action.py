import numpy as np
import random
from utils import *
from sklearn.gaussian_process import GaussianProcess as GP

# prob of success. index corresponds to action. index 0 = sound
attack_success_no_sound = [.5, .35, .45, .6 ] #lambda values #[(.5, 0.5), (1, 1), (0.5, 2), (0.5, 1)]
attack_success_sound = [.75, .75, .6, .3]#[(0, 0.5), (0, 1), (0, 2), (1, 1)]
attack_success_soundnfish = [.5, .15, .25, .6 ] #[(.5, 0.5), (1.5, 1), (1, 2), (0.5, 1)]

class ActionPlanner():
    def __init__(self):
        self.prev_action_index = -1
        self.gp = GP()
        self.action_x_train = []
        self.action_y_train = []
        
        self.event_count = 0
        
    
    def get_random_action_success(self):
        action_index = random.randint(0, len(attack_success_no_sound)-1)
        success_lambda = attack_success_no_sound[action_index]
        success = np.random.poisson(success_lambda) >= 2 
        return success, action_index
    
    def get_planned_action_success(self, prey):
        success = False
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
            #print "Training x", training_x
            trained_model = self.gp.fit(training_x, \
                np.reshape(self.action_y_train, (len(self.action_y_train), 1)))
            
            # Ponder your options...
            opinions = []
            for i in range(0, len(attack_success_no_sound)):
                o = trained_model.score(np.array((len(prevs) + 1, self.prev_action_index, i)),\
                    np.array([True]))
                opinions.append(o)
            opinions = opinions/np.max(opinions)
            # Randomly select option (better options have higher probabilites)
            action_index = np.nonzero(np.random.multinomial(1, opinions))[0].tolist()[0]
            # Execute action
            success_lambda = None
            if self.prev_action_index != 0:
                success_lambda = attack_success_no_sound[action_index]
            else:
                if prey.type == AgentType.fish:
                    success_lambda = attack_success_soundnfish[action_index]
                else:
                    success_lambda = attack_success_sound[action_index]
            success = np.random.poisson(success_lambda) > 1.5
            # Forget the oldest past incident and commit the new one to memory
            if len(self.action_x_train) > 50:
                self.action_x_train.remove(self.action_x_train[0])
                self.action_y_train.remove(self.action_y_train[0])
            self.event_count = (self.event_count + 1) % 50
            self.action_x_train.append((self.prev_action_index, action_index))
            self.action_y_train.append(success)
            self.prev_action_index = action_index
        return success, action_index
            
        