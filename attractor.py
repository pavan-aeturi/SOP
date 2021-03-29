import random
def getAttractorArea(n,count):
    if n*n<=count:
        return [[ True for i in range(n)] for j in range(n)]
    grid=[[ False for i in range(n)] for j in range(n)]
    x=random.randint(0, n-1)
    y=random.randint(0,n-1)
    l=[[x,y]]
    arr=[]
    for i in [1,-1,0]:
        for j in [1,-1,0]:
            if not (i==0 and j==0):
                arr.append([i,j])
    while len(l) and count>0:
        point=l.pop(0)
        grid[point[0]][point[1]]=True
        count-=1
        for [dx,dy] in arr:
            if point[0]+dx>=0 and point[1]+dy>=0 and point[0]+dx<n and point[1]+dy<n and not grid[point[0]+dx][point[1]+dy]:
                l.append([point[0]+dx,point[1]+dy])
        random.shuffle(l)
    return grid

def getOnlyAttractor(n,grid):
    attractor=[]
    for i in range(n):
        for j in range(n):
            if grid[i][j]:
                attractor.append([i,j])
    return attractor

if __name__ == '__main__':
    print(getAttractorArea(5,10))
        
        
                    
        
    
    