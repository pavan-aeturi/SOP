import random
import math
from time import sleep
NODE   =[145,9,30]
WHITE  =[255,255,255]

ROWS   =500
COLUMNS=500


class node():
    def __init__(self,x=2,y=2,Vx=1,Vy=1): 
        self.Vx=Vx
        self.Vy=Vy
        self.x=x
        self.y=y
        
    def setVx(self,Vx):
        self.Vx=Vx
    def setVy(self,Vy):
        self.Vy=Vy
    def setx(self,x):
        self.x=x
    def sety(self,y):
        self.y=y
        
def main(boxsize,numberOfParticals):
        
   
    iterations=100
    
    gridL=500//boxsize
    count=[[0 for i in range(gridL)] for j in range(gridL)]
    particle=[None for i in range(numberOfParticals)]
    
    for i in range(numberOfParticals):
         
        vtempx=random.randint(1,4)*boxsize
        vtempy=random.randint(1,4)*boxsize
        Vx=vtempx if (random.randint(1,2)==1) else -vtempx
        Vy=vtempy if (random.randint(1,2)==1) else -vtempy
        
        myPresentX=(random.randint(0,COLUMNS))//boxsize*boxsize 
        myPresentY=(random.randint(0,ROWS))//boxsize*boxsize 
        
        myPresentX+=2
        myPresentY+=2
        
        particle[i]=node(myPresentX,myPresentY,Vx,Vy)
        
        
    for i in range(iterations):    
        for i in range(numberOfParticals):    

            Vx=particle[i].Vx
            Vy=particle[i].Vy
            myPresentX=particle[i].x
            myPresentY=particle[i].y
            
            boolY=(myPresentY>=0 and myPresentY<=ROWS)
            boolX=(myPresentX>=0 and myPresentX<=COLUMNS)
                
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
                
                Vx=-(Vx//abs(Vx))*random.randint(1,4)*boxsize
                Vy=((Vy//abs(Vy)))*random.randint(1,4)*boxsize
                
                
            if not bTempY:
                if myTempY<=0:
                    myTempY=2
                else:
                    myTempY=ROWS+2-boxsize
                
                Vx=(Vx//abs(Vx))*random.randint(1,4)*boxsize
                Vy=-((Vy//abs(Vy)))*random.randint(1,4)*boxsize
            
            myPresentX=myTempX
            myPresentY=myTempY
            
            count[myPresentX//boxsize][myPresentY//boxsize]+=1
            
            particle[i].Vx=Vx
            particle[i].Vy=Vy
            particle[i].x=myPresentX
            particle[i].y=myPresentY
    probabilities=[0 for i in range(10)]
    for i in range(gridL):
        for j in range(gridL):
            pb=(count[i][j]/iterations)
            probabilities[min(int(pb*10),9)]+=1
    
    print("total:"+str(gridL*gridL))
    for i in range(10):
        if i!=9:
            print("0."+str(i)+" to 0."+str(i+1)+" = "+str(probabilities[i]))
        else:
            print("0."+str(i)+" to 1 = "+str(probabilities[i]))

if __name__=="__main__":
    main(20,400)