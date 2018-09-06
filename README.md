# Final-project-planning-for-drunks


Show me the way to go home...
______________________________________

Aims are as follows...

1.	Pull in the data file and find out the pub point and the home points.
2.	Draw the pub and homes on the screen.
3.	Model the drunks leaving their pub and reaching their homes, and store how many drunks pass through each point on the map.
4.	Draw the density of drunks passing through each point on a map.
5.	Save the density map to a file as text.

The basic algorithm is, for each drunk (who will have numbers between 10 and 250 assigned before leaving the pub), 
move the drunk randomly left/right/up/down in a loop that picks randomly the way it will go. When it hits the correctly 
numbered house, stop the process and start with the next drunk. At each step for each drunk, add one to the density 
for that point on the map.
