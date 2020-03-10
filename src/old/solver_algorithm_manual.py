from move_tiles import *
from tempfile import TemporaryFile
import numpy as np

def best_swipe_dir(matrix):
    outfile = TemporaryFile()
    np.save(outfile, matrix)

    # Constructing weight matrix
    depth = 3       # Constant
    W = np.zeros(shape=[4,4,4])
    moves  = np.zeros(4)
    merges = np.zeros(4)
    
    arrows     = ["s",    "d",     "a",    "w"]
    operations = ["down", "right", "left", "up"]
    
    # Construct W
    counter = 0
    for operation in operations:
        outfile.seek(0)
        matrix = np.load(outfile)
        call = "move_%s(matrix, 0, 0, 2048)" % operation
        moves[counter], merges[counter], num_goal, points = eval(call)
        
        for i in range(4):
            for j in range(4):
                W[counter,i,j] += points
        
        outfile1 = TemporaryFile()
        np.save(outfile1, matrix)
        
        counter2 = 0
        for operation1 in operations:
            outfile1.seek(0)
            matrix = np.load(outfile1)
            call = "move_%s(matrix, 0, 0, 2048)" % operation1
            moves1, merges1, num_goal1, points1 = eval(call)

            for i in range(4):
                W[counter,counter2,i] += points1
            
            outfile2 = TemporaryFile()
            np.save(outfile2, matrix)
            
            counter3 = 0
            for operation2 in operations:
                outfile2.seek(0)
                matrix = np.load(outfile2)
                call = "move_%s(matrix, 0, 0, 2048)" % operation2
                moves2, merges2, num_goal2, points2 = eval(call)
                
                W[counter, counter2, counter3] += points2
                counter3 += 1
            counter2 += 1
        counter += 1
    
    # Argmax of W
    maximum = 0
    indices = []
    for i in range(4):
        for j in range(4):
            for k in range(4):
                if W[i,j,k] > maximum:
                    indices = []
                    indices.append([i,j,k])
                    maximum = W[i,j,k]
                elif W[i,j,k] == maximum:
                    indices.append([i,j,k])
    '''
    print("W: \n",W)
    print("indices: ", indices)
    print("moves: ", moves)
    print("merges: ", merges)
    print("maximum: ", maximum)
    '''
    
    # Decide move
    if len(indices) > 1:
        if int(maximum) == 0:
            for i in range(4):
                if merges[i] > 0:
                    print('merges = ',merges[i])
                    return arrows[i]
                    break
                elif moves[i] > 0:
                    print('moves = ',moves[i])
                    return arrows[i]
                    break
            return "d"
        else:
            for i in range(4):
                for j in range(len(indices)):
                    if indices[j][0] == i and merges[i] > 0:
                        return arrows[i]
                        break
                    elif indices[j][0] == i and moves[i] > 0:
                        return arrows[i]
                        break
            return "s"
                
    else:
        return arrows(int(indices[0][0]))

'''
matrix = np.zeros([4,4])
matrix[0,0] = 2
matrix[1,0] = 2

print(matrix)
best_swipe_dir(matrix)
'''
