import threading
from clientDupe import main
from time import sleep

def important():
    for boxsize in [ 5, 10, 20, 25, 50]:   
        for numberOfParticals in range(0,200,10):
            print("boxsize: "+str(boxsize)+" np: "+str(numberOfParticals))
            main(boxsize,numberOfParticals)
        
if __name__ == '__main__':
    important()
    