from random_options import *
from tools import *
from solver_algorithm_manual import *
from time import sleep
from move_tiles import *

'''
---To be fixed---
- Make program as universial as possible: dynamic size
- Leaderboard can be performed more elegantly with dictioneries
- And leaderboard spacing can be fixed
''' 

def Engine(N, M, goal, prob_doubleM, points, mode):
    matrix = np.zeros([N, N])           #Creating matrix
    ran = Random(N, M, prob_doubleM)    #Create random object

    #---Set value to two random tiles---
    i, j = ran.ran_pos()
    matrix[i, j] = ran.ran_val()        #Pick randomly from pick_list
    m = 0
    while m == 0:
        i, j = ran.ran_pos()
        if matrix[i,j] == 0:
            matrix[i,j] = ran.ran_val()
            m += 1

    print_matrix(matrix)            #Printing initial matrix

    num_goal = 0                    #Number of times goal is reached

    while True:
        if mode == 0:
            arrow = input("Please use 'w', 's', 'a' or 'd' to move the tiles: ")
        elif mode == 1:
            arrow = best_swipe_dir(matrix)
            sleep(1.0)

        #UpArrow
        if arrow == "w":
            moves, merges, num_goal, points = move_up(matrix, num_goal, points, goal)  
                                
        #DownArrow
        if arrow == "s":
            moves, merges, num_goal, points = move_down(matrix, num_goal, points, goal)

        #LeftArrow
        if arrow == "a":
            moves, merges, num_goal, points = move_left(matrix, num_goal, points, goal)

        #RightArrow
        if arrow == "d":
            moves, merges, num_goal, points = move_right(matrix, num_goal, points, goal)

        #---Adding new tile on random empty spot---
        listfori = []
        listforj = []

        counter = 0
        for i in range(4):
            for j in range(4):
                if matrix[i,j]==0:
                    counter+=1
                    listfori.append(i)
                    listforj.append(j)
            
        if counter > 0:
            if moves > 0 or merges > 0:
                if counter > 1:
                    randomindex = listfori.index(random.choice(listfori))
                    matrix[listfori[randomindex],listforj[randomindex]] = ran.ran_val()
                    print_matrix(matrix)
                    print ("Points: ", int(points))
                else:
                    matrix[listfori[0]][listforj[0]] = ran.ran_val()
                    print_matrix(matrix)
                    print ("Points: ", int(points))
            else:
                print ("Please swipe in another direction!")
            
        else:
            d = 0
            for i in range(N-1):
                for j in range(N):
                    if matrix[i,j]==matrix[i+1,j]:
                        d += 1
                        
            for i in range(N):
                for j in range(N-1):
                    if matrix[i,j]==matrix[i,j+1]:
                        d += 1
                        
            if d == 0:     
                print (color.RED + "Game over" + color.END)
                name = input("Please enter your name, mister: ")
                leaderboard(name, points, '.leaderboard')
                break

        if num_goal > 0:
            print ("Congratulation, you've reached %.d for the %.d. times" % (goal,num_goal))
