import random
import math
from time import sleep
NODE   =[145,9,30]
WHITE  =[255,255,255]




maxspeed=4
minspeed=1

def main(ROWS,COLUMNS,node):
    boxsize=node.boxsize
    vtempx=random.randint(minspeed,maxspeed)*boxsize
    vtempy=random.randint(minspeed,maxspeed)*boxsize
    Vx=vtempx if (random.randint(1,2)==1) else -vtempx
    Vy=vtempy if (random.randint(1,2)==1) else -vtempy
    
    myPresentX=(random.randint(0,COLUMNS))//boxsize*boxsize 
    myPresentY=(random.randint(0,ROWS))//boxsize*boxsize 
    
    myPresentX+=2
    myPresentY+=2
    
    node.x=myPresentX
    node.y=myPresentY
    node.Vx=Vx
    node.Vy=Vy
    
    boolY=(myPresentY>=0 and myPresentY<=ROWS)
    boolX=(myPresentX>=0 and myPresentX<=COLUMNS)
    
   
    
    while boolX and boolY:
        
        myTempX=myPresentX
        myTempX+=Vx
        myTempY=myPresentY
        myTempY+=Vy
        
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
        
        
        myPresentX=myTempX
        myPresentY=myTempY
        node.x=myPresentX
        node.y=myPresentY
        node.Vx=Vx
        node.Vy=Vy
        sleep(0.3)
        
if __name__=="__main__":
    pass