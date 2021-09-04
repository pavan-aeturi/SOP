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
loadBalancing=False
gridsize=25
useColors=True
targetEdge=5
iterations=float('inf')
boxSize=gridsize-2
numberOfParticals=10
edgesAlongRow=4
attractorSize=2
ClientThreads=[]
edgeThreads=[]
edgeBoundariesVisible=True
writePosToFile=False
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
isAttractor=[[False for _ in range(ROWS//gridsize)]for i in range(ROWS//gridsize)]   

for i in range(ROWS//gridsize):
    for j in range(ROWS//gridsize):
        if isAttractor[i][j]:
            pygame.draw.rect(window,ATTRACT, (i*gridsize+2,j*gridsize+2,boxSize,boxSize),0,0)
        pygame.display.update()
  


runThreads=True
while runThreads:
    
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit()
            runThreads=False
