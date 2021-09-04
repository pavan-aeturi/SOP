from time import sleep
import threading
import random
from client import main as clientMain
from math import floor
ROWS   =500
COLUMNS=500

class myClientThread (threading.Thread):
    def __init__(self,WritePosToFile,threadID,Attractor=None,iterations=float('inf'),gridsize=25):
      threading.Thread.__init__(self)
      self.threadID = threadID
      myPresentX=(random.randint(0,COLUMNS-1))//gridsize*gridsize 
      myPresentY=(random.randint(0,ROWS-1))//gridsize*gridsize 
      self.node = node(myPresentX,myPresentY,self,iterations,gridsize)
      self.turnoff=False
      self.gridsize=gridsize
      self.writePosToFile=WritePosToFile
      self.attractor=Attractor
      
    def run(self):
       clientMain(ROWS,COLUMNS,self.node,self.turnoff,self.writePosToFile,self.attractor)
    #    print("done")
    
    def syncNodeWithEdge(self,edgeThread,potentialThread):
        self.node.setEdge(edgeThread,potentialThread)
        
        
    def getCoorColors(self):
        return floor(self.node.x/self.gridsize)*self.gridsize+2,floor(self.node.y/self.gridsize)*self.gridsize+2, self.node.colors
    
    def switchOff(self):
        self.turnoff=True


class node():
    def __init__(self,x=2,y=2,myThread=None,iterations=float('inf'),gridsize=25): 
        self.Vx=1
        self.Vy=1
        self.x=x
        self.y=y
        self.iterations=iterations
        self.myThread=myThread
        self.potentialThread=None
        self.edgeThread=None
        self.boundaries=None
        self.boxsize=gridsize
        self.positions=[]
        self.colors=[250,120,120]
        self.cost=0
        
    def setEdge(self,edgeThread,potentialThread):
        self.edgeThread=edgeThread
        self.potentialThread=potentialThread
        self.boundaries=potentialThread.boundaries
        self.colors=edgeThread.colors

    def setVx(self,Vx):
        self.Vx=Vx
        
    def setVy(self,Vy):
        self.Vy=Vy
    def setx(self,x):
        self.x=x
          
    def sety(self,y):
        self.y=y

