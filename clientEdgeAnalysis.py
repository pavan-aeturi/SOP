import random
import math
from time import sleep

maxspeed=1
minspeed=1


def main(ROWS,COLUMNS,node,turnoff,numOfIterations):
    cost=0
    boxsize=node.boxsize
    vtempx=random.randint(minspeed,maxspeed)*boxsize
    vtempy=random.randint(minspeed,maxspeed)*boxsize
    Vx=vtempx if (random.randint(1,2)==1) else -vtempx
    Vy=vtempy if (random.randint(1,2)==1) else -vtempy
    
    myPresentX=node.x
    myPresentY=node.y
    
    myPresentX+=2
    myPresentY+=2
    
    node.x=myPresentX
    node.y=myPresentY
    node.Vx=Vx
    node.Vy=Vy
    
    boolY=(myPresentY>=0 and myPresentY<=ROWS)
    boolX=(myPresentX>=0 and myPresentX<=COLUMNS)
   
    
    while numOfIterations>0 and not turnoff:
        numOfIterations-=1
        myTempX=myPresentX
        myTempX+=Vx
        myTempY=myPresentY
        myTempY+=Vy
        
        minx=node.boundaries[0][0]
        maxx=node.boundaries[0][1]
        miny=node.boundaries[1][0]
        maxy=node.boundaries[1][1]
        ed=[(maxx+minx)//2 ,(maxy+miny)//2]
        #print(node.boundaries)
        bTempX= (myTempX>=0 and myTempX<=COLUMNS)
        bTempY= (myTempY>=0 and myTempY<=ROWS)
        
        
        if not bTempX:
            if myTempX<=0:
                myTempX=2
            else:
                myTempX=COLUMNS+2-boxsize
            
            Vx=-(Vx//abs(Vx))*random.randint(minspeed,maxspeed)*boxsize
            Vy=((Vy//abs(Vy)))*random.randint(minspeed,maxspeed)*boxsize
            
           
        if not bTempY:
            if myTempY<=0:
                myTempY=2
            else:
                myTempY=ROWS+2-boxsize
            
            Vx=(Vx//abs(Vx))*random.randint(minspeed,maxspeed)*boxsize
            Vy=-((Vy//abs(Vy)))*random.randint(minspeed,maxspeed)*boxsize
        
        bTempX= (myTempX>=minx and myTempX<=maxx)
        bTempY= (myTempY>=miny and myTempY<=maxy)
        dis=pow(pow(ed[0]-myPresentX,2)+pow(ed[1]-myPresentY,2),0.5)
        #print(dis)
        if ( not bTempX ) or (not bTempY):
            # b1=node.edgeThread.boundaries
            node.myThread.syncNodeWithEdge(node.edgeThread.returnMyEdge(node.myThread,[myTempX,myTempY]))
            b2=node.edgeThread.boundaries
            minx=node.boundaries[0][0]
            maxx=node.boundaries[0][1]
            miny=node.boundaries[1][0]
            maxy=node.boundaries[1][1]
            ed2=[(maxx+minx)//2 ,(maxy+miny)//2]
        
            c1=pow(pow(ed2[0]-ed[0],2)+pow(ed2[1]-ed[1],2),0.5)
            dis2=pow(pow(ed2[0]-myPresentX,2)+pow(ed2[1]-myPresentY,2),0.5)
            w=(node.myThread.logOutCost*c1+dis2+dis)
            node.cost+=w
            node.edgeThread.cost+=w
        else:
            w=2*dis
            node.cost+=w
            node.edgeThread.cost+=w
        myPresentX=myTempX
        myPresentY=myTempY
        node.x=myPresentX
        node.y=myPresentY
        node.Vx=Vx
        node.Vy=Vy
        # sleep(0.3)
    

if __name__=="__main__":
    pass