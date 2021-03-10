from time import sleep
import threading
import random
from client import main as clientMain

ROWS   =500
COLUMNS=500
gridsize=25
boxSize=gridsize-2
numberOfParticals=140
edgesAlongRow=4

# class edge():
#     def __init__(self,mythread,clientThreads,boundaries):
#         self.clientThreads=clientThreads
#         self.boundaries=boundaries
#         self.cost=0
#         self.mythread=mythread
#         self.on=True
    
#     def signIn(self,clientThread):
#         self.clientThreads.append(clientThread)
#         clientThread.syncNodeWithEdge(self.mythread)
#         return True

#     def signOut(self,clientThread):
#         try:
#             self.clientThreads.remove(clientThread)
#             return True
#         except:
#             return False
    
#     def turnOff(self):
#         self.on=False
 
#     def egdeRun(self):
#         while(self.on):
#             sleep(0.3)
#             pass
#         return self.on

class myClientThread (threading.Thread):
    def __init__(self, threadID):
      threading.Thread.__init__(self)
      self.threadID = threadID
      myPresentX=(random.randint(0,COLUMNS-1))//gridsize*gridsize 
      myPresentY=(random.randint(0,ROWS-1))//gridsize*gridsize 
      self.node = node(self,myPresentX,myPresentY)
      self.turnoff=False
    
    def run(self):
       clientMain(ROWS,COLUMNS,self.node,self.turnoff)
    
    def syncNodeWithEdge(self,edgeThread):
        self.node.setEdge(edgeThread)
        
        
    def getCoorColors(self):
        return self.node.x,self.node.y, [self.node.colorR,self.node.colorG,self.node.colorB]
    
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
        self.colorR=250
        self.colorG=120
        self.colorB=120
        self.cost=0
        
    def setEdge(self,edgeThread):
        self.edgeThread=edgeThread
        self.boundaries=edgeThread.boundaries
        
          
    def setVx(self,Vx):
        self.Vx=Vx
        
    def setVy(self,Vy):
        self.Vy=Vy
    def setx(self,x):
        self.x=x
          
    def sety(self,y):
        self.y=y

