import random
from math import floor 
from time import sleep

maxspeed=50
minspeed=25
minInAttractor=1
maxInAttractor=1
Logincost=8.5

def main(ROWS,COLUMNS,iterations,node,turnoff,attractor=None):
    cost=0
    boxsize=node.boxsize
    mins=minspeed
    maxs=maxspeed
    K=False
    p=[floor(node.x/boxsize),floor(node.y/boxsize)]
    if p in attractor:
        mins=minInAttractor
        maxs=maxInAttractor

    vtempx=random.randint(mins,maxs)
    vtempy=random.randint(mins,maxs)
        
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
    isInAttractor=False
    while iterations>0 and not turnoff:
        
        p=[floor(node.x/boxsize),floor(node.y/boxsize)]
       
        if p in attractor:
            # print(p)
            
            mins=minInAttractor
            maxs=maxInAttractor
            Vx=(Vx//abs(Vx))*random.randint(mins,maxs)
            Vy=((Vy//abs(Vy)))*random.randint(mins,maxs)
            # print(Vx,Vy)
        else:
            mins=minspeed
            maxs=maxspeed
            Vx=(Vx//abs(Vx))*random.randint(mins,maxs)
            Vy=(Vy//abs(Vy))*random.randint(mins,maxs)


        
        myTempX=myPresentX+Vx
        myTempY=myPresentY+Vy
        minx=node.boundaries[0][0]
        maxx=node.boundaries[0][1]
        miny=node.boundaries[1][0]
        maxy=node.boundaries[1][1]
        ed=[(maxx+minx)//2 ,(maxy+miny)//2]
        bTempX= (myTempX>=0 and myTempX<=COLUMNS)
        bTempY= (myTempY>=0 and myTempY<=ROWS)
      
        if not bTempX:
            if myTempX<=0:
                myTempX=2
            else:
                myTempX=COLUMNS+2-boxsize
            Vx=-(Vx//abs(Vx))*random.randint(mins,maxs)
            Vy=((Vy//abs(Vy)))*random.randint(mins,maxs)
            
            
        if not bTempY:
            if myTempY<=0:
                myTempY=2
            else:
                myTempY=ROWS+2-boxsize
            Vx=(Vx//abs(Vx))*random.randint(mins,maxs)
            Vy=-((Vy//abs(Vy)))*random.randint(mins,maxs)
        
        bTempX= (myTempX>=minx and myTempX<=maxx)
        bTempY= (myTempY>=miny and myTempY<=maxy)
        
        dis=pow(pow(ed[0]-myPresentX,2)+pow(ed[1]-myPresentY,2),0.5)
        
        if ( not bTempX ) or (not bTempY):
            node.edgeThread.pingEdges+=1
            e,p=node.edgeThread.returnMyEdge(node.myThread,[myTempX,myTempY])
            node.myThread.syncNodeWithEdge(e,p)
            ed2=[(maxx+minx)//2 ,(maxy+miny)//2]
            c1=pow(pow(ed2[0]-ed[0],2)+pow(ed2[1]-ed[1],2),0.5)
            dis2=pow(pow(ed2[0]-myPresentX,2)+pow(ed2[1]-myPresentY,2),0.5)
            w=(Logincost*c1+dis2+dis)
            node.cost+=w
            node.edgeThread.increaseCost(w)
        else:
            w=2*dis
            node.cost+=w
            node.edgeThread.increaseCost(w)
            node.edgeThread.pingEdges+=1
        
        myPresentX=myTempX
        myPresentY=myTempY
        node.x=myPresentX
        node.y=myPresentY
        # print(node.x,node.y)
        node.Vx=Vx
        node.Vy=Vy
        iterations-=1
        sleep(0.3)

if __name__=="__main__":
    pass