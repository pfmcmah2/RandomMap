import matplotlib.pyplot as plt
from matplotlib import colors
import numpy as np
import math
import random
import queue

# creates an NxN map filled with 1's -1's and 0's
# for the sake of variable names 1 voters will be called A's and -1 voters B's

#TODO:  Next steps, multiple voters in one element, keep track of number of voters
#       as well as vote balance

N = 200
# pA + pB <= 1
# probability of empty space = 1 - pA - pB
# percent of "1" voters = pA/(pA + pB)
pA = .4     # probability of a 1
pB = .4     # probability of a -1
c = 100      # presence of clusters
s = 20      # size of clusters
map = []



def RandomShuffleCluster(N, pA, pB, c):
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
                    numA -= 1
                    # recurse
                    rand = random.uniform(0, 1)
                    if(rand < PA and y < N-1):
                        if(Map[y+1][x] == 0):
                            q.put([x, y+1])

                    rand = random.uniform(0, 1)
                    if(rand < PA and y > 0):
                        if(Map[y-1][x] == 0):
                            q.put([x, y-1])

                    rand = random.uniform(0, 1)
                    if(rand < PA and x < N-1):
                        if(Map[y][x+1] == 0):
                            q.put([x+1, y])

                    rand = random.uniform(0, 1)
                    if(rand < PA and x > 0):
                        if(Map[y][x-1] == 0):
                            q.put([x-1, y])

    q = queue.Queue() # clear q
    # fill in -1's
    for i in range(j, N*N, 1):
        if(numB <= 0):
            break;
        x = idx[i][0]
        y = idx[i][1]
        if(numB > 0 and Map[y][x] == 0):
            q.put([x, y])
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
                    numB -= 1
                    # recurse
                    rand = random.uniform(0, 1)
                    if(rand < PB and y < N-1):
                        if(Map[y+1][x] == 0):
                            q.put([x, y+1])

                    rand = random.uniform(0, 1)
                    if(rand < PB and y > 0):
                        if(Map[y-1][x] == 0):
                            q.put([x, y-1])

                    rand = random.uniform(0, 1)
                    if(rand < PB and x < N-1):
                        if(Map[y][x+1] == 0):
                            q.put([x+1, y])

                    rand = random.uniform(0, 1)
                    if(rand < PB and x > 0):
                        if(Map[y][x-1] == 0):
                            q.put([x-1, y])

    return Map


# using P(s) = p*e^(-clusterSize/s) to cotrol cluster size higher s -> larger clusters
# as s -> infinity, P(s) -> p, behavior -> RandomShuffleCluster
def RandomShuffleControlledCluster(N, pA, pB, c, s):
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

    return Map

#map = RandomShuffleCluster(N, pA, pB, c)
#map = RandomShuffleControlledCluster(N, pA, pB, c, s)

'''x = np.arange(0, N, 1)
y = np.arange(0, N, 1)
x, y = np.meshgrid(x, y)
cMap = colors.ListedColormap(['blue', 'white', 'red'])

plt.pcolormesh(x, y, map, cmap = cMap)
plt.colorbar()
plt.show()'''
