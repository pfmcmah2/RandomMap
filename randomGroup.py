import matplotlib.pyplot as plt
from matplotlib import colors
import numpy as np
import math
import random
import queue
import openMap as oM

# for the sake of variable names 1 voters will be called A's and -1 voters B's
# A's have color blue, B's have color red

# Fills an NxN map in with G equal size groups
# Picks G start locations from map at random
# Performs G queue based floodfills simultanously
# Should produce simiplar shaped groups - not truly random
# For a map with empty spaces, could be more random
# Not truly random but fair in terms of voting

# DONE: if a group is densly populated slow it's spread, similar to the
# original clustering methods have number of points expanded to be a function of
# current population of the groups, i.e. above average population -> smaller expansion
# with min 1, randomly shuffle the four directions and take the first n

# NOTE: 2:1 advantage in voters usually leads to all groups belonging to majority party
# unless very high cluster size in which case ~1 group goes to minority
# clusteing irl might be higher than I had thought
# creating good test maps is likely a more difficult task than creating fair groups

# NOTE: BRFS is by far the best method for creating random groups so far 8/7/18
# Very little difference in results for maxSkip = 100 and 500
# Better off increasing number of test group maps generated with lower maxSkip

# Map is visulaized in the following way: (0,0) (0,1) (0,2)
# (0,0) is top left                       (1,0) (1,1) (1,2)
# (2,2) is bottom right                   (2,0) (2,1) (2,2)


N = 100
G = 20
groupSize = []
numSquares = N*N
pA = .4
pB = .4


# create map of voters
# voteMap = oM.RandomShuffleControlledCluster(N, pA, pB, 100, 200)
Map = oM.RSCC_Stacking(N, pA, pB, 5, 2)
voteMap = Map[0]
pMap = Map[1]



### PURE RANDOM FLOODFILL
# goes until all queues have been emptied, does not guarentee equal sized groups
def PureRandomFloodfill(N, G):
    # initialize
    queues = []
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
    return map

### BALANCED RANDOM FLOODFILL
# goes until all queues have been emptied
# expands to 2 to 4 points depending on relative size of group
def BalancedRandomFloodfill(N, G, voteMap):
    # initialize
    queues = []
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
    return map


### BALANCED RANDOM FLOODFILL
# goes until all queues have been emptied
# skips expansion if group is larger than average
# only skips a certain number of times in a row to avoid hang
# takes in populationMap instead of voteMap, built to be used with RSCC_Stacking
def BalancedRandomFloodfillSkip(N, G, maxSkip, populationMap):
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
        totalVoters -= populationMap[startLocation[i][1]][startLocation[i][0]]
        groupSize[i] = populationMap[startLocation[i][1]][startLocation[i][0]]

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
                        groupSize[i] += populationMap[y+1][x]
                        newVoters += populationMap[y+1][x]

                if(y > 0):
                    if(map[y-1][x] == -1):
                        map[y-1][x] = i
                        queues[i].put([x, y-1])
                        groupSize[i] += populationMap[y-1][x]
                        newVoters += populationMap[y-1][x]

                if(x < N - 1):
                    if(map[y][x+1] == -1):
                        map[y][x+1] = i
                        queues[i].put([x+1, y])
                        groupSize[i] += populationMap[y][x+1]
                        newVoters += populationMap[y][x+1]

                if(x > 0):
                    if(map[y][x-1] == -1):
                        map[y][x-1] = i
                        queues[i].put([x-1, y])
                        groupSize[i] += populationMap[y][x-1]
                        newVoters += populationMap[y][x-1]

        # increment group number
        i = (i + 1)%G
    return map

# same as BRFS but includes group size in output
# Output[0] = map,   Output[1] = groupSize
def BRFS_G(N, G, maxSkip, voteMap):
    # initialize
    # TODO: Test Different maxSkip values increasing maxSkip should decrease stdev of group size
    # Not sure if there is a way to guarentee an upper bound on stdev size
    # maxSkip;  max number of turns than can be skipped for a group
    skip = [0 for i in range(G)]    # number of turns which have been skipped for each
    groupSize = [1 for i in range(G)]   # had to change initialization for iterative method
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
                        if(voteMap[y+1][x] != 0): # if point on map is populted inc count
                            groupSize[i] += 1
                            newVoters += 1

                if(y > 0):
                    if(map[y-1][x] == -1):
                        map[y-1][x] = i
                        queues[i].put([x, y-1])
                        if(voteMap[y-1][x] != 0):
                            groupSize[i] += 1
                            newVoters += 1

                if(x < N - 1):
                    if(map[y][x+1] == -1):
                        map[y][x+1] = i
                        queues[i].put([x+1, y])
                        if(voteMap[y][x+1] != 0):
                            groupSize[i] += 1
                            newVoters += 1

                if(x > 0):
                    if(map[y][x-1] == -1):
                        map[y][x-1] = i
                        queues[i].put([x-1, y])
                        if(voteMap[y][x-1] != 0):
                            groupSize[i] += 1
                            newVoters += 1

        # increment group number
        i = (i + 1)%G
    return [map, groupSize]

# NOT WORKING
def StructuedFloodfill(N, G, pA, pB, voteMap):
    # modify this to set to G-1, last group is what's left
    map = [[-1 for x in range(N)] for y in range(N)]

    # List of starting locations (top left corner) of new groups
    # startList = [[0, 0]]
    quota = N*N*(pA+pB)

    #main loop, i = group id#
    for i in range(G-1):
        # new group
        print(i)

        # use start point closest to top, tie breaker closest to left
        # could change this to closest to (0,0)
        # should be a better way to to this testing below
        '''startPoint = [-1, -1]
        found = False
        for y in range(N):
            for x in range(N):
                if(map[y][x] == -1):
                    startPoint = [x, y]
                    map[y][x] = i   # mark group on map
                    found = True
                    break
            if(found):
                break
        print('startPoint = ', startPoint)'''


        ###startPoint = [N, N]
        #### use start point closest to top, tie breaker closest to left
        ###for j in startList:
        ###    if(j[1] < startPoint[1] or (j[1] == startPoint[1] and j[0] < startPoint[0])):
        ###        startPoint = j
        ###startList.remove(startPoint)


        # do a standard floodfill until population = groupSize
        groupSize = quota/(G - i)
        quota -= groupSize
        population = 1

        q = queue.Queue()
        q.put(startPoint)
        while(population < groupSize):
            point = q.get()
            x = point[0]
            y = point[1]

            if(population < groupSize and y < N-1):
                if(map[y+1][x] == -1):
                    map[y+1][x] = i
                    q.put([x, y+1])
                    if(voteMap[y+1][x] != 0):
                        population += 1

            if(population < groupSize and y > 0):
                if(map[y-1][x] == -1):
                    map[y-1][x] = i
                    q.put([x, y-1])
                    if(voteMap[y-1][x] != 0):
                        population += 1

            if(population < groupSize and x < N-1):
                if(map[y][x+1] == -1):
                    map[y][x+1] = i
                    q.put([x+1, y])
                    if(voteMap[y][x+1] != 0):
                        population += 1

            if(population < groupSize and x > 0):
                if(map[y][x-1] == -1):
                    map[y][x-1] = i
                    q.put([x-1, y])
                    if(voteMap[y][x-1] != 0):
                        population += 1

    # last group takes whatever is left
    return map


# most simple implementation I can think of
# linear "snaking" traversal, fills quota extactly
# fair for a random input but doesn't make sense for practical use due to
# a it ignores city/tow/community structure in favor of geometric structure
def RandomLinear(N, G, pA, pB, voteMap):
    # final group (# G-1) is made up of what's left
    map = [[G-1 for x in range(N)] for y in range(N)]
    quota = N*N*(pA + pB)
    groupSize = []
    # set group size
    for i in range(G-1):
        size = round(quota/(G-i))
        groupSize.append(size)
        quota -= size

    # start point
    point = [0, 0]
    # direction of movement
    direction = 1
    for i in range(G-1):
        count = 0
        while(count < groupSize[i]):
            x = point[0]
            y = point[1]
            map[y][x] = i   # set map to group id#
            if(voteMap[y][x] != 0):
                count += 1

            if(direction == 1):   # expand to the right
                if(point[0] == N-1):     # if at end of row move to next row
                    point[1] += 1
                    direction = -1  # change direction
                else:
                    point[0] += 1
            else:
                if(point[0] == 0):     # if at end of row move to next row
                    point[1] += 1
                    direction = 1  # change direction
                else:
                    point[0] -= 1
    return map



# runs BalancedRandomFloodfillSkip I times and takes the result with the lowest
# standard deviation for group size
def IterativeBRFS(I, N, G, maxSkip, voteMap):
    STD = N*N
    map = []
    for i in range(I):
        tempMap = BRFS_G(N, G, maxSkip, voteMap)
        print(tempMap[1])
        tempSTD = np.std(tempMap[1])    # take stdev of groupSize
        print(tempSTD)
        if(tempSTD < STD):
            STD = tempSTD
            map = tempMap[0]
    return map


# same skip method as BRFS
# shapes groups to favor party A (1 voters)
# this is done by creating grops in which A wins by a slim margin
# and in which B wins by a large margin in order to cluster all B voters into
# a few groups
# TODO: work on this
def BiasedFloodfill(N, G, pA, pB, maxSkip, voteMap):
    # initialize
    targetGroupSize = N*N*(pA+pB)/G
    # Not sure if there is a way to guarentee an upper bound on stdev size
    # maxSkip;  max number of turns than can be skipped for a group
    skip = [0 for i in range(G)]    # number of turns which have been skipped for each
    groupSize = [1 for i in range(G)]   # had to change initialization for iterative method
    voteBalance = [0 for i in range(G)]
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

                # let the groups expand naturally initially
                # for now, just focus on B donminated groups
                if(groupSize[i] < targetGroupSize/10 or voteBalance[i] >= 0):
                    # fill in surrounding elements
                    # filling in elements when added to queue, rather than when

                    skipFlag = True     # if over target size only allow one expand

                    if(y < N - 1 and skipFlag):
                        if(map[y+1][x] == -1):
                            if(groupSize[i] > targetGroupSize):
                                skipFlag = False
                            map[y+1][x] = i
                            queues[i].put([x, y+1])
                            if(voteMap[y+1][x] != 0): # if point on map is populted inc count
                                groupSize[i] += 1
                                voteBalance[i] += voteMap[y+1][x]
                                newVoters += 1

                    if(y > 0 and skipFlag):
                        if(map[y-1][x] == -1):
                            if(groupSize[i] > targetGroupSize):
                                skipFlag = False
                            map[y-1][x] = i
                            queues[i].put([x, y-1])
                            if(voteMap[y-1][x] != 0):
                                groupSize[i] += 1
                                voteBalance[i] += voteMap[y-1][x]
                                newVoters += 1

                    if(x < N - 1 and skipFlag):
                        if(map[y][x+1] == -1):
                            if(groupSize[i] > targetGroupSize):
                                skipFlag = False
                            map[y][x+1] = i
                            queues[i].put([x+1, y])
                            if(voteMap[y][x+1] != 0):
                                groupSize[i] += 1
                                voteBalance[i] += voteMap[y][x+1]
                                newVoters += 1

                    if(x > 0 and skipFlag):
                        if(map[y][x-1] == -1):
                            if(groupSize[i] > targetGroupSize):
                                skipFlag = False
                            map[y][x-1] = i
                            queues[i].put([x-1, y])
                            if(voteMap[y][x-1] != 0):
                                groupSize[i] += 1
                                voteBalance[i] += voteMap[y][x-1]
                                newVoters += 1

                else:
                    neighbors = []  # holds vote and direction of neighbors
                    if(y < N - 1):
                        if(map[y+1][x] == -1):
                            neighbors.append([voteMap[y+1][x], [0, 1]])

                    if(y > 0):
                        if(map[y-1][x] == -1):
                            neighbors.append([voteMap[y-1][x], [0, -1]])

                    if(x < N - 1):
                        if(map[y][x+1] == -1):
                            neighbors.append([voteMap[y][x+1], [1, 0]])

                    if(x > 0):
                        if(map[y][x-1] == -1):
                            neighbors.append([voteMap[y][x-1], [-1, 0]])

                    neighbors.sort() # put 1's last
                    # expand
                    for j in range(len(neighbors)):
                        if(neighbors[j][0] != 1):
                            # apply direction of expand
                            Y = y + neighbors[j][1][1]
                            X = x + neighbors[j][1][0]
                            map[Y][X] = i
                            queues[i].put([X, Y])
                            if(voteMap[Y][X] != 0):
                                groupSize[i] += 1
                                voteBalance[i] += voteMap[Y][X]
                                newVoters += 1






        # increment group number
        i = (i + 1)%G
    return map

#map = PureRandomFloodfill(N, G)
#map = BalancedRandomFloodfill(N, G, voteMap)
# changed for testing not working use BRFS_G
#map = BalancedRandomFloodfillSkip(N, G, 100, pMap)
#map = StructuedFloodfill(N, G, pA, pB, voteMap)
#map = RandomLinear(N, G, pA, pB, voteMap)
#map = BiasedFloodfill(N, G, pA, pB, 10, voteMap)

#map = IterativeBRFS(100, N, G, 5, voteMap)

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

#print('groupSize = ', groupSize)
print('groupPopulation = ', groupPopulation)
print('stdev = ', np.std(groupPopulation))
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
