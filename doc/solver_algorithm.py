def best_swipe_dir(matrix):
    
    # --- Check if merge is possible ---
    for i in range(4):
        for j in range(3):
            if matrix[i,j] != 0:
                if matrix[i,j] == matrix[i,j+1]:
                    print("Merge right")
                    return "d"
                    break
                
    for i in range(4):
        for j in range(2):
            if matrix[i,j] != 0:
                if matrix[i,j] == matrix[i,j+2] and matrix[i,j+1] == 0:
                    print("Merge right")
                    return "d"
                    break
    
    for i in range(4):
        if matrix[i,0] != 0:
            if matrix[i,0] == matrix[i,3] and matrix[i,1] == matrix[i,2] == 0:
                print("Merge right")
                return "d"
                break
                
    for i in range(3):
        for j in range(4):
            if matrix[i,j] != 0:
                if matrix[i,j] == matrix[i+1,j]:
                    print("Merge down")
                    return "s"
                    break   
    
    for i in range(2):
        for j in range(4):
            if matrix[i,j] != 0:
                if matrix[i,j] == matrix[i+2,j] and matrix[i+1,j] == 0:
                    print("Merge down")
                    return "s"
                    break   
    
    for j in range(4):
        if matrix[0,j] != 0:
            if matrix[0,j] == matrix[3,j] and matrix[1,j] == matrix[2,j] == 0:
                print("Merge down")
                return "s"
                break
    
    # --- Check if merge is possible in two moves ---
    for i in range(3):
        for j in range(3):
            if matrix[i,j] != 0:
                if matrix[i,j] == matrix[i+1,j+1] and matrix[i,j+1] == 0:
                    print("Preparing for merge right")
                    return "d"
                    break 
                elif matrix[i+1,j] == matrix[i,j+1] and matrix[i,j] == 0:
                    print("Preparing for merge left")
                    return "a"
                    break 
    
    
    # --- Check if move is possible ---
    for i in range(4):
        for j in range(3):
            if matrix[i,j] != 0 and matrix[i,j+1] == 0:
                print("Move right")
                return "d"
                break
                
    for i in range(3):
        for j in range(4):
            if matrix[i,j] != 0 and matrix[i+1,j] == 0:
                print("Move down")
                return "s"
                break 
                
    for i in range(4):
        for j in range(3):
            if matrix[i,j+1] != 0 and matrix[i,j] == 0:
                print("Move left")
                return "a"
                break
    
    for i in range(3):
        for j in range(4):
            if matrix[i+1,j] != 0 and matrix[i,j] == 0:
                print("Move up")
                return "w"
                break
                
    return "w"
