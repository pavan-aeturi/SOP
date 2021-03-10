import threading
from clientDupe import main
from time import sleep
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import matplotlib.pyplot as plt


x=[]
y=[]
z=[]
occupancyPercentage=30
ROWS=500
COLUMNS=500
divOfrows =[10,20,25, 50,100]
arr=[ i for i in range(0,400,5)]
        
for i in range(len(divOfrows)):
    for j in range(len(arr)):
        x.append(divOfrows[i])
        y.append(arr[j])
        z.append(main(ROWS,COLUMNS,divOfrows[i],arr[j],occupancyPercentage))  
     
fig = plt.figure()
ax = fig.add_subplot(111,projection="3d")

ax.scatter(x, y, z, color='green',marker='o')
ax.set_xlabel('(x) size of grid')
ax.set_ylabel('(y) Number of particles')
ax.set_zlabel("(z) % of grids with "+str(occupancyPercentage)+"-"+str(occupancyPercentage+10)+"% occupancy rate")

plt.show()
   
if __name__ == '__main__':
    pass
    