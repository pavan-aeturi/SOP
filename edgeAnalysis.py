from clientEdgeAnalysis import main as clientMain
import matplotlib.pyplot as plt
import threading
import random
from colors import colors
from  time import sleep
from edge import node

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
numOfIterations=1000
ClientThreads=[]
edgeThreads=[]

class myClientThread (threading.Thread):
    def __init__(self, threadID,gz,cost=3):
      threading.Thread.__init__(self)
      self.threadID = threadID
      myPresentX=(random.randint(0,COLUMNS-1))//gz*gz 
      myPresentY=(random.randint(0,ROWS-1))//gz*gz 
      self.node = node(self,myPresentX,myPresentY)
      self.logOutCost=cost
      self.turnoff=False
    
    def run(self):
        clientMain(ROWS,COLUMNS,self.node,self.turnoff,numOfIterations)
    
    def syncNodeWithEdge(self,edgeThread):
        self.node.setEdge(edgeThread)
        
        
    def getCoorColors(self):
        return self.node.x,self.node.y, self.node.colors
    
    def switchOff(self):
        self.turnoff=True


class edgeClients(threading.Thread):
    def __init__(self, threadID,firstX,lastX,firstY,lastY,clientThreads=[]):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.boundaries= [[firstX,lastX],[firstY,lastY]]
        self.clientThreads=[]
        self.cost=0
        self.colors=colors[0]
        
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
    def increaseCost(self,cost):
        self.cost+=cost



    
def putEdges(edgeNum,edgesAlongRow,edgeGz,gz,et=None):
    for j in range(edgeNum):
        x=j%edgesAlongRow
        y=j//edgesAlongRow
        xmid=2+x*edgeGz+((edgeGz//2)//gz)*gz
        ymid=2+y*edgeGz+((edgeGz//2)//gz)*gz
        if et!=None:
            thread1=edgeClients(j,x*edgeGz,(x+1)*edgeGz,y*edgeGz,(y+1)*edgeGz)
            et.append(thread1)
    

def main(edgesAlongRow=4,cost=3):
    
    edgeNum=edgesAlongRow*edgesAlongRow
    edgeGridSize=((ROWS//gridsize)//(edgesAlongRow))*gridsize
    putEdges(edgeNum,edgesAlongRow,edgeGridSize,gridsize,edgeThreads)    

    for i in range(numberOfParticals):
        thread1 = myClientThread(i,gridsize,cost)
        myPresentX,myPresentY,colors=thread1.getCoorColors()
        x=myPresentX//(edgeGridSize)
        y=myPresentY//(edgeGridSize)
        edgeThreads[int(y*edgesAlongRow+x)].addNodes(thread1)
        thread1.syncNodeWithEdge(edgeThreads[int(y*edgesAlongRow+x)])
        ClientThreads.append(thread1)
    c=0
    
    for i in range(numberOfParticals):
       ClientThreads[i].start()
    for i in range(numberOfParticals):
        ClientThreads[i].join()
    for i in range(numberOfParticals):
       c+=ClientThreads[i].node.cost
    
    return c
    
   
if __name__ == '__main__':
    edgesAR = [1,2,4,5]
    values=[]
    # for i in (edgesAR):
    #     values.append(main(i)/(numberOfParticals*numOfIterations))
    #     ClientThreads=[]
    #     edgeThreads=[]
    
    # fig = plt.figure(figsize = (7, 4))
    
    # plt.bar(edgesAR, values,  color=(0.2, 0.4, 0.6, 0.6))
    
    # plt.xlabel("No of edges along the row")
    # plt.ylabel("cost factor")
    # plt.title("Edge service analysis")
    # plt.show()
    
    arr=[ i for i in range(1,10)]
    x=[]
    y=[]
    z=[]      
    for i in edgesAR:
        for j in range(len(arr)):
            x.append(i*i)
            y.append(arr[j])
            z.append(main(i,arr[j])/(numberOfParticals*numOfIterations))
            ClientThreads=[]
            edgeThreads=[]
        
    fig = plt.figure()
    ax = fig.add_subplot(111,projection="3d")

    ax.scatter(x, y, z, color='green',marker='o')
    ax.set_xlabel('(x) number of edges')
    ax.set_ylabel('(y) cost of login ang logout')
    ax.set_zlabel("(z) cost factor")

    plt.show()
