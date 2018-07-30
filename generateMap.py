import matplotlib.pyplot as plt
from matplotlib import colors
import numpy as np
import math
import scipy.stats
import random
import queue

# creates an NxN array of 1's and 0's with an expected percent of p 1's

# another method is to pick array indexes at random and place 1's until quota is filled
# the the rest with 0's
# However this might be harder to scale to having clustering of numbers
N = 200
p = .6
c = 8 # cluster
map = []

# standard random map
def RandomPure():
    global map
    map = []
    num0 = 0
    num1 = 0
    for i in range(N):
        row = []
        for j in range(N):
            rand = random.uniform(0, 1) # generate random number
            if(rand < p):
                row.append(1)
                num1 += 1
            else:
                row.append(0)
                num0 += 1
        map.append(row)
    print(num0)
    print(num1)



# loops through the map row by row starting in the top left corner
# at each index assigns a 0 or 1 determined by a bernoilli random variable
# with probability dependent on number of 0's and 1's needed to fill the quota
# ensures the quota is filled exactly
def RandomIterative():
    global map
    map = []
    num0 = N*N*(1-p)    # quota of 0's
    num1 = N*N*p       # quota of 1's
    for i in range(N):
        row = []
        for j in range(N):
            # Fill in an element with a 1 or 0 determined by a bernoilli random variable
            # Probabily is based on past values which have been filled in
            P = num1/(num0 + num1)  # local probability
            #print(P)
            rand = random.uniform(0, 1) # generate random number
            if(rand < P):
                row.append(1)
                num1 -= 1
                #print(1)
            else:
                row.append(0)
                num0 -= 1
                #print(0)
        map.append(row)



# ensures quota is filled exactly
# clustering can be controlled;
# c = 1 -> same as RandomIterative, increaseing c -> more clustering
def ClusterIterative():
    # same as generateRandomMap but prioritizes same as neighbors
    # not truly random, tends to have minority cluster around top left
    # this is because
    global map
    map = []
    num0 = N*N*(1-p)    # quota of 0's
    num1 = N*N*p       # quota of 1's
    for i in range(N):
        row = []
        prev = -1
        for j in range(N):
            # Fill in an element with a 1 or 0 determined by a bernoilli random variable
            # Probabily is based on past values which have been filled in
            P = num1/(num0 + num1)  # local probability

            # probaility weight based on an exponential function f(p,c) = p^1/c
            # higher c -> higher f
            # f(0, c) = 0,  f(1, c) = 1  This condition must hold for any f
            if(i == 0):
                if(prev == 1):
                    P = P**(1/c)
                if(prev == 0):
                    P = 1 - (1-P)**(1/c)
            # lots of boundary conditions
            else:
                if(j == 0):
                    if(map[i-1][j] == 1):
                        P = P**(1/c)
                    if(map[i-1][j] == 0):
                        P = 1 - (1-P)**(1/c)
                else:
                    if(map[i-1][j] == 1 and prev == 1):
                        P = P**(1/c)
                    if(map[i-1][j] == 0 and prev == 0):
                        P = 1 - (1-P)**(1/c)

            #print(P)
            rand = random.uniform(0, 1) # generate random number
            if(rand < P):
                row.append(1)
                num1 -= 1
                prev = 1
            else:
                row.append(0)
                num0 -= 1
                prev = 0
        map.append(row)
    print(num0)
    print(num1)



# clustering can be controlled;
# c = 1 -> same as RandomPure, increaseing c -> more clustering
# as c increases variance of ratio of 0's to 1's increses
# at very high c this becomes a big problem
def ClusterPure():
    global map
    map = []
    num0 = 0
    num1 = 0
    P = p
    for i in range(N):
        row = []
        prev = -1
        for j in range(N):
            # probaility weight based on an exponential function f(p,c) = p^1/c
            # higher c -> higher f
            # f(0, c) = 0,  f(1, c) = 1  This condition must hold for any f
            if(i == 0):
                if(prev == 1):
                    P = p**(1/c)
                if(prev == 0):
                    P = 1 - (1-p)**(1/c)
            # lots of boundary conditions
            else:
                if(j == 0):
                    if(map[i-1][j] == 1):
                        P = p**(1/c)
                    if(map[i-1][j] == 0):
                        P = 1 - (1-p)**(1/c)
                else:
                    if(map[i-1][j] == 1 and prev == 1):
                        P = p**(1/c)
                    if(map[i-1][j] == 0 and prev == 0):
                        P = 1 - (1-p)**(1/c)

            #print(P)
            rand = random.uniform(0, 1) # generate random number
            if(rand < P):
                row.append(1)
                num1 += 1
                prev = 1
            else:
                row.append(0)
                num0 += 1
                prev = 0
        map.append(row)
    print(num0)
    print(num1)



# getting some /0 and complex number errors
# also not creating good non-clustering maps
def ClusterFloodFill():
    global map
    map =  [[-1 for x in range(N)] for y in range(N)]
    q = queue.Queue()         # queue for flood fill
    num0 = N*N*(1-p)    # quota of 0's
    num1 = N*N*p        # quota of 1's
    #q.put([0,0])
    for i in range(N):
        for j in range(N):
            if(map[i][j] == -1):
                if(num0 + num1 > 0):
                    P = num1/(num0 + num1)      # local probability
                rand = random.uniform(0, 1) # generate random number
                if(rand < P):
                    val = 1
                else:
                    val = 0

                q.put([i, j])
                while(not q.empty()):
                    idx = q.get()                  # get index from queue
                    map[idx[0]][idx[1]] = val      # set index of map to val
                    # update count and probability
                    # unlike other random map generators, not determining if a
                    # 0 or a 1 should be placed, instead determining if floodfill
                    # should be continued
                    if(val == 1):
                        num1 -= 1
                        if(num0 + num1 > 0):
                            P = (num1/(num0 + num1))**(1/c)
                        else:
                            P = 0
                    else:
                        num0 -= 1
                        if(num0 + num1 > 0):
                            P = (num0/(num0 + num1))**(1/c)
                        else:
                            P = 0
                    # recurse
                    rand = random.uniform(0, 1)
                    if(rand < P and i < N-1):
                        if(map[i+1][j] == -1):
                            q.put([i+1, j])

                    rand = random.uniform(0, 1)
                    if(rand < P and i > 0):
                        if(map[i-1][j] == -1):
                            q.put([i-1, j])

                    rand = random.uniform(0, 1)
                    if(rand < P and j < N-1):
                        if(map[i][j+1] == -1):
                            q.put([i, j+1])

                    rand = random.uniform(0, 1)
                    if(rand < P and j > 0):
                        if(map[i][j-1] == -1):
                            q.put([i, j-1])



# starts with a list of indexes 0 to N^2-1, shuffles the list into random order
# these represent the idexes of map stored in row major order
# set the first num0 indexes to 0, the rest to 1
# ensures quota is filled
def RandomShuffle():
    global map
    map =  [[-1 for x in range(N)] for y in range(N)]
    idx = []
    for i in range(N):
        for j in range(N):
            idx.append([j, i])
    # sort idx
    # InsertionShuffle: CS 473 UIUC Lecture 1
    for i in range(N*N):
        rand = random.randint(0, i)
        temp = idx[i]
        idx[i] = idx[rand]
        idx[rand] = temp

    for i in range(N*N):
        x = idx[i][0]
        y = idx[i][1]
        if(i < N*N*p):
            map[y][x] = 1
        else:
            map[y][x] = 0



# c = 1 does not make this the same as RandomShuffle
def RandomShuffleCluster():
    global map
    # ideal function for P = f(p, c)
    # c = 1 -> f = 0
    # as c -> inf f slowly -> 1
    # f(p, c) = 1 - (1-p)^((c-1)/100)) works (10 is arbitrary, the higher the number
    # in the denomiator of the exponent, the slower the increase of f with c)
    # Very open to experimentation on this
    P = 1 - (1-p)**((c-1)/10)
    # if this number gets high, map is usually filled in one floodfill
    num1 = N*N*p
    q = queue.Queue()
    map =  [[0 for x in range(N)] for y in range(N)]
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

    print(num1)
    for i in range(N*N):
        if(num1 <= 0):
            print(i)
            break;
        x = idx[i][0]
        y = idx[i][1]
        if(num1 > 0 and map[y][x] == 0):
            q.put([x, y])
            while(not q.empty() and num1 > 0):
                point = q.get()                  # get point on map from queue
                x = point[0]
                y = point[1]

                # update count and probability
                # unlike other random map generators, not determining if a
                # 0 or a 1 should be placed, instead determining if floodfill
                # should be continued, in this case flood fill is done for
                # only the 1's with randomly selected starting points, the rest
                # is filled in with 0's
                if(map[y][x] == 0):
                    map[y][x] = 1
                    num1 -= 1
                    # recurse
                    rand = random.uniform(0, 1)
                    if(rand < P and y < N-1):
                        if(map[y+1][x] == 0):
                            q.put([x, y+1])

                    rand = random.uniform(0, 1)
                    if(rand < P and y > 0):
                        if(map[y-1][x] == 0):
                            q.put([x, y-1])

                    rand = random.uniform(0, 1)
                    if(rand < P and x < N-1):
                        if(map[y][x+1] == 0):
                            q.put([x+1, y])

                    rand = random.uniform(0, 1)
                    if(rand < P and x > 0):
                        if(map[y][x-1] == 0):
                            q.put([x-1, y])
    print(num1)







def numNeighbors(): # checks number of differnet neighbors
    count = 0
    for i in range(1, N-1, 1):
        for j in range(1, N-1, 1):
            if(map[i][j] == map[i-1][j]):
                count += 1
            if(map[i][j] == map[i+1][j]):
                count += 1
            if(map[i][j] == map[i][j-1]):
                count += 1
            if(map[i][j] == map[i][j+1]):
                count += 1
    print(count/((N-2)*(N-2)*4))    # not sure what to call this, relates to clustering

#RandomPure()
#RandomIterative()
#ClusterPure()
#ClusterIterative()
#ClusterFloodFill()
#RandomShuffle()
RandomShuffleCluster()
numNeighbors()


x = np.arange(0, N, 1)
y = np.arange(0, N, 1)
x, y = np.meshgrid(x, y)
cMap = colors.ListedColormap(['blue', 'orange'])

plt.pcolormesh(x, y, map, cmap = cMap)
plt.colorbar()
plt.show()
