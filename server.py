import pygame
from client import main as clientMain
import threading
import random
from  time import sleep
from edge import myClientThread,node


WHITE  =[255,255,255]
SUBGRID=[150,150,150]
EDGE   =[0,200,150]
GRID   =[220,220,220] 
NODE   =[250,120,120]

ROWS   =500
COLUMNS=500
gridsize=25
boxSize=gridsize-2
numberOfParticals=150
edgesAlongRow=4

ClientThreads=[]
edgeThreads=[]

pos=[]
edgeNum=edgesAlongRow*edgesAlongRow
edgeGridSize=((ROWS//gridsize)//(edgesAlongRow))*gridsize

class edgeClients(threading.Thread):
    def __init__(self, threadID,firstX,lastX,firstY,lastY,clientThreads=[]):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.boundaries= [[firstX,lastX],[firstY,lastY]]
        self.clientThreads=[]
        
    def addNodes(self,n):
        self.clientThreads.append(n)
        n.syncNodeWithEdge(self)
        
    def returnMyEdge(self,nodeThread,boundary):
        e=self
        for i in range(len(edgeThreads)):
            if edgeThreads[i].checkMyboundaries(boundary):
                   e=edgeThreads[i]
        self.clientThreads.remove(nodeThread)
        e.addNodes(nodeThread)
        return e
        
    def checkMyboundaries(self,boundary):
       
        if self.boundaries[0][0]<=boundary[0] and self.boundaries[0][1]>=boundary[0]:
            if self.boundaries[1][0]<=boundary[1] and self.boundaries[1][1]>=boundary[1]:
                return True
        
        return False


    
def putEdges(et=None):
    for j in range(edgeNum):
        x=j%edgesAlongRow
        y=j//edgesAlongRow
        
        xmid=2+x*edgeGridSize+((edgeGridSize//2)//gridsize)*gridsize
        ymid=2+y*edgeGridSize+((edgeGridSize//2)//gridsize)*gridsize
        pygame.draw.rect(window,EDGE,(xmid,ymid,boxSize,boxSize),0,0)
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

for i in range(numberOfParticals):
    thread1 = myClientThread(i)
    myPresentX,myPresentY,colors=thread1.getCoorColors()
    x=myPresentX//(edgeGridSize)
    y=myPresentY//(edgeGridSize)
    edgeThreads[int(y*edgesAlongRow+x)].addNodes(thread1)
    thread1.syncNodeWithEdge(edgeThreads[int(y*edgesAlongRow+x)])
    ClientThreads.append(thread1)
    
for i in range(numberOfParticals):
    ClientThreads[i].start()
    myPresentX,myPresentY,colors=ClientThreads[i].getCoorColors()
    pos.append([myPresentX,myPresentY])
    pygame.draw.rect(window,colors, (myPresentX,myPresentY,boxSize,boxSize),0,0)
    putEdges()
    pygame.display.update()
    
    
while True:
    for i in range(numberOfParticals): 
        pygame.draw.rect(window, WHITE, (pos[i][0],pos[i][1],boxSize,boxSize),0,0)
        myPresentX,myPresentY,colors=ClientThreads[i].getCoorColors()
        pygame.draw.rect(window, colors, (myPresentX,myPresentY,boxSize,boxSize),0,0)
        putEdges()
        pos[i]=[myPresentX,myPresentY]
        pygame.display.update()

    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit()
            