import random
import numpy as np

class Random:
    def __init__(self, N, M, prob_doubleM):
        self.N            = N
        self.M            = M
        self.prob_doubleM = prob_doubleM
        
        
    def ran_pos(self):
        '''Random position'''
        
        N      = self.N
        
        row    = np.random.randint(0, N)
        column = np.random.randint(0, N)
        
        return row, column


    def ran_val(self):
        '''Random value'''
        
        M            = self.M
        prob_doubleM = self.prob_doubleM

        tol          = 0.01
        freq_doubleM = 1/prob_doubleM
        count        = 1
        
        while abs(freq_doubleM-int(freq_doubleM))>tol:
            freq_doubleM = freq_doubleM*2
            count += 1
            
        pick_list = []      #Filled with freq_doubleM Ms
        pick_list = pick_list + [M]*(int(freq_doubleM) - len(pick_list))
        
        for i in range(count):
            pick_list[i]=2*M
            
        return random.choice(pick_list)
