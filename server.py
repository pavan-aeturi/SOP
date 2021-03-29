import pygame
from client import main as clientMain
import threading
import random
from math import ceil
from colors import colors as C
from  time import sleep
from edge import myClientThread,node
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
boxSize=gridsize-2
numberOfParticals=150
edgesAlongRow=4
attractorSize=100
ClientThreads=[]
edgeThreads=[]

pos=[]
edgeNum=edgesAlongRow*edgesAlongRow
edgeGridSize=((ROWS//gridsize)//(edgesAlongRow))*gridsize
attractor=None

class edgeClients(threading.Thread):
    def __init__(self, threadID,firstX,lastX,firstY,lastY,clientThreads=[]):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.boundaries= [[firstX,lastX],[firstY,lastY]]
        self.clientThreads=[]
        self.cost=0
        self.colors=C[threadID]
        
    def addNodes(self,n,f=False):
        self.clientThreads.append(n)
        n.syncNodeWithEdge(self)
    
            
    def returnMyEdge(self,nodeThread,boundary):
        e=self
        for i in range(len(edgeThreads)):
            if edgeThreads[i].checkMyboundaries(boundary):
                   e=edgeThreads[i]
                   break
        if len(e.clientThreads)<=ceil(1.5*numberOfParticals/(edgesAlongRow*edgesAlongRow)):
            self.clientThreads.remove(nodeThread)
            e.addNodes(nodeThread)
        else:
            e=self
            closest=self.findDistance(boundary)
            for i in range(len(edgeThreads)):
                if len(edgeThreads[i].clientThreads)<=ceil(1.5*numberOfParticals/(edgesAlongRow*edgesAlongRow)):
                    val=edgeThreads[i].findDistance(boundary)
                    if closest>val:
                        e=edgeThreads[i]
                        closest=val
            self.clientThreads.remove(nodeThread)
            e.addNodes(nodeThread)
        return e
        
    def checkMyboundaries(self,boundary):
       
        if self.boundaries[0][0]<=boundary[0] and self.boundaries[0][1]>=boundary[0]:
            if self.boundaries[1][0]<=boundary[1] and self.boundaries[1][1]>=boundary[1]:
                return True
        
        return False
    def increaseCost(self,cost):
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
        pygame.draw.rect(window,C[j],(xmid,ymid,boxSize,boxSize),0,0)
        if et!=None:
            thread1=edgeClients(j,x*edgeGridSize,(x+1)*edgeGridSize,y*edgeGridSize,(y+1)*edgeGridSize)
            et.append(thread1)
    pygame.display.update()


pygame.init()
window = pygame.display.set_mode((COLUMNS,ROWS))
pygame.display.set_caption("HOUSE GRID")
window.fill(WHITE)
pygame.display.update()

for i in range(0,ROWS,gridsize):
    pygame.draw.rect(window, GRID, (i,0,2,ROWS),0,5)
for i in range(0,ROWS,gridsize):
    pygame.draw.rect(window, GRID, (0,i,ROWS,2),0,5)
for i in range(0,ROWS,((ROWS//edgesAlongRow)//gridsize)*gridsize):
    pygame.draw.rect(window, SUBGRID, (i,0,2,ROWS),0,5)
    pygame.draw.rect(window, SUBGRID, (0,i,ROWS,2),0,5)

pygame.display.update()
putEdges(edgeThreads)    


isAttractor=getAttractorArea(ROWS//gridsize,attractorSize)

attractor=getOnlyAttractor(ROWS//gridsize,isAttractor)

for i in range(numberOfParticals):
    thread1 = myClientThread(i,attractor)
    myPresentX,myPresentY,colors=thread1.getCoorColors()
    x=myPresentX//(edgeGridSize)
    y=myPresentY//(edgeGridSize)
    edgeThreads[int(y*edgesAlongRow+x)].addNodes(thread1)
    thread1.syncNodeWithEdge(edgeThreads[int(y*edgesAlongRow+x)])
    ClientThreads.append(thread1)

for i in range(ROWS//gridsize):
    for j in range(ROWS//gridsize):
        if isAttractor[i][j]:
            pygame.draw.rect(window,ATTRACT, (i*gridsize+2,j*gridsize+2,boxSize,boxSize),0,0)
        pygame.display.update()


for i in range(numberOfParticals):
    ClientThreads[i].start()
    myPresentX,myPresentY,colors=ClientThreads[i].getCoorColors()
    pos.append([myPresentX,myPresentY])
    pygame.draw.rect(window,colors, (myPresentX,myPresentY,boxSize,boxSize),0,0)
    putEdges()
    pygame.display.update()
    
    
while True:
    for i in range(numberOfParticals):
        x=(pos[i][0]-2)//gridsize
        y=(pos[i][1]-2)//gridsize
        if isAttractor[min(x,(ROWS//gridsize)-1)][min(y,(ROWS//gridsize)-1)]:
            pygame.draw.rect(window, ATTRACT, (pos[i][0],pos[i][1],boxSize,boxSize),0,0)
        else:
            pygame.draw.rect(window, WHITE, (pos[i][0],pos[i][1],boxSize,boxSize),0,0)
        myPresentX,myPresentY,colors=ClientThreads[i].getCoorColors()
        pygame.draw.rect(window, colors, (myPresentX,myPresentY,boxSize,boxSize),0,0)
        putEdges()
        pos[i]=[myPresentX,myPresentY]
        pygame.display.update()

    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit()
            