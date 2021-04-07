import numpy as np
import matplotlib.pyplot as plt
import threading
import random
from math import ceil
from colors import colors as C
from  time import sleep
from edge_for_performanceTest import myClientThread,node
from attractor import getAttractorArea,getOnlyAttractor

WHITE  =[255,255,255]
SUBGRID=[150,150,150]
EDGE   =[0,200,150]
GRID   =[220,220,220] 
NODE   =[250,120,120]
ATTRACT=[100,50,100]
ROWS   =500
COLUMNS=500 
gridsize=25
loadBalancing=True
boxSize=gridsize-2
numberOfParticals=150
targetEdge=5
edgesAlongRow=4
attractorSize=7
ClientThreads=[]
edgeThreads=[]
iterations=1000
pos=[]
edgeNum=edgesAlongRow*edgesAlongRow
edgeGridSize=((ROWS//gridsize)//(edgesAlongRow))*gridsize
attractor=None

def returnCloser(edges,boundary):
    closest=float('inf')
    e=None
    for ed in (edges):
        if len(ed.clientThreads)<=ceil(1.5*numberOfParticals/(edgesAlongRow*edgesAlongRow)):
            val=ed.findDistance(boundary)
            if closest>val:
                e=ed
                closest=val
    return e

class edgeClients(threading.Thread):
    def __init__(self, threadID,firstX,lastX,firstY,lastY,clientThreads=[]):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.boundaries= [[firstX,lastX],[firstY,lastY]]
        self.clientThreads=[]
        self.cost=0
        self.pingEdges=0
        self.faceNeighbours=[]
        self.cornerNeighbours=[]
        self.colors=C[threadID]
    
    def addNeighbours(self):
        
        for e in (edgeThreads):
            if e!=self:
                left=e.boundaries[0][1]==self.boundaries[0][0] and e.boundaries[1][0]==self.boundaries[1][0]
                right=e.boundaries[0][0]==self.boundaries[0][1] and e.boundaries[1][0]==self.boundaries[1][0]
                top=e.boundaries[0][0]==self.boundaries[0][0] and e.boundaries[1][1]==self.boundaries[1][0]
                bottom=e.boundaries[0][0]==self.boundaries[0][0] and e.boundaries[1][0]==self.boundaries[1][1]
                if left or right or top or bottom:
                    self.faceNeighbours.append(e)
                else :
                    topLeft=e.boundaries[0][1]==self.boundaries[0][0] and e.boundaries[1][1]==self.boundaries[1][0]
                    topRight=e.boundaries[0][0]==self.boundaries[0][1] and e.boundaries[1][1]==self.boundaries[1][0]
                    bottomLeft=e.boundaries[0][1]==self.boundaries[0][0] and e.boundaries[1][0]==self.boundaries[1][1]
                    bootomRight=e.boundaries[0][0]==self.boundaries[0][1] and e.boundaries[1][0]==self.boundaries[1][1]
                    if topLeft or topRight or bottomLeft or bootomRight:
                        self.cornerNeighbours.append(e)
        
    def addNodes(self,n,p):
        self.clientThreads.append(n)
        n.syncNodeWithEdge(self,p)
    
            
    def returnMyEdge(self,nodeThread,boundary):
        # first declare our answer(e) and potential answer(myReale)
        e=self
        myReale=self
        # Now assign present potential thread to our answer(e) and store potential thread in "myReale"
        for ed in (e.faceNeighbours+e.cornerNeighbours):
            if ed.checkMyboundaries(boundary):
                   e=ed
                   myReale=ed
                   break
        # if loadBalaning is True and if our potential thread is busy find if any 
        # faceNeighbours are free if not find any corner Neighbours are free
        # if everyone is busy then its the job of our potential thread to handle the node
        
        if loadBalancing and len(e.clientThreads)>=ceil(1.5*numberOfParticals/(edgesAlongRow*edgesAlongRow)):
            e=returnCloser(myReale.faceNeighbours,boundary) or myReale
            if e is myReale:
                e = returnCloser(myReale.cornerNeighbours,boundary) or myReale
        # Do the handover and takeover 
        self.clientThreads.remove(nodeThread)
        e.addNodes(nodeThread,myReale)
        return e,myReale
        
    def checkMyboundaries(self,boundary):
       
        if self.boundaries[0][0]<=boundary[0] and self.boundaries[0][1]>=boundary[0]:
            if self.boundaries[1][0]<=boundary[1] and self.boundaries[1][1]>=boundary[1]:
                return True
        
        return False
    def increaseCost(self,cost):
        #print(cost)
        self.cost+=cost

    def findDistance(self,loc):
        x=abs((self.boundaries[0][0]+self.boundaries[1][0])/2-loc[0])
        y=abs((self.boundaries[0][1]+self.boundaries[1][1])/2-loc[1])
        return pow(pow(x,2)+pow(y,2),0.5)
    
def putEdges(et=None):
    for j in range(edgeNum):
        x=j%edgesAlongRow
        y=j//edgesAlongRow
        xmid=2+x*edgeGridSize+((edgeGridSize//2)//gridsize)*gridsize
        ymid=2+y*edgeGridSize+((edgeGridSize//2)//gridsize)*gridsize
        if et!=None:
            thread1=edgeClients(j,x*edgeGridSize,(x+1)*edgeGridSize,y*edgeGridSize,(y+1)*edgeGridSize)
            et.append(thread1)
    if et!=None:
        for e in et:
            e.addNeighbours()
    
    


putEdges(edgeThreads)
isAttractor=[[False for _ in range(ROWS//gridsize)]for i in range(ROWS//gridsize)]   
for i in range(targetEdge,targetEdge+1):
    k=getAttractorArea(ROWS//gridsize//edgesAlongRow,attractorSize)
    bxsz=ROWS//gridsize//edgesAlongRow
    for x in range(bxsz):
        for y in range(bxsz):
             isAttractor[(i//edgesAlongRow)*bxsz+x][(i%edgesAlongRow)*bxsz+y]=k[x][y]

attractor=getOnlyAttractor(ROWS//gridsize,isAttractor)

for i in range(numberOfParticals):
    thread1 = myClientThread(i,iterations,attractor)
    myPresentX,myPresentY,colors=thread1.getCoorColors()
    x=myPresentX//(edgeGridSize)
    y=myPresentY//(edgeGridSize)
    e=edgeThreads[int(y*edgesAlongRow+x)]
    e.addNodes(thread1,e)
    thread1.syncNodeWithEdge(e,e)
    ClientThreads.append(thread1)


for i in range(numberOfParticals):
    ClientThreads[i].start()

for i in range(numberOfParticals):
    ClientThreads[i].join()
  

x=["face","center","corner"]
cost =[0 for i in range(3)]
Number=[0 for i in range(3)]


for i in range(len(edgeThreads)):
    index=int()
    if (i%edgesAlongRow==1 or i%edgesAlongRow==2) and (i//edgesAlongRow==1 or i//edgesAlongRow==2):
        index=1
    elif (i%edgesAlongRow==0 or i%edgesAlongRow==3) and (i//edgesAlongRow==0 or i//edgesAlongRow==3):
        index=2
    else:
        index=0
        # print(i%edgesAlongRow)
        # print(i/edgesAlongRow)
        # print("hello")
    #print(edgeThreads[i].cost)
    cost[index]+=edgeThreads[i].cost/iterations
    Number[index]+=edgeThreads[i].pingEdges/(iterations)

left = [1, 2, 3]

cost[0]/=8
cost[1]/=4
cost[2]/=4

Number[0]/=8
Number[1]/=4
Number[2]/=4
# plotting a bar chart
plt.bar(left, cost, tick_label = x,
        width = 0.4, color = 'blue')
  
# naming the x-axis
plt.xlabel('position of edges')
# naming the y-axis
plt.ylabel('operational cost factor of each edge')
# plot title
plt.title('My bar chart!')
  
# function to show the plot
plt.show()

plt.bar(left, Number, tick_label = x,
        width = 0.4, color = 'blue')
plt.ylabel('Number of clients of each edge')
plt.show()