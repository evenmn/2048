from move_tiles import *
import numpy as np

def best_swipe_dir(matrix):

    # Constructing weight matrix
    depth = 2
    structure = []
    [structure.append(4) for i in range(depth)] 
    W = np.zeros(shape=structure)
    
    operations = ["up", "down", "left", "right"]
    
    def reg_func(matrix, depth, counter=0):
        for operation in operations:
            matrix = np.zeros([4, 4])
            matrix[3,2] = 2
            matrix[0,2] = 2
        
            stat = Mover(matrix, 0, 0, 2048)
            call = "stat.move_%s()[3]" % operation
            
            W[counter].fill(eval(call))
            print(W)
            print(operation)
            print(matrix)
            
            counter += 1
            print(counter)
            if counter < depth:
                reg_func(matrix, depth, counter)
                
    reg_func(matrix, depth)
    

    return W
    
    
    
matrix = np.zeros([4, 4])
matrix[3, 2] = 2
matrix[0, 2] = 2

W = best_swipe_dir(matrix)
print(W)
