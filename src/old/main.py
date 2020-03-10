from engine import *

#Variables
N = 4                   #System size, NxN
M = 2                   #Starting multiplicator
goal = M**11            #Goal (usually M**11, ex: 2**11=2048)
prob_doubleM = 1/10.    #Probability of getting 2*M, fraction
points = 0              #Initial points
mode = 1                # 0 - Play yourself, 1 - Let computer play

Engine(N, M, goal, prob_doubleM, points, mode)
