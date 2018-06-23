#---Print color---
class color:
   PURPLE    = '\033[95m'
   CYAN      = '\033[96m'
   DARKCYAN  = '\033[36m'
   BLUE      = '\033[94m'
   GREEN     = '\033[92m'
   YELLOW    = '\033[93m'
   RED       = '\033[91m'
   BOLD      = '\033[1m'
   UNDERLINE = '\033[4m'
   GRAY      = '\033[2m'
   KURSIV    = '\033[3m'
   END       = '\033[0m'
   
#---Printing matrix---
def print_matrix(matrix):

    list = []
    for i in range(4):
        for j in range(4):
            if int(matrix[i,j]) == 0:
                list.append(color.GRAY + "0" + color.END)
            else:
                list.append(color.BOLD + "%.d" % int(matrix[i,j]) + color.BOLD)

    print (chr(27) + "[2J")     #Clear terminal 
    print ("\t")
    print ("\t", list[0],  "\t", list[1],  "\t", list[2],  "\t", list[3],  "\n")
    print ("\t", list[4],  "\t", list[5],  "\t", list[6],  "\t", list[7],  "\n")
    print ("\t", list[8],  "\t", list[9],  "\t", list[10], "\t", list[11], "\n")
    print ("\t", list[12], "\t", list[13], "\t", list[14], "\t", list[15], "\n")
    
    
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
