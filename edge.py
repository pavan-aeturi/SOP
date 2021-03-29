from time import sleep
import threading
import random
from client import main as clientMain
from math import floor
ROWS   =500
COLUMNS=500
gridsize=25
boxSize=gridsize-2
numberOfParticals=140
edgesAlongRow=4

class myClientThread (threading.Thread):
    def __init__(self, threadID,Attractor=None):
      threading.Thread.__init__(self)
      self.threadID = threadID
      myPresentX=(random.randint(0,COLUMNS-1))//gridsize*gridsize 
      myPresentY=(random.randint(0,ROWS-1))//gridsize*gridsize 
      self.node = node(self,myPresentX,myPresentY)
      self.turnoff=False
      self.attractor=Attractor
      
    def run(self):
       clientMain(ROWS,COLUMNS,self.node,self.turnoff,self.attractor)
    
    def syncNodeWithEdge(self,edgeThread):
        self.node.setEdge(edgeThread)
        
        
    def getCoorColors(self):
        return floor(self.node.x/gridsize)*gridsize+2,floor(self.node.y/gridsize)*gridsize+2, self.node.colors
    
    def switchOff(self):
        self.turnoff=True


class node():
    def __init__(self,myThread=None,x=2,y=2): 
        self.Vx=1
        self.Vy=1
        self.x=x
        self.y=y
        self.myThread=myThread
        self.edgeThread=None
        self.boundaries=None
        self.boxsize=gridsize
        self.colors=[250,120,120]
        self.cost=0
        
    def setEdge(self,edgeThread):
        self.edgeThread=edgeThread
        self.boundaries=edgeThread.boundaries
        self.colors=edgeThread.colors
    
    def setVx(self,Vx):
        self.Vx=Vx
        
    def setVy(self,Vy):
        self.Vy=Vy
    def setx(self,x):
        self.x=x
          
    def sety(self,y):
        self.y=y

