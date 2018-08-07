import matplotlib.pyplot as plt
from matplotlib import colors
import numpy as np
import math
import random
import queue
import openMap as oM


# Fills an NxN map in with G equal size groups
# Picks G start locations from map at random
# Performs G queue based floodfills simultanously
# Should produce simiplar shaped groups - not truly random
# For a map with empty spaces, could be more random
# Not truly random but fair in terms of voting

# TODO: if a group is densly populated slow it's spread, similar to the
# original clustering methods have number of points expanded to be a function of
# current population of the groups, i.e. above average population -> smaller expansion
# with min 1, randomly shuffle the four directions and take the first n

# NOTE: 2:1 advantage in voters usually leads to all groups belonging to majority party
# unless very high cluster size in which case ~1 group goes to minority
# clusteing irl might be higher than I had thought
# creating good test maps is likely a more difficult task than creating fair groups


N = 200
G = 20
groupSize = []
queues = []
numSquares = N*N


# create map of voters
voteMap = oM.RandomShuffleControlledCluster(N, .4, .2, 1000, 200)


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
        x = random.randint(0, N-1)
        y = random.randint(0, N-1)
        repeat = False
        for j in range(i):
            if(x == startLocation[j][0] and y == startLocation[j][1]):
                repeat = True
    startLocation.append([x, y])
    queues[i].put([x, y])

### PURE RANDOM FLOODFILL
# goes until all queues have been emptied, does not guarentee equal sized groups
'''map = [[-1 for x in range(N)] for y in range(N)]
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
'''

### BALANCED RANDOM FLOODFILL
# goes until all queues have been emptied
# expands to 1 to 3 points depending on relative size of group
map = [[-1 for x in range(N)] for y in range(N)]
done = [0 for x in range(G)] # when queue is emptied mark as done
numDone = 0 # number of goups that are finished being filled
i = 0    # current group
newVoters = 0   # number of new voters in each round of expansion
totalVoters = G # total number of voters, updated after each round
# check if start point is populated, if not fix values
for i in range(G):
    if(voteMap[startLocation[i][1]][startLocation[i][0]] == 0):
        totalVoters -= 1
        groupSize[i] = 0

while(numDone < G):
    if(i == 0):
        # compare size of each group to total voters at beginning of the round
        # Otherwise this would give an advantage to higher index groups
        totalVoters += newVoters
        newVoters = 0

    if(queues[i].empty()):
        if(done[i] == 0):
            done[i] = 1
            numDone += 1
    else:
        point = queues[i].get()
        x = point[0]
        y = point[1]

        # choose how many elements to expand to and which directions
        if(groupSize[i] < totalVoters/G):
            expandSize = 4
        if(groupSize[i] == totalVoters/G):
            expandSize = 3
        if(groupSize[i] > totalVoters/G):
            expandSize = 2

        direction = []  # which direction to expand to
        if(y < N-1):
            if(map[y+1][x] == -1):
                direction.append(0) # 0 = up
        if(y > 0):
            if(map[y-1][x] == -1):
                direction.append(1) # 1 = down
        if(x < N-1):
            if(map[y][x+1] == -1):
                direction.append(2) # 2 = right
        if(x > 0):
            if(map[y][x-1] == -1):
                direction.append(3) # 3 = left

         # cut direction down to correct size
         # direction can be smaller than intended, this is ok
        while(len(direction) > expandSize):
            # select a random element of direction to remove
            rand = random.randint(0, len(direction) - 1)
            del direction[rand]

        # fill in surrounding elements
        # filling in elements when added to queue, rather than when
        if(0 in direction):
            if(map[y+1][x] == -1):
                map[y+1][x] = i
                queues[i].put([x, y+1])
                if(voteMap[y+1][x] != 0): # if point on map is populted inc count
                    groupSize[i] += 1
                    newVoters += 1

        if(1 in direction):
            if(map[y-1][x] == -1):
                map[y-1][x] = i
                queues[i].put([x, y-1])
                if(voteMap[y-1][x] != 0):
                    groupSize[i] += 1
                    newVoters += 1

        if(2 in direction):
            if(map[y][x+1] == -1):
                map[y][x+1] = i
                queues[i].put([x+1, y])
                if(voteMap[y][x+1] != 0):
                    groupSize[i] += 1
                    newVoters += 1

        if(3 in direction):
            if(map[y][x-1] == -1):
                map[y][x-1] = i
                queues[i].put([x-1, y])
                if(voteMap[y][x-1] != 0):
                    groupSize[i] += 1
                    newVoters += 1

    # increment group number
    i = (i + 1)%G


# count votes
voteCount = [0 for x in range(G)]
groupPopulation = [0 for x in range(G)]
for y in range(N):
    for x in range(N):
        idx = map[y][x] # get group index
        voteCount[idx] += voteMap[y][x] # add vote
        if(voteMap[y][x] != 0): # if point on map is populated
            groupPopulation[idx] += 1

# count groups won
a = 0
b = 0
for i in range(G):
    if(voteCount[i] > 0):
        a += 1
    if(voteCount[i] < 0):
        b += 1

print('groupSize = ', groupSize)
print('groupPopulation = ', groupPopulation)
print('voteCount = ', voteCount)
print('Red wins: ', b, '\nBlue wins: ', a)

x = np.arange(0, N, 1)
y = np.arange(0, N, 1)
x, y = np.meshgrid(x, y)
cMap = colors.ListedColormap(['red', 'white', 'blue'])

plt.pcolormesh(x, y, voteMap, cmap = cMap)
plt.colorbar()
plt.show()

plt.pcolormesh(x, y, map)#, cmap = cMap)
plt.colorbar()
plt.show()
