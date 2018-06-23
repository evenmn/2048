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
