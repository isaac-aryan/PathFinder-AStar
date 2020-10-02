#IMPORTED STUFF
import os,math,sys
import pygame
from tkinter import *

#import project modules
try:
    import configs as cfg
except:
    print("1 or more project modules are missing.")


openSet=[]
closedSet=[]
cameFrom=[]

#CREATE 2D ARRAY
grid = [ [0 for i in range(cfg.row)] for i in range(cfg.cols)]



st=input("Enter x and y coordinates for the start point in the following format: x,y\n").split(",")
try:
    st=list(map(int,st))
except Exception as e:
    print(e)

ed=input("Enter x and y coordinates for the end point in the following format: x,y\n").split(",")
try:
    ed=list(map(int,ed))
except Exception as e:
    print(e)
#print("Start point: ",start[0],",",start[1])
#print("End point: ",end[0],",",end[1])



#screen
pygame.init()

screen=pygame.display.set_mode((cfg.scr_width, cfg.scr_height))

class spot:

    
    def __init__(self, x, y):
        self.i = x
        self.j = y
        self.f = 0
        self.g = 0      
        self.h = 0      #h is heuristic 
        self.neighbors = [] #neighbour for every cell
        self.previous = None
        self.obs = False    #Tells whether the spot is an obstacle or not
        self.closed = False
        self.value = 1

    def show(self, color, width):
        if self.closed == False :
            pygame.draw.rect(screen, color, (self.i * cfg.w, self.j * cfg.h, cfg.w, cfg.h), width)
            pygame.display.update()

    def path(self, color, width):
        pygame.draw.rect(screen, color, (self.i * cfg.w, self.j * cfg.h, cfg.w, cfg.h), width)
        pygame.display.update()

    def addNeighbors(self, grid):
        i = self.i
        j = self.j
        if i < cfg.cols-1 and grid[self.i + 1][j].obs == False:
            self.neighbors.append(grid[self.i + 1][j])
        if i > 0 and grid[self.i - 1][j].obs == False:
            self.neighbors.append(grid[self.i - 1][j])
        if j < cfg.row-1 and grid[self.i][j + 1].obs == False:
            self.neighbors.append(grid[self.i][j + 1])
        if j > 0 and grid[self.i][j - 1].obs == False:
            self.neighbors.append(grid[self.i][j - 1])

# Create Spots
for i in range(cfg.cols):
    for j in range(cfg.row):
        grid[i][j] = spot(i, j)

def heurisitic(n, e):
    d = math.sqrt((n.i - e.i)**2 + (n.j - e.j)**2)
    #d = abs(n.i - e.i) + abs(n.j - e.j)
    return d


# SHOW RECT

for i in range(cfg.cols):
    for j in range(cfg.row):
        grid[i][j].show((255, 255, 255), 1)

for i in range(0,cfg.row):
    grid[0][i].show(cfg.grey, 0)
    grid[0][i].obs = True
    grid[cfg.cols-1][i].obs = True
    grid[cfg.cols-1][i].show(cfg.grey, 0)
    grid[i][cfg.row-1].show(cfg.grey, 0)
    grid[i][0].show(cfg.grey, 0)
    grid[i][0].obs = True
    grid[i][cfg.row-1].obs = True

def mousePress(x):
    global grid
    t = x[0]
    w = x[1]
    g1 = t // (800 // cfg.cols)
    g2 = w // (800 // cfg.row)
    #acess = grid[g1][g2]
    if grid[g1][g2] != start and grid[g1][g2] != end:
        if grid[g1][g2].obs == False:
            grid[g1][g2].obs = True
            grid[g1][g2].show((255, 255, 255), 0)

end=grid[ed[0]][ed[1]]
start=grid[st[0]][st[1]]
openSet.append(start)

flg=False

#MAIN FUNCTION
def main():
    global openSet,closedSet,cameFrom
    global flg


    end.show((255, 8, 127), 0)
    start.show((255, 8, 127), 0)
  
    if len(openSet) > 0:
    
        lowestIndex = 0
        for i in range(len(openSet)):
            if openSet[i].f < openSet[lowestIndex].f:
                lowestIndex = i

        current = openSet[lowestIndex]
        if current == end:
            print('done', current.f)
            start.show((255,8,127),0)
            temp = current.f
            for i in range(round(current.f)):
                current.closed = False
                current.show((0,0,255), 0)
                current = current.previous
            end.show((255, 8, 127), 0)
            flg=True

        openSet.pop(lowestIndex)
        closedSet.append(current)

        neighbors = current.neighbors
        for i in range(len(neighbors)):
            neighbor = neighbors[i]
            if neighbor not in closedSet:
                tempG = current.g + current.value
                if neighbor in openSet:
                    if neighbor.g > tempG:
                        neighbor.g = tempG
                else:
                    neighbor.g = tempG
                    openSet.append(neighbor)

            neighbor.h = heurisitic(neighbor, end)
            neighbor.f = neighbor.g + neighbor.h

            if neighbor.previous == None:
                neighbor.previous = current
    current.closed = True
    for i in range(len(openSet)):
        openSet[i].show(cfg.green, 0)

    for i in range(len(closedSet)):
        if closedSet[i] != start:
            closedSet[i].show(cfg.red,0)
            
            

#POST CREATING THE GRID
end.show((255, 8, 127), 0)
start.show((255, 8, 127), 0)


#DRAW OBSTACLE LOOP
loop=True
while loop:
    ev=pygame.event.get()

    for event in ev:
        if event.type==pygame.QUIT:
            pygame.quit()

        if pygame.mouse.get_pressed()[0]:
            try:
                pos = pygame.mouse.get_pos()
                mousePress(pos)
            except AttributeError:
                pass
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                loop=False
                break

for i in range(cfg.cols):
    for j in range(cfg.row):
        grid[i][j].addNeighbors(grid)

#MAIN LOOP
while True:
    ev = pygame.event.poll()
    if ev.type == pygame.QUIT:
        pygame.quit()
    pygame.display.update()

    if flg==False:
        main()
print("End of process")