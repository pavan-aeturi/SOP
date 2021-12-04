import pygame
import threading
from math import ceil
from colors import colors as C
from edge import myClientThread
from attractor import getAttractorArea,getOnlyAttractor

WHITE  =[255,255,255]
SUBGRID=[150,150,150]
EDGE   =[0,200,150]
GRID   =[220,220,220]
NODE   =[250,120,120]
ATTRACT=[100,50,100]
ROWS   =500
COLUMNS=500
REPEL=[255,255,191]
loadBalancing=False
gridsize=25
useColors=True
targetEdge=5
iterations=10
boxSize=gridsize-2
numberOfParticals=1
edgesAlongRow=4
threshold=1.5
attractorSize=20
ClientThreads=[]
edgeThreads=[]
edgeBoundariesVisible=True
writePosToFile=True
FILE_NAME="positions.txt"
file = None

pos=[]
edgeNum=edgesAlongRow*edgesAlongRow
edgeGridSize=((ROWS//gridsize)//(edgesAlongRow))*gridsize
attractor=None
pygame.init()
window = pygame.display.set_mode((COLUMNS,ROWS))
pygame.display.set_caption("HOUSE GRID")
window.fill(WHITE)
pygame.display.update()

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
        self.faceNeighbours=[]
        self.cornerNeighbours=[]
        if useColors:
            self.colors=C[threadID]
        else:
            self.colors=NODE
    
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
        e=nodeThread.node.potentialThread
        myReale=nodeThread.node.potentialThread
        for ed in (e.faceNeighbours+e.cornerNeighbours):
            if ed.checkMyboundaries(boundary):
                   e=ed
                   myReale=e
                   break
        if loadBalancing and len(e.clientThreads)>=ceil(threshold*numberOfParticals/(edgesAlongRow*edgesAlongRow)):
            e=returnCloser(myReale.faceNeighbours,boundary) or myReale
            if e is myReale:
                e = returnCloser(myReale.cornerNeighbours,boundary) or myReale

        self.clientThreads.remove(nodeThread)
        e.addNodes(nodeThread,myReale)
        return e,myReale
        
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
        if useColors:
            pygame.draw.rect(window,C[j],(xmid,ymid,boxSize,boxSize),0,0)
        if et!=None:
            thread1=edgeClients(j,x*edgeGridSize,(x+1)*edgeGridSize,y*edgeGridSize,(y+1)*edgeGridSize)
            et.append(thread1)
    if et!=None:
        for e in et:
            e.addNeighbours()
    pygame.display.update()

if edgeBoundariesVisible:
    for i in range(0,ROWS,gridsize):
        pygame.draw.rect(window, GRID, (i,0,2,ROWS),0,5)
    for i in range(0,ROWS,gridsize):
        pygame.draw.rect(window, GRID, (0,i,ROWS,2),0,5)
    for i in range(0,ROWS,((ROWS//edgesAlongRow)//gridsize)*gridsize):
        pygame.draw.rect(window, SUBGRID, (i,0,2,ROWS),0,5)
        pygame.draw.rect(window, SUBGRID, (0,i,ROWS,2),0,5)

pygame.display.update()
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
    thread1 = myClientThread(writePosToFile,i,attractor,iterations,gridsize)
    myPresentX,myPresentY,colors=thread1.getCoorColors()
    x=myPresentX//(edgeGridSize)
    y=myPresentY//(edgeGridSize)
    e=edgeThreads[int(y*edgesAlongRow+x)]
    e.addNodes(thread1,e)
    thread1.syncNodeWithEdge(e,e)
    ClientThreads.append(thread1)

for i in range(ROWS//gridsize):
    for j in range(ROWS//gridsize):
        if isAttractor[i][j]:
            pygame.draw.rect(window,ATTRACT, (i*gridsize+2,j*gridsize+2,boxSize,boxSize),0,0)
        pygame.display.update()
        
if writePosToFile:
    file = open(FILE_NAME, "w")
    file.write(str(gridsize)+" "+str(numberOfParticals)+" "+str(iterations)+" ")
    file.write(str(edgesAlongRow)+" ")
    for i in range(ROWS//gridsize):
        for j in range(ROWS//gridsize):
            file.write(str(1 if isAttractor[i][j]==True else 0)+" ")
    
for i in range(numberOfParticals):
    ClientThreads[i].start()
    myPresentX,myPresentY,colors=ClientThreads[i].getCoorColors()
    pos.append([myPresentX,myPresentY])
    pygame.draw.rect(window,colors, (myPresentX,myPresentY,boxSize,boxSize),0,0)
    pygame.display.update()

runThreads=True
while runThreads:
    for i in range(numberOfParticals):
        x=(pos[i][0])//gridsize
        y=(pos[i][1])//gridsize
        if isAttractor[min(x,(ROWS//gridsize)-1)][min(y,(ROWS//gridsize)-1)]:
            pygame.draw.rect(window, ATTRACT, (pos[i][0],pos[i][1],boxSize,boxSize),0,0)
        else:
            pygame.draw.rect(window, WHITE, (pos[i][0],pos[i][1],boxSize,boxSize),0,0)
        myPresentX,myPresentY,colors=ClientThreads[i].getCoorColors()
        pygame.draw.rect(window, colors, (myPresentX,myPresentY,boxSize,boxSize),0,0)
        putEdges()
        pos[i]=[myPresentX,myPresentY]
        pygame.display.update()
    
    completedThreadCount=0
    for thread1 in ClientThreads:
        if not thread1.is_alive():
            completedThreadCount+=1
    
    if completedThreadCount==len(ClientThreads):
        if writePosToFile and file!=None:
            for thread1 in ClientThreads:
                for pos in thread1.node.positions:
                    file.write(str(pos[0])+" "+str(pos[1])+" "+str(pos[2])+" ")
            file.close()
        pygame.quit()
        runThreads=False
        continue
                
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit()
            runThreads=False
