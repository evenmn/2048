from random_options import *
from tools import *

'''
---To be fixed---
- Make program as universial as possible: dynamic size
- Leaderboard can be performed more elegantly with dictioneries
- And leaderboard spacing can be fixed
'''

def Engine(N, M, goal, prob_doubleM, points):
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
        arrow = input("Please use 'w', 's', 'a' or 'd' to move the tiles: ")
        moves = 0           #Number of tiles moving by one swipe
        merges = 0          #Number of tiles merging by one swipe

        #UpArrow
        if arrow == "w":

            #---Move the tiles---
            i=0

            for j in range(4):
                if matrix[i,j]!=0 or matrix[i+1,j]!=0 or matrix[i+2,j]!=0 or matrix[i+3,j]!=0:

                    if matrix[i,j]==0:
                        moves += 1
                        while matrix[i,j]==0:
                            matrix[i,j]=matrix[i+1,j]   
                            matrix[i+1,j]=matrix[i+2,j]    
                            matrix[i+2,j]=matrix[i+3,j]    
                            matrix[i+3,j]=0
	                    
                    if matrix[i+1,j]==0 and (matrix[i+2,j]!=0 or matrix[i+3,j]!=0):
                        moves += 1
                        while matrix[i+1,j]==0:  
                            matrix[i+1,j]=matrix[i+2,j]    
                            matrix[i+2,j]=matrix[i+3,j]
                            matrix[i+3,j]=0
	                    
                    if matrix[i+2,j]==0 and (matrix[i+3,j]!=0):
                        moves += 1
                        while matrix[i+2,j]==0:
                            matrix[i+2,j]=matrix[i+3,j]   
                            matrix[i+3,j]=0
	    
            #---Merge the tiles---
            i=0

            for j in range(4):
                if matrix[i,j]==matrix[i+1,j]:
                    matrix[i,j]=matrix[i,j]+matrix[i+1,j]
                    matrix[i+1,j]=matrix[i+2,j]
                    matrix[i+2,j]=matrix[i+3,j]
                    matrix[i+3,j]=0
                    points += matrix[i,j]
                    if matrix[i,j] == goal:
                        num_goal += 1
                    if matrix[i,j] != 0:
                        merges += 1
	                
                if matrix[i+1,j]==matrix[i+2,j]:
                    matrix[i+1,j]=matrix[i+1,j]+matrix[i+2,j]
                    matrix[i+2,j]=matrix[i+3,j]
                    matrix[i+3,j]=0
                    points += matrix[i+1,j]
                    if matrix[i+1,j] == goal:
                        num_goal += 1
                    if matrix[i+1,j]!=0:
                        merges += 1
	                
                if matrix[i+2,j]==matrix[i+3,j]:
                    matrix[i+2,j]=matrix[i+2,j]+matrix[i+3,j]
                    matrix[i+3,j]=0
                    points += matrix[i+2,j]
                    if matrix[i+2,j] == goal:
                        num_goal += 1
                    if matrix[i+2,j]!=0:
                        merges += 1
                                
        #DownArrow
        if arrow == "s":

            #---Move the tiles---
            i=0
            
            for j in range(4):
                if matrix[i,j]!=0 or matrix[i+1,j]!=0 or matrix[i+2,j]!=0 or matrix[i+3,j]!=0:

                    if matrix[i+3,j]==0:
                        moves += 1
                        while matrix[i+3,j]==0: 
                            matrix[i+3,j]=matrix[i+2,j]   
                            matrix[i+2,j]=matrix[i+1,j]    
                            matrix[i+1,j]=matrix[i,j]    
                            matrix[i,j]=0
	                    
                    if matrix[i+2,j]==0 and (matrix[i+1,j]!=0 or matrix[i,j]!=0):
                        moves += 1
                        while matrix[i+2,j]==0:  
                            matrix[i+2,j]=matrix[i+1,j]    
                            matrix[i+1,j]=matrix[i,j]
                            matrix[i,j]=0
	                    
                    if matrix[i+1,j]==0 and (matrix[i,j]!=0):
                        moves += 1
                        while matrix[i+1,j]==0:
                            matrix[i+1,j]=matrix[i,j]   
                            matrix[i,j]=0
	    
            #---Merge the tiles---
            i=0

            for j in range(4):
                if matrix[i+3,j]==matrix[i+2,j]:
                    matrix[i+3,j]=matrix[i+3,j]+matrix[i+2,j]
                    matrix[i+2,j]=matrix[i+1,j]
                    matrix[i+1,j]=matrix[i,j]
                    matrix[i,j]=0
                    points += matrix[i+3,j]
                    if matrix[i+3,j] == goal:
                        num_goal += 1
                    if matrix[i+3,j]!=0:
                        merges += 1
	                
                if matrix[i+2,j]==matrix[i+1,j]:
                    matrix[i+2,j]=matrix[i+2,j]+matrix[i+1,j]
                    matrix[i+1,j]=matrix[i,j]
                    matrix[i,j]=0
                    points += matrix[i+2,j]
                    if matrix[i+2,j] == goal:
                        num_goal += 1
                    if matrix[i+2,j]!=0:
                        merges += 1
	                
                if matrix[i+1,j]==matrix[i,j]:
                    matrix[i+1,j]=matrix[i+1,j]+matrix[i,j]
                    matrix[i,j]=0
                    points += matrix[i+1,j]
                    if matrix[i+1,j] == goal:
                        num_goal += 1
                    if matrix[i+1,j]!=0:
                        merges += 1

        #LeftArrow
        if arrow == "a":

            #---Move the tiles---
            j=0

            for i in range(4):
                if matrix[i,j]!=0 or matrix[i,j+1]!=0 or matrix[i,j+2]!=0 or matrix[i,j+3]!=0:

                    if matrix[i,j]==0:
                        moves += 1
                        while matrix[i,j]==0: 
                            matrix[i,j]=matrix[i,j+1]   
                            matrix[i,j+1]=matrix[i,j+2]    
                            matrix[i,j+2]=matrix[i,j+3]    
                            matrix[i,j+3]=0
	                    
                    if matrix[i,j+1]==0 and (matrix[i,j+2]!=0 or matrix[i,j+3]!=0):
                        moves += 1
                        while matrix[i,j+1]==0:  
                            matrix[i,j+1]=matrix[i,j+2]    
                            matrix[i,j+2]=matrix[i,j+3]
                            matrix[i,j+3]=0
	                    
                    if matrix[i,j+2]==0 and (matrix[i,j+3]!=0):
                        moves += 1
                        while matrix[i,j+2]==0:
                            matrix[i,j+2]=matrix[i,j+3]   
                            matrix[i,j+3]=0

            #---Merge the tiles---
            j=0

            for i in range(4):
                if matrix[i,j]==matrix[i,j+1]:
                    matrix[i,j]=matrix[i,j]+matrix[i,j+1]
                    matrix[i,j+1]=matrix[i,j+2]
                    matrix[i,j+2]=matrix[i,j+3]
                    matrix[i,j+3]=0
                    points += matrix[i,j]
                    if matrix[i,j] == goal:
                        num_goal += 1
                    if matrix[i,j]!=0:
                        merges += 1
	                
                if matrix[i,j+1]==matrix[i,j+2]:
                    matrix[i,j+1]=matrix[i,j+1]+matrix[i,j+2]
                    matrix[i,j+2]=matrix[i,j+3]
                    matrix[i,j+3]=0
                    points += matrix[i,j+1]
                    if matrix[i,j+1] == goal:
                        num_goal += 1
                    if matrix[i,j+1]!=0:
                        merges += 1
	                
                if matrix[i,j+2]==matrix[i,j+3]:
                    matrix[i,j+2]=matrix[i,j+2]+matrix[i,j+3]
                    matrix[i,j+3]=0
                    points += matrix[i,j+2]
                    if matrix[i,j+2] == goal:
                        num_goal += 1
                    if matrix[i,j+2]!=0:
                        merges += 1

        #RightArrow
        if arrow == "d":

            #---Move the tiles---
            j=0

            for i in range(4):
                if matrix[i,j]!=0 or matrix[i,j+1]!=0 or matrix[i,j+2]!=0 or matrix[i,j+3]!=0:

                    if matrix[i,j+3]==0:
                        moves += 1
                        while matrix[i,j+3]==0: 
                            matrix[i,j+3]=matrix[i,j+2]   
                            matrix[i,j+2]=matrix[i,j+1]    
                            matrix[i,j+1]=matrix[i,j]    
                            matrix[i,j]=0
	                    
                    if matrix[i,j+2]==0 and (matrix[i,j+1]!=0 or matrix[i,j]!=0):
                        moves += 1
                        while matrix[i,j+2]==0:  
                            matrix[i,j+2]=matrix[i,j+1]    
                            matrix[i,j+1]=matrix[i,j]
                            matrix[i,j]=0
	                    
                    if matrix[i,j+1]==0 and (matrix[i,j]!=0):
                        moves += 1
                        while matrix[i,j+1]==0:
                            matrix[i,j+1]=matrix[i,j]   
                            matrix[i,j]=0

            #---Merge the tiles---
            j=0
	    
            for i in range(4):
                if matrix[i,j+3]==matrix[i,j+2]:
                    matrix[i,j+3]=matrix[i,j+3]+matrix[i,j+2]
                    matrix[i,j+2]=matrix[i,j+1]
                    matrix[i,j+1]=matrix[i,j]
                    matrix[i,j]=0
                    points += matrix[i,j+3]
                    if matrix[i,j+3] == goal:
                        num_goal += 1
                    if matrix[i,j+3]!=0:
                        merges += 1

                if matrix[i,j+2]==matrix[i,j+1]:
                    matrix[i,j+2]=matrix[i,j+2]+matrix[i,j+1]
                    matrix[i,j+1]=matrix[i,j]
                    matrix[i,j]=0
                    points += matrix[i,j+2]
                    if matrix[i,j+2] == goal:
                        num_goal += 1
                    if matrix[i,j+2]!=0:
                        merges += 1
	                
                if matrix[i,j+1]==matrix[i,j]:
                    matrix[i,j+1]=matrix[i,j+1]+matrix[i,j]
                    matrix[i,j]=0
                    points += matrix[i,j+1]
                    if matrix[i,j+1] == goal:
                        num_goal += 1
                    if matrix[i,j+1]!=0:
                        merges += 1

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
                    print ("Points: ",int(points))
                else:
                    matrix[listfori[0]][listforj[0]] = ran.ran_val()
                    print_matrix(matrix)
                    print ("Points: ",int(points))
            else:
                print ("Please swipe in another direction!")
            
        else:
            d = 0
            for i in range(N-1):
                for j in range(N-1):
                    if matrix[i,j]==matrix[i+1,j] or matrix[i,j]==matrix[i,j+1]:
                        d += 1
            if d == 0:     
                print (color.RED + "Game over" + color.END)
                name = raw_input("Please enter your name, mister: ")
                leaderboard(name, points, '.leaderboard')
                break

        if num_goal > 0:
            print ("Congratulation, you've reached %.d for the %.d. time" % (goal,num_goal))
