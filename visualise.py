import pygame
import threading
from client import main as clientMain
from colors import colors as C
from math import floor
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

def read_integers(filename):
    with open(filename,'r') as f:
        return f.read().split()

content = read_integers('positions.txt')
index=0
loadBalancing=False
gridsize=int(content[index])
index+=1
useColors=True
targetEdge=5
pos=[]
isAttractor=[[False for _ in range(ROWS//gridsize)]for i in range(ROWS//gridsize)]   

boxSize=gridsize-2
numberOfParticals=int(content[index])
index+=1

iterations=int(content[index])
index+=1

edgesAlongRow=int(content[index])
index+=1

isAttractor=[[False for _ in range(ROWS//gridsize)]for i in range(ROWS//gridsize)]   
for i in range(ROWS//gridsize):
    for j in range(ROWS//gridsize):
        if int(content[index])==1 :
            isAttractor[i][j]=True
        index+=1

for i in range(numberOfParticals):
    l=[]
    for j in range(3*iterations):
        l.append(int(content[index]))
        index+=1
    pos.append(l)

edgeBoundariesVisible=True
writePosToFile=True
FILE_NAME="positions.txt"
file = None

edgeNum=edgesAlongRow*edgesAlongRow
edgeGridSize=((ROWS//gridsize)//(edgesAlongRow))*gridsize
attractor=None
pygame.init()
window = pygame.display.set_mode((COLUMNS,ROWS))
pygame.display.set_caption("HOUSE GRID")
window.fill(WHITE)
pygame.display.update()
    
def putEdges():
    for j in range(edgeNum):        
        x=j%edgesAlongRow
        y=j//edgesAlongRow
        xmid=2+x*edgeGridSize+((edgeGridSize//2)//gridsize)*gridsize
        ymid=2+y*edgeGridSize+((edgeGridSize//2)//gridsize)*gridsize
        if useColors:
            pygame.draw.rect(window,C[j],(xmid,ymid,boxSize,boxSize),0,0)
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


for i in range(ROWS//gridsize):
    for j in range(ROWS//gridsize):
        if isAttractor[i][j]:
            pygame.draw.rect(window,ATTRACT, (i*gridsize+2,j*gridsize+2,boxSize,boxSize),0,0)
        pygame.display.update()

class DummyClient(threading.Thread):
    def __init__(self,positions):
      threading.Thread.__init__(self)
      self.positions=positions
      self.index=0
      
    def run(self):
       while self.index<len(self.positions):
           sleep(0.3)
           self.index+=3
           
    def getPos(self):
        return [self.positions[min(self.index,len(self.positions)-3)],self.positions[min(self.index+1,len(self.positions)-2)]],C[self.positions[min(self.index+2,len(self.positions)-1)]]
        
    


putEdges()
run=True
dummyCliThreads=[]
print(iterations)
for i in range(numberOfParticals):
    l=[ int(x) for x in pos[i]]
    thread1 = DummyClient(l)
    dummyCliThreads.append(thread1)
    
    
for dct in dummyCliThreads:
    dct.start()
    
currIter=0
lastPos=[[0 for _ in range(2)] for j in range(numberOfParticals)]
firstPass=True
while run:
    for i in range(numberOfParticals):
        if not firstPass:
            x=(lastPos[i][0])
            y=(lastPos[i][1])
            if isAttractor[min(x,(ROWS//gridsize)-1)][min(y,(ROWS//gridsize)-1)]:
                pygame.draw.rect(window, ATTRACT, (floor(x/gridsize)*gridsize+2,floor(y/gridsize)*gridsize+2,boxSize,boxSize),0,0)
            else:
                pygame.draw.rect(window, WHITE, (floor(x/gridsize)*gridsize+2,floor(y/gridsize)*gridsize+2,boxSize,boxSize),0,0)
        curPos,colorParticle=dummyCliThreads[i].getPos()
        lastPos[i]=curPos
        pygame.draw.rect(window, colorParticle, (floor(curPos[0]/gridsize)*gridsize+2,floor(curPos[1]/gridsize)*gridsize+2,boxSize,boxSize),0,0)
        pygame.display.update()
    if firstPass:
        firstPass=False
    putEdges()
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit()
            run=False

