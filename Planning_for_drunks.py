# -*- coding: utf-8 -*-
"""
Created on Mon Dec 18 18:14:13 2017

@author: gy17a3m
"""

'''The following program aims to do the following...

    Pull in the data file and finds out the pub point and the home points.
    Draws the pub and homes on the screen.
    Models the drunks leaving their pub and reaching their homes, and stores how 
    many drunks pass through each point on the map.
    Draws the density of drunks passing through each point on a map.
    Saves the density map to a file as text.'''
    
'''The basic algorithm is, for each drunk (who will have numbers between 10 and 250 assigned 
    before leaving the pub), move the drunk randomly left/right/up/down in a loop 
    that picks randomly the way it will go. When it hits the correctly numbered house, 
    stop the process and start with the next drunk. At each step for each drunk, add one 
    to the density for that point on the map.'''
    
    
#Imported libraries/modules with built in functions.
import csv #Implements classes to read and write tabular data in CSV format.
import random #Allows for random number in a given range.
import numpy  #For multidimensional array.
import matplotlib.pyplot #2D plotting library.

environment = [] #An empty list

'''Csv reading code which is reading in the in Drunk.txt file.'''

f = open('Drunk.txt', 'r') 
reader = csv.reader(f)
for row in reader:
    rowlist =[]
    for item in row: 
        rowlist.append(float(item))
    environment.append(rowlist)             
f.close()

lsize = len(environment) #Size of the canvas is lsize X lsize.
#print("canvas size = "+str(lsize))


'''Having read in the file now to process the input data and extract the location of	    
   the non-zero boxes. Assuming the boxes are squares, deduce the first coordinate hit, 
   it's size (21, pub, 11, houses) and value (1, pub, 10 house.....).
   '''

place_c = []	#Store coordinate (i1,i2).
place_v = []	#Store valuse 1, 10, 20... unique.
place_l = []	#Store size of square, 21 for pub and 11 for houses.
	    

'''From the first row (index=0), and in each row search for the
   first nonzero entry which defines the start of the square block. 

   Next, since the shapes are square, this entry will stay nonzero until
   the square ends. Then deduce that, which gives the size of the square.

   Note that for every row of the given square only the data for 
   the first occurrence is saved. Below the "ValueError" is to make sure
   only the first entry is saved of the given square and the rest discarded.

   Once the entire canvas is scanned a list of all the squares is produced.
   '''

for row in range(lsize):
	vec = environment[row]	#Vec now represent the current row.
	c = 0 # counter.
	flag = False
	if (vec[0] !=0.0):	 #A square found already. If the first entry of vec[0] itself is non-zero.
		place_v.append(vec[0]) #Append the value
		place_c.append([0,row]) #and the coordinate.
	else: #Continue on through the loop.
		for col in range(1,lsize): 
			if (vec[col] != 0.0): #Keep counting the number of times in the square.
				c += 1  #Condition to count how many times the entry has been non-zero
                           #and is used to get the difference between end and start of non-zero entries 
                           #thus giving the size of square.   
			if (vec[col] == vec[col-1]):  #Either inside the square or totally outside.
				pass
              #If statement checks whether current entry is same as previous one.
              #If yes, then current iteration of col is either totally inside a square or totally outside, and there is nothing to do. .
              #at the boundary.
			else: #Check if append needed.
				if (vec[col] > 0.0): #At left boundary, otherwise vec[col] would be 0.
					try: 
						b=place_v.index(vec[col]) #Provides the index of place_v that has value vec[col].
					except ValueError:
						'''Do something with variable b.'''
						place_v.append(vec[col])  #Append the value
						place_c.append([col,row]) #and the coordinate.
						flag = True
					else:
						flag = False
									
				if (vec[col]== 0.0): #At the right boundary.
					if (flag):
						place_l.append(c) #Has the size of the square.
					c = 0 #Re-initialize. 
                    
del vec #reassigned.

'''Now know the location of the boxes, their sizes, and their numbers.''' 

numbox = len(place_v)	#Number of boxes: one of which is the pub and the rest are houses.
ndrunk = numbox - 1    #Number of drunks = number of houses.

mlist = []
#print("lengths = ",len(place_v),len(place_c),len(place_l))
for i in range(numbox):
	tmp = [place_v[i], place_l[i], place_c[i]] 
	mlist.append(tmp)

del tmp #No longer of use.

mlist.sort() #Sort the list in increasing order of values. 

for i in range(numbox):
	print(i,mlist[i])

pub_loc = mlist[0][2]	#First coordinate hit for the pub.
pbsize = mlist[0][1]	#Size of the pub.

range_ndrunk = list(range(ndrunk))

#Initialize drunks. 

a,b = pub_loc	#Coordinate of the pub.
l = pbsize   #Size of the pub.

drunk_loc = [] #List of coordinates for the drunks (ndrunk x 25).
for i in range_ndrunk:
	
    '''x,y are randomly generated integers in the box representing the pub.'''
	
    x = random.randint(a,a+l-1) #a,b = pub_loc, l = pbsize.
    y = random.randint(b,b+l-1)
	#print(x,y)
    drunk_loc.append([x,y])

print(drunk_loc)	#print initial location (should be inside pub).

def random_move(ndrunk):
	'''Function to perform a random move on square grid
	with four choices, left, right, up and down, with
	periodic boundary. Call a random number to decide which way to move.
	(1,0), (-1,0), (0,1), (0,-1)
	'''
	rr = random.uniform(0,1)	# Call a uniform random number.

	''' range 1  |   range 2   |   range 3   |    range 4     
	------------0.25----------0.50----------0.75----------1.0
         (1,0)        (-1,0)        (0,1)         (0,-1)  
     '''  
	
	if  rr <= 0.25 :					   # range 1
		ndrunk[0] += 1; ndrunk[0] = ndrunk[0]%lsize # Returns the number in range 0 to lsize.
	elif (rr > 0.25) and (rr <= 0.5):	   # range 2
		ndrunk[0] += -1; ndrunk[0] = ndrunk[0]%lsize
	elif (rr > 0.5) and (rr <= 0.75):      # range 3 
		ndrunk[1] += 1; ndrunk[1] = ndrunk[1]%lsize
	else:						       # range 4 
		ndrunk[1] += -1; ndrunk[1] = ndrunk[1]%lsize
	
	return

for i in range_ndrunk:
    nsteps = numpy.zeros([lsize,lsize])	#2d array to save footprints in each grid.
	
    '''Whenever the drunk walks to a coordinate x,y increase nwalks[x][y] by 1.'''

    home_val = mlist[i+1][0]      #The value representing the home of the drunk on the environment.
    home_size = mlist[i+1][1]     #Size of the square (house) for the drunk.
    xhome,yhome = mlist[i+1][2]   #The location of the house.
    #print(drunk_loc[i])

    flag = True
    xa, xb = xhome,xhome+home_size - 1 #The bottom left boundary (xa,ya)
    ya, yb = yhome,yhome+home_size - 1 #The top right boundary   (xb,yb)

    count = 0 #Counter for the number of walks
    while (flag):
        count += 1
        random_move(drunk_loc[i]) #Move randomly left, right, up, down.
        x,y = drunk_loc[i]

        nsteps[x][y] += 1	#Drunk passes through x,y once more.
		
        '''Both if statements below are equivaluet.'''
	    #if (vec[0] >= xa and vec[0] <= xb) and (vec[1] >= ya and vec[1] <= yb): flag = False # The drunk has entered home.
        if (environment[x][y] == home_val):	flag = False # The drunk has entered home.
		
	
    print("number of steps = ",count,"final coordinates = ",drunk_loc[i]) # [xa,ya],[xb,yb])
		
    str_n='' #Newline.
    for i1 in range(lsize): 
        for i2 in range(lsize):
            str_n  += str(i1)+' '+str(i2)+' '+str(nsteps[i1][i2])+'\n' 
				
        str_n += '\n'
		
    f1=open("nwalks"+str(i)+".text",'w') #Write file
    f1.write(str_n)
    f1.close()

    fig,ax = matplotlib.pyplot.subplots(1)
    matplotlib.pyplot.xlim(0, lsize-1)
    matplotlib.pyplot.ylim(0, lsize-1)
    ax.imshow(nsteps)
    rect1 = matplotlib.patches.Rectangle((xhome,yhome),home_size,home_size, fill=None,edgecolor="white",linewidth=1)
    ax.add_patch(rect1)
    rect2 = matplotlib.patches.Rectangle(pub_loc,pbsize,pbsize, fill=None,edgecolor="white",linewidth=1)
    ax.add_patch(rect2)
    ax.text(12, lsize - 24, "Number of steps = "+str(count),color="black")
    matplotlib.pyplot.show()
   