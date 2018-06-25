class Mover:
    def __init__(self, matrix, num_goal, points, goal):
        self.matrix   = matrix
        self.num_goal = num_goal
        self.points   = points
        self.goal     = goal

    def move_up(self):
        matrix   = self.matrix
        num_goal = self.num_goal
        points   = self.points
        goal     = self.goal

        #---Move the tiles---
        i=0
        moves = 0           #Number of tiles moving by one swipe
        merges = 0          #Number of tiles merging by one swipe

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
        return moves, merges, num_goal, points
        

    def move_down(self):
        matrix   = self.matrix
        num_goal = self.num_goal
        points   = self.points
        goal     = self.goal

        #---Move the tiles---
        i=0
        moves = 0           #Number of tiles moving by one swipe
        merges = 0          #Number of tiles merging by one swipe
        
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
        return moves, merges, num_goal, points
        
        
    def move_left(self):
        matrix   = self.matrix
        num_goal = self.num_goal
        points   = self.points
        goal     = self.goal

        #---Move the tiles---
        j=0
        moves = 0           #Number of tiles moving by one swipe
        merges = 0          #Number of tiles merging by one swipe

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
        return moves, merges, num_goal, points
        

    def move_right(self):
        matrix   = self.matrix
        num_goal = self.num_goal
        points   = self.points
        goal     = self.goal

        #---Move the tiles---
        j=0
        moves = 0           #Number of tiles moving by one swipe
        merges = 0          #Number of tiles merging by one swipe

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
        return moves, merges, num_goal, points
