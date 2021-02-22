import pygame
from client import main
import threading

from  time import sleep


WHITE  =[255,255,255]
GRID1  =[234,191,159]
GRID   =[220,220,220] 
NODE   =[250,120,120]

ROWS   =500
COLUMNS=500

gridsize=10
numberOfParticals=500



boxSize=gridsize-2
class node():
    def __init__(self,x=2,y=2): 
        self.Vx=1
        self.Vy=1
        self.x=x
        self.y=y
        self.boxsize=gridsize
        
    def setVx(self,Vx):
        self.Vx=Vx
    def setVy(self,Vy):
        self.Vy=Vy
    def setx(self,x):
        self.x=x
    def sety(self,y):
        self.y=y

    

class myClientThread (threading.Thread):
    def __init__(self, threadID):
      threading.Thread.__init__(self)
      self.threadID = threadID
      self.node = node()
    
    def run(self):
       main(ROWS,COLUMNS,self.node)
        
    def getCoordinates(self):
        return self.node.x,self.node.y

                   
pygame.init()
window = pygame.display.set_mode((COLUMNS,ROWS))
pygame.display.set_caption("HOUSE GRID")
window.fill(WHITE)
pygame.display.update()

for i in range(0,500,gridsize):
    pygame.draw.rect(window, GRID, (i,0,2,500),0,5)
for i in range(0,500,gridsize):
    pygame.draw.rect(window, GRID, (0,i,500,2),0,5)

pygame.display.update()

ClientThreads=[]

pos=[]


for i in range(numberOfParticals):
    thread1 = myClientThread(i)
    thread1.start()
    myPresentX,myPresentY=thread1.getCoordinates()
    pos.append([myPresentX,myPresentY])
    pygame.draw.rect(window, NODE, (myPresentX,myPresentY,boxSize,boxSize),0,0)
    pygame.display.update()
    ClientThreads.append(thread1)
    

    
while True:
    for i in range(numberOfParticals): 
        pygame.draw.rect(window, WHITE, (pos[i][0],pos[i][1],boxSize,boxSize),0,0)
        myPresentX,myPresentY=ClientThreads[i].getCoordinates()
        pygame.draw.rect(window, NODE, (myPresentX,myPresentY,boxSize,boxSize),0,0)
        pos[i]=[myPresentX,myPresentY]
        pygame.display.update()

    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit()
            