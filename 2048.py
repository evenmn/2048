import numpy as np
import random

'''
---To be fixed---
- Make program as universial as possible: dynamic size
- Leaderboard can be performed more elegant with dictoneries
- And leaderboard spacing can be fixed
'''

#Variables
N = 4                   #System size, NxN
M = 2                   #Starting multiplicator
goal = M**11            #Goal (usually M**11, ex: 2**11=2048)
prob_doubleM = 1/10.    #Probability of getting 2*M, fraction
points = 0              #Initial points

#---Creating matrix---
matrix = np.zeros([N, N])

#---Initial tile positions---
def ran_pos():
    row = np.random.randint(0, N)
    column = np.random.randint(0, N)
    return row, column

#---Pick number of 2*M correctly (ex. ratio between 4 and 2)---
tol = 0.01
freq_doubleM = 1/prob_doubleM
count = 1
while abs(freq_doubleM-int(freq_doubleM))>tol:
    freq_doubleM = freq_doubleM*2
    count += 1
pick_list = []      #Filled with freq_doubleM Ms
pick_list = pick_list + [M]*(int(freq_doubleM) - len(pick_list))
for i in range(count):
    pick_list[i]=2*M

#---Set value to two random tiles---
i, j = ran_pos()
matrix[i, j] = random.choice(pick_list)        #Pick randomly from pick_list
m = 0
while m == 0:
    i, j = ran_pos()
    if matrix[i,j] == 0:
        matrix[i,j] = random.choice(pick_list)
        m += 1

#---Print color---
class color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   GRAY = '\033[2m'
   KURSIV = '\033[3m'
   END = '\033[0m'

#---Printing matrix---
def print_matrix(matrix):
    print (chr(27) + "[2J")     #Clear terminal 
    print ("\t")
    print ("\t",int(matrix[0,0]),"\t",int(matrix[0,1]),"\t",int(matrix[0,2]),"\t",int(matrix[0,3]),"\n")
    print ("\t",int(matrix[1,0]),"\t",int(matrix[1,1]),"\t",int(matrix[1,2]),"\t",int(matrix[1,3]),"\n")
    print ("\t",int(matrix[2,0]),"\t",int(matrix[2,1]),"\t",int(matrix[2,2]),"\t",int(matrix[2,3]),"\n")
    print ("\t",int(matrix[3,0]),"\t",int(matrix[3,1]),"\t",int(matrix[3,2]),"\t",int(matrix[3,3]),"\n")
print_matrix(matrix)            #Printing initial matrix

#---Gives the leaderboard---
def leaderboard(name, point, filename):
    outfile = open(filename,'a')
    outfile.write('%s %.d\n'%(name,point))
    outfile.close()
    infile = open(filename,'r')
    names = []; points = []
    for line in infile:
        objects = line.split()
        names.append(objects[0])
        points.append(int(objects[1]))
    infile.close()
    indices = sorted(range(len(points)), key=lambda k: points[k])
    points = sorted(points); points = list(reversed(points))
    names_sorted = []; indices = list(reversed(indices))
    for i in range(len(names)):
        names_sorted.append(names[indices[i]])
    print ('--------------------------------------')
    print ('Top 10 highscores of all time:')
    print ('--------------------------------------')
    if len(names)>10:
        for i in range(10):
            print ('%d. %s\t \t\t\t %d'%(i+1,names_sorted[i],int(points[i])))
    else:
        for i in range(len(names)):
            print ('%d. %s\t \t\t\t %d'%(i+1,names_sorted[i],int(points[i])))
    print ('--------------------------------------')

num_goal = 0            #Number of times goal is reached

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
                matrix[listfori[randomindex],listforj[randomindex]] = random.choice(pick_list)
                print_matrix(matrix)
                print ("Points: ",int(points))
            else:
                matrix[listfori[0]][listforj[0]] = random.choice(pick_list)
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
            leaderboard(name, points, '2048_leaderboard.txt')
            break

    if num_goal > 0:
        print ("Congratulation, you've reached %.d for the %.d. time"%(goal,num_goal))
