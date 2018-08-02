import matplotlib.pyplot as plt
from matplotlib import colors
import numpy as np
import math
import scipy.stats
import random
import openMap as oM
N = 200
p = .5
pA = .4
pB = .4
c = 100
s = 25
numGroups = 7

# assigns number of squares for each group
numSquares = N*N
groupSize = []
for i in range(numGroups):
    val = round(numSquares/(numGroups - i))
    numSquares -= val
    groupSize.append(val)
# count of vote of groups, positivie -> 1, negative -> -1
groupVote = [0 for i in range(numGroups)]
# map of groups
groupMap = [[0 for x in range(N)] for y in range(N)]

print(groupSize)


map = oM.RandomShuffleControlledCluster(N, pA, pB, c, s)

currGroup = 0
for x in range(N):
    for y in range(N):
        if(groupSize[currGroup] == 0):
            currGroup += 1
        groupVote[currGroup] += map[y][x]
        groupSize[currGroup] -= 1
        groupMap[y][x] = currGroup

print(groupVote)



x = np.arange(0, N, 1)
y = np.arange(0, N, 1)
x, y = np.meshgrid(x, y)
cMap = colors.ListedColormap(['blue', 'white', 'red'])

plt.pcolormesh(x, y, map, cmap = cMap)
plt.colorbar()
plt.show()

plt.pcolormesh(x, y, groupMap)
plt.colorbar()
plt.show()
