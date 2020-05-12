import API
import sys

def log(string):
    sys.stderr.write("{}\n".format(string))
    sys.stderr.flush()

#functions to move robot, returns direction
def goUp(direction):
    if direction == 0:
        API. moveForward()
    if direction == 1:
        API.turnLeft()
        API.moveForward()
    if direction == 2:
        API.turnLeft()
        API.turnLeft()
        API.moveForward()
    if direction == 3:
        API.turnRight()
        API.moveForward()
    return 0

def goRight(direction):
    if direction == 0:
        API.turnRight()
        API. moveForward()
    if direction == 1:
        API.moveForward()
    if direction == 2:
        API.turnLeft()
        API.moveForward()
    if direction == 3:
        API.turnRight()
        API.turnRight()
        API.moveForward()
    return 1

def goDown(direction):
    if direction == 0:
        API.turnRight()
        API.turnRight()
        API. moveForward()
    if direction == 1:
        API.turnRight()
        API.moveForward()
    if direction == 2:
        API.moveForward()
    if direction == 3:
        API.turnLeft()
        API.moveForward()
    return 2

def goLeft(direction):
    if direction == 0:
        API.turnLeft()
        API. moveForward()
    if direction == 1:
        API.turnLeft()
        API.turnLeft()
        API.moveForward()
    if direction == 2:
        API.turnRight()
        API.moveForward()
    if direction == 3:
        API.moveForward()
    return 3

#check if specific cell is in previous cells visited
def searchArr(cell, arr):
    inArr = False
    count = 0
    for x in arr:
        if cell == x:
            inArr = True
            count = count + 1
    return inArr, count
            

#calculate Manhattan Distance, src = current node, dst = goal
def MD(src, dst, wall, arr):
    x = abs(src[0] - dst[0])
    y = abs(src[1] - dst[1])
    z = 0 #used to decrease priority of cells blocked by wall
    a = 0 #used to mark previously explored cells
    inArr = False
    mult = 0

    if wall:
        z = 50

    inArr, mult = searchArr(src, arr)
    
    if inArr:
        a = mult * 15
    return x+y+z+a

#find next optimal move, returns tuple (returnNode, returnDirection)
def nextTurn(current, goal, direction, prevCells):
    #initialize surrounding cells to 0
    cur_left = (0,0)
    cur_forward = (0,0)
    cur_right = (0,0)
    cur_back = (0,0)
    retNode = (0,0)
    retDir = 0

    #initialize variables to store manhattan distances of surrounding cells
    mdl = 0
    mdf = 0
    mdr = 0

    #if looking up
    if direction == 0:
        cur_left = (current[0]-1, current[1])
        cur_forward = (current[0], current[1]+1)
        cur_right = (current[0]+1, current[1])
        cur_back = (current[0], current[1]-1)

        #calculate MD for surrounding cells
        mdl = MD(cur_left, goal, API.wallLeft(), prevCells)
        mdf = MD(cur_forward, goal, API.wallFront(), prevCells)
        mdr = MD(cur_right, goal, API.wallRight(), prevCells)

        if ((not API.wallLeft()) and mdl <= mdf and mdl <= mdr):
            retDir = goLeft(direction)
            retNode = cur_left
        elif ((not API.wallFront()) and mdf <= mdl and mdf <= mdr):
            retDir = goUp(direction)
            retNode = cur_forward
        elif ((not API.wallRight()) and mdr <= mdl and mdr <= mdf):
            retDir = goRight(direction)
            retNode = cur_right
        else:
            retDir = goDown(direction)
            retNode = cur_back

    #if looking right
    if direction == 1:
        cur_left = (current[0], current[1]+1)
        cur_forward = (current[0]+1, current[1])
        cur_right = (current[0], current[1]-1)
        cur_back = (current[0]-1, current[1])

        #calculate MD for surrounding cells
        mdl = MD(cur_left, goal, API.wallLeft(), prevCells)
        mdf = MD(cur_forward, goal, API.wallFront(), prevCells)
        mdr = MD(cur_right, goal, API.wallRight(), prevCells)

        if ((not API.wallLeft()) and mdl <= mdf and mdl <= mdr):
            retDir = goUp(direction)
            retNode = cur_left
        elif ((not API.wallFront()) and mdf <= mdl and mdf <= mdr):
            retDir = goRight(direction)
            retNode = cur_forward
        elif ((not API.wallRight()) and mdr <= mdl and mdr <= mdf):
            retDir = goDown(direction)
            retNode = cur_right
        else:
            retDir = goLeft(direction)
            retNode = cur_back

    #if looking down
    if direction == 2:
        cur_left = (current[0]+1, current[1])
        cur_forward = (current[0], current[1]-1)
        cur_right = (current[0]-1, current[1])
        cur_back = (current[0], current[1]+1)

        #calculate MD for surrounding cells
        mdl = MD(cur_left, goal, API.wallLeft(), prevCells)
        mdf = MD(cur_forward, goal, API.wallFront(), prevCells)
        mdr = MD(cur_right, goal, API.wallRight(), prevCells)

        if ((not API.wallLeft()) and mdl <= mdf and mdl <= mdr):
            retDir = goRight(direction)
            retNode = cur_left
        elif ((not API.wallFront()) and mdf <= mdl and mdf <= mdr):
            retDir = goDown(direction)
            retNode = cur_forward
        elif ((not API.wallRight()) and mdr <= mdl and mdr <= mdf):
            retDir = goLeft(direction)
            retNode = cur_right
        else:
            retDir = goUp(direction)
            retNode = cur_back

    #if looking left
    if direction == 3:
        cur_left = (current[0], current[1]-1)
        cur_forward = (current[0]-1, current[1])
        cur_right = (current[0], current[1]+1)
        cur_back = (current[0]+1, current[1])

        #calculate MD for surrounding cells
        mdl = MD(cur_left, goal, API.wallLeft(), prevCells)
        mdf = MD(cur_forward, goal, API.wallFront(), prevCells)
        mdr = MD(cur_right, goal, API.wallRight(), prevCells)

        if ((not API.wallLeft()) and mdl <= mdf and mdl <= mdr):
            retDir = goDown(direction)
            retNode = cur_left
        elif ((not API.wallFront()) and mdf <= mdl and mdf <= mdr):
            retDir = goLeft(direction)
            retNode = cur_forward
        elif ((not API.wallRight()) and mdr <= mdl and mdr <= mdf):
            retDir = goUp(direction)
            retNode = cur_right
        else:
            retDir = goRight(direction)
            retNode = cur_back

    return retNode, retDir

def main():
    log("Running...")

    #set color and text of start and end cells
    API.setColor(0, 0, "G")
    API.setColor(7, 7, "R")
    API.setColor(7, 8, "G")
    API.setColor(8, 7, "G")
    API.setColor(8, 8, "G")

    API.setText(0, 0, "start")
    API.setText(7, 7, "end")
    API.setText(7, 8, "end")
    API.setText(8, 7, "end")
    API.setText(8, 8, "end")

    # Up = 0, Right = 1, Down = 2, Left = 3
    dir = 0 # start facing up

    #important coords
    start = (0,0)
    goal = (7,7)
    end2 = (7,8)
    end3 = (8,7)
    end4 = (8,8)

    current = start
    prevCells = [start] #store cells you've been to
    while (current != goal):
        log(dir)
        log("currently at" + str(current))
        prevCells.append(current)
        current, dir = nextTurn(current, goal, dir, prevCells)
 

if __name__ == "__main__":
    main()