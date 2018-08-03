import matplotlib.pyplot as plt
from matplotlib import colors
import numpy as np
import math
import random
import queue


# Fills an NxN map in with G equal size groups
# Picks G start locations from map at random
# Performs G queue based floodfills simultanously
# Should produce simiplar shaped groups - not truly random
# For a map with empty spaces, could be more random
# Not truly random but fair in terms of voting


N = 100
G = 5
groupSize = []
queues = []
numSquares = N*N

# initialize
for i in range(G):
    #val = round(numSquares/(G - i))
    #numSquares -= val
    groupSize.append(1) # each group is initialized with one point on the map
    q = queue.Queue()
    queues.append(q)


# assign starting location for each group
startLocation = []      # used to check repeat start locations
for i in range(G):
    repeat = True       # detect repeated start points
    # expected number of tries = SUM(i = 0 to G - 1) (N^2 - 1)/N^2 ~ G for N >> G
    # expected running time = SUM(i = 0 to G - 1) (i + 1)(N^2 - 1)/N^2 ~ G^2 for N >> G
    while(repeat):
        x = random.randint(0, N)
        y = random.randint(0, N)
        repeat = False
        for j in range(i):
            if(x == startLocation[j][0] and y == startLocation[j][1]):
                repeat = True
    startLocation.append([x, y])
    queues[i].put([x, y])




# goes until all queues have been emptied, does not guarentee equal sized groups
map = [[-1 for x in range(N)] for y in range(N)]
done = [0 for x in range(G)] # when queue is emptied mark as done
numDone = 0 # number of goups that are finished being filled
i = 0    # current group
while(numDone < G):
    if(queues[i].empty()):
        if(done[i] == 0):
            done[i] = 1
            numDone += 1
    else:
        point = queues[i].get()
        x = point[0]
        y = point[1]

        # fill in surrounding elements
        # filling in elements when added to queue, rather than when
        if(y < N-1):
            if(map[y+1][x] == -1):
                map[y+1][x] = i
                queues[i].put([x, y+1])
                groupSize[i] += 1

        if(y > 0):
            if(map[y-1][x] == -1):
                map[y-1][x] = i
                queues[i].put([x, y-1])
                groupSize[i] += 1

        if(x < N-1):
            if(map[y][x+1] == -1):
                map[y][x+1] = i
                queues[i].put([x+1, y])
                groupSize[i] += 1

        if(x > 0):
            if(map[y][x-1] == -1):
                map[y][x-1] = i
                queues[i].put([x-1, y])
                groupSize[i] += 1

    # increment group number
    i = (i + 1)%G

print(groupSize)

x = np.arange(0, N, 1)
y = np.arange(0, N, 1)
x, y = np.meshgrid(x, y)
cMap = colors.ListedColormap(['red', 'orange', 'yellow', 'green', 'blue'])

plt.pcolormesh(x, y, map, cmap = cMap)
plt.colorbar()
plt.show()
