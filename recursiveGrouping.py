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

MapType = 0     # Select type of voter map to be created

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




# recursively splits map unitl G even groups are created

# start with everything in group 0
map = [[0 for x in range(N)] for y in range(N)]


population = math.ceil(N*N*pA) + math.ceil(N*N*pB)
RecursiveGrouping(N, G, population, PMap, map, 0, [0,0], 0):


# G = number of groups the input map needs to be split into
# pop = population of input map
# popMap = holds population for the voter map which was randomly generated
# map = map of groupings
# currGroup = map indexes with this value are considered to be the
def RecursiveGrouping(G, pop, popMap, map, currGroup, startIdx, mode):
    if(G > 1):
        # the map will be split into 2 connected sub maps the first will contain G1 groupSize
        # the second will contain G2 groups
        G1 = round(G/2)
        G2 = G - G1
        # Target population of subgroup 1
        quota1 = pop*G1/G
        pop1 = 0

        # horizontal linear group creation
        ### TODO: Don't do linear, do random floodfill and have smaller group
        # eat the larger
        # check reachability of eaten group and if not reachable create a bridge?
        # problem I am trying to solve: Given a connected graph G with weighted
        # vertices find two connected subgraphs G1 and G2 such that the difference
        # in the sum of the weights of the verices for each subgraph is minimized
        # Can this be modeled as a DAG with 
        if(mode == 0):
            while()


    # if G == 1, base case do nothing
