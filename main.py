import matplotlib.pyplot as plt
from matplotlib import colors
import numpy as np
import math
import random
import queue

N = 200
G = 20
pA = .4
pB = .4
c = 100      # presence of clusters
s = 50      # size of clusters

maxSkip = 5     # number of consecutive times a group can be prevented from
                # expanding during group creation, increasing increases runtime
I = 10          # number of RandomMaps to be generated, increasing increases runtime
                # but also increases chance of an even grouping
MapType = 1     # Select type of voter map to be created

### BUILD RANDOM MAP ###
# Both functions use random shuffle to order start points and perform a
# random floodfill with controlled probability from the start points unitl
# the quota for both voter groups is filled
# stores vote count in Map and population count in PMap

# Maximum one person per index
if(MapType == 0):
    # Up to one person per index
    # ideal function for P = f(p, c)
    # c = 1 -> f = 0
    # as c -> inf f slowly -> 1
    # f(p, c) = 1 - (1-p)^((c-1)/100)) works (10 is arbitrary, the higher the number
    # in the denomiator of the exponent, the slower the increase of f with c)
    # Very open to experimentation on this
    PA = 1 - (1-pA)**((c-1)/10)
    PB = 1 - (1-pB)**((c-1)/10)
    # if this number gets high, map is usually filled in one floodfill
    numA = N*N*pA
    numB = N*N*pB
    q = queue.Queue()
    Map =  [[0 for x in range(N)] for y in range(N)]
    PMap =  [[0 for x in range(N)] for y in range(N)]
    idx = []
    for i in range(N):
        for j in range(N):
            idx.append([j, i])
    # sort idx
    # InsertionShuffle: CS 473 UIUC Lecture 1
    for i in range(N*N):  # could speed this up? only need num1 < N*N
        rand = random.randint(0, i)
        temp = idx[i]
        idx[i] = idx[rand]
        idx[rand] = temp

    # fill in 1's
    for i in range(N*N):
        if(numA <= 0):
            j = i
            break;
        x = idx[i][0]
        y = idx[i][1]
        if(numA > 0 and Map[y][x] == 0):
            q.put([x, y])
            clusterSize = 1 # as cluster size increases, chance of adding to the cluster decreases
            while(not q.empty() and numA > 0):
                point = q.get()                  # get point on map from queue
                x = point[0]
                y = point[1]

                # update count and probability
                # unlike other random map generators, not determining if a
                # 0 or a 1 should be placed, instead determining if floodfill
                # should be continued, in this case flood fill is done for
                # only the 1's with randomly selected starting points, the rest
                # is filled in with 0's
                if(Map[y][x] == 0):
                    Map[y][x] = 1
                    PMap[y][x] = 1
                    numA -= 1
                    P = PA*(2.718**(-1*(clusterSize/s)))

                    rand = random.uniform(0, 1)
                    if(rand < P and y < N-1):
                        if(Map[y+1][x] == 0):
                            q.put([x, y+1])
                            clusterSize += 1

                    rand = random.uniform(0, 1)
                    if(rand < P and y > 0):
                        if(Map[y-1][x] == 0):
                            q.put([x, y-1])
                            clusterSize += 1

                    rand = random.uniform(0, 1)
                    if(rand < P and x < N-1):
                        if(Map[y][x+1] == 0):
                            q.put([x+1, y])
                            clusterSize += 1

                    rand = random.uniform(0, 1)
                    if(rand < P and x > 0):
                        if(Map[y][x-1] == 0):
                            q.put([x-1, y])
                            clusterSize += 1

    q = queue.Queue()
    # fill in -1's
    for i in range(j, N*N, 1):
        if(numB <= 0):
            break;
        x = idx[i][0]
        y = idx[i][1]
        if(numB > 0 and Map[y][x] == 0):
            q.put([x, y])
            clusterSize = 1
            while(not q.empty() and numB > 0):
                point = q.get()                  # get point on map from queue
                x = point[0]
                y = point[1]

                # update count and probability
                # unlike other random map generators, not determining if a
                # 0 or a 1 should be placed, instead determining if floodfill
                # should be continued, in this case flood fill is done for
                # only the 1's with randomly selected starting points, the rest
                # is filled in with 0's
                if(Map[y][x] == 0):
                    Map[y][x] = -1
                    PMap[y][x] = 1
                    numB -= 1
                    P = PA*(2.718**(-1*(clusterSize/s)))
                    # recurse
                    rand = random.uniform(0, 1)
                    if(rand < P and y < N-1):
                        if(Map[y+1][x] == 0):
                            q.put([x, y+1])
                            clusterSize += 1

                    rand = random.uniform(0, 1)
                    if(rand < P and y > 0):
                        if(Map[y-1][x] == 0):
                            q.put([x, y-1])
                            clusterSize += 1

                    rand = random.uniform(0, 1)
                    if(rand < P and x < N-1):
                        if(Map[y][x+1] == 0):
                            q.put([x+1, y])
                            clusterSize += 1

                    rand = random.uniform(0, 1)
                    if(rand < P and x > 0):
                        if(Map[y][x-1] == 0):
                            q.put([x-1, y])
                            clusterSize += 1
# Multiple people per index
if(MapType == 1):
    # ideal function for P = f(p, c)
    # c = 1 -> f = 0
    # as c -> inf f slowly -> 1
    # f(p, c) = 1 - (1-p)^((c-1)/100)) works (10 is arbitrary, the higher the number
    # in the denomiator of the exponent, the slower the increase of f with c)
    # Very open to experimentation on this
    PA = 1 - (1-pA)**((c-1)/10)
    PB = 1 - (1-pB)**((c-1)/10)
    # if this number gets high, map is usually filled in one floodfill
    numA = N*N*pA
    numB = N*N*pB
    q = queue.Queue()
    Map =  [[0 for x in range(N)] for y in range(N)]    # vote balance
    PMap = [[0 for x in range(N)] for y in range(N)]    # population
    idx = []
    for i in range(N):
        for j in range(N):
            idx.append([j, i])
    # sort idx
    # InsertionShuffle: CS 473 UIUC Lecture 1
    for i in range(N*N):  # could speed this up? only need num1 < N*N
        rand = random.randint(0, i)
        temp = idx[i]
        idx[i] = idx[rand]
        idx[rand] = temp

    # fill in 1's
    for i in range(N*N):
        if(numA <= 0):
            j = i
            break;
        x = idx[i][0]
        y = idx[i][1]
        if(numA > 0):
            q.put([x, y])
            clusterSize = 1 # as cluster size increases, chance of adding to the cluster decreases
            while(not q.empty() and numA > 0):
                point = q.get()                  # get point on map from queue
                x = point[0]
                y = point[1]

                # update count and probability
                # unlike other random map generators, not determining if a
                # 0 or a 1 should be placed, instead determining if floodfill
                # should be continued, in this case flood fill is done for
                # only the 1's with randomly selected starting points, the rest
                # is filled in with 0's
                Map[y][x] += 1
                PMap[y][x] += 1
                numA -= 1
                P = PA*(2.718**(-1*(clusterSize/s)))

                rand = random.uniform(0, 1)
                if(rand < P and y < N-1):
                    q.put([x, y+1])
                    clusterSize += 1

                rand = random.uniform(0, 1)
                if(rand < P and y > 0):
                    q.put([x, y-1])
                    clusterSize += 1

                rand = random.uniform(0, 1)
                if(rand < P and x < N-1):
                    q.put([x+1, y])
                    clusterSize += 1

                rand = random.uniform(0, 1)
                if(rand < P and x > 0):
                    q.put([x-1, y])
                    clusterSize += 1

    q = queue.Queue()
    # fill in -1's
    for i in range(j, N*N, 1):
        if(numB <= 0):
            break;
        x = idx[i][0]
        y = idx[i][1]
        if(numB > 0):
            q.put([x, y])
            clusterSize = 1
            while(not q.empty() and numB > 0):
                point = q.get()                  # get point on map from queue
                x = point[0]
                y = point[1]

                # update count and probability
                # unlike other random map generators, not determining if a
                # 0 or a 1 should be placed, instead determining if floodfill
                # should be continued, in this case flood fill is done for
                # only the 1's with randomly selected starting points, the rest
                # is filled in with 0's
                Map[y][x] += -1
                PMap[y][x] += 1
                numB -= 1
                P = PA*(2.718**(-1*(clusterSize/s)))
                # recurse
                rand = random.uniform(0, 1)
                if(rand < P and y < N-1):
                    q.put([x, y+1])
                    clusterSize += 1

                rand = random.uniform(0, 1)
                if(rand < P and y > 0):
                    q.put([x, y-1])
                    clusterSize += 1

                rand = random.uniform(0, 1)
                if(rand < P and x < N-1):
                    q.put([x+1, y])
                    clusterSize += 1

                rand = random.uniform(0, 1)
                if(rand < P and x > 0):
                    q.put([x-1, y])
                    clusterSize += 1


### CREATE GROUPS ###
# creates a set of random groups using simultanous floodfills with random starting
# points, scheduled to keep groups close in population size
def RandomGroup(N, G, maxSkip, popMap):
    # initialize
    # TODO: Test Different maxSkip values increasing maxSkip should decrease stdev of group size
    # Not sure if there is a way to guarentee an upper bound on stdev size
    # maxSkip;  max number of turns than can be skipped for a group
    skip = [0 for i in range(G)]    # number of turns which have been skipped for each
    groupSize = [0 for i in range(G)]
    queues = []
    for i in range(G):
        #val = round(numSquares/(G - i))
        #numSquares -= val
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

    map = [[-1 for x in range(N)] for y in range(N)]
    done = [0 for x in range(G)] # when queue is emptied mark as done
    numDone = 0 # number of goups that are finished being filled
    i = 0    # current group
    newVoters = 0   # number of new voters in each round of expansion
    totalVoters = G # total number of voters, updated after each round
    # check if start point is populated, if not fix values
    for i in range(G):
        totalVoters -= popMap[startLocation[i][1]][startLocation[i][0]]
        groupSize[i] = popMap[startLocation[i][1]][startLocation[i][0]]

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
            expandFlag = True    # is the group allowed to expand this round
            if(groupSize[i] > totalVoters/G):
                skip[i] += 1    # increment skip count
                if(skip[i] == maxSkip): # if max number of skips reach
                    skip[i] = 0 # reset count and allow to expand
                else:
                    expandFlag = False

            if(expandFlag):
                point = queues[i].get()
                x = point[0]
                y = point[1]


                # fill in surrounding elements
                # filling in elements when added to queue, rather than when
                if(y < N - 1):
                    if(map[y+1][x] == -1):
                        map[y+1][x] = i
                        queues[i].put([x, y+1])
                        groupSize[i] += popMap[y+1][x]
                        newVoters += popMap[y+1][x]

                if(y > 0):
                    if(map[y-1][x] == -1):
                        map[y-1][x] = i
                        queues[i].put([x, y-1])
                        groupSize[i] += popMap[y-1][x]
                        newVoters += popMap[y-1][x]

                if(x < N - 1):
                    if(map[y][x+1] == -1):
                        map[y][x+1] = i
                        queues[i].put([x+1, y])
                        groupSize[i] += popMap[y][x+1]
                        newVoters += popMap[y][x+1]

                if(x > 0):
                    if(map[y][x-1] == -1):
                        map[y][x-1] = i
                        queues[i].put([x-1, y])
                        groupSize[i] += popMap[y][x-1]
                        newVoters += popMap[y][x-1]

        # increment group number
        i = (i + 1)%G
    return [map, groupSize]

# create I grouping and choose the one with the most evenly distributed population
STD = N*N
map = []
for i in range(I):
    tempMap = RandomGroup(N, G, maxSkip, PMap)
    print(tempMap[1])
    tempSTD = np.std(tempMap[1])    # take stdev of groupSize
    print(tempSTD)
    if(tempSTD < STD):
        STD = tempSTD
        map = tempMap[0]


### SHOW RESULTS ###

voteCount = [0 for x in range(G)]
groupPopulation = [0 for x in range(G)]
for y in range(N):
    for x in range(N):
        idx = map[y][x] # get group index
        voteCount[idx] += Map[y][x] # add vote
        groupPopulation[idx] += PMap[y][x]

# count groups won
a = 0
b = 0
for i in range(G):
    if(voteCount[i] > 0):
        a += 1
    if(voteCount[i] < 0):
        b += 1

#print('groupSize = ', groupSize)
print('groupPopulation = ', groupPopulation)
print('stdev = ', np.std(groupPopulation))
print('voteCount = ', voteCount)
print('Red wins: ', b, '\nBlue wins: ', a)

x = np.arange(0, N, 1)
y = np.arange(0, N, 1)
x, y = np.meshgrid(x, y)
cMap = colors.ListedColormap(['red', 'white', 'blue'])

# show vote map
if(MapType == 0):
    plt.pcolormesh(x, y, Map, cmap = cMap)
if(MapType == 1):
    plt.pcolormesh(x, y, Map)
plt.colorbar()
plt.show()

# show groups
plt.pcolormesh(x, y, map) #, cmap = cMap)
plt.colorbar()
plt.show()
