import random
from time import sleep
NODE   =[145,9,30]
WHITE  =[255,255,255]



def main(ROWS,COLUMNS,node):
    Vx=20 if (random.randint(1,2)==1) else -10
    Vy=20 if (random.randint(1,2)==1) else -10
    
    myPresentX=(random.randint(0,COLUMNS))//10*10 
    myPresentY=(random.randint(0,ROWS))//10*10 
    
    node.x=myPresentX
    node.y=myPresentY
    node.Vx=Vx
    node.Vy=Vy
    
    boolY=(myPresentY>=0 and myPresentY<=ROWS)
    boolX=(myPresentX>=0 and myPresentX<=COLUMNS)
    
    myPresentX+=2
    myPresentY+=2
    
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
                myTempX=COLUMNS+2
            Vx=-Vx
            
        if not bTempY:
            if myTempY<=0:
                myTempY=2
            else:
                myTempY=ROWS+2
            Vy=-Vy
        
        
        myPresentX=myTempX
        myPresentY=myTempY
        node.x=myPresentX
        node.y=myPresentY
        node.Vx=Vx
        node.Vy=Vy
        sleep(0.3)
        
if __name__=="__main__":
    pass