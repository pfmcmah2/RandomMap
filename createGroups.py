import matplotlib.pyplot as plt
from matplotlib import colors
import numpy as np
import math
import scipy.stats
import random
import generateMap as gM
N = 100
p = .5
c = 1
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


map = gM.RandomShuffleCluster(N, p, c)

currGroup = 0
for x in range(N):
    for y in range(N):
        if(groupSize[currGroup] == 0):
            currGroup += 1
        if(map[y][x] == 1):
            groupVote[currGroup] += 1
        else:
            groupVote[currGroup] -= 1
        groupSize[currGroup] -= 1
        groupMap[y][x] = currGroup

print(groupVote)



x = np.arange(0, N, 1)
y = np.arange(0, N, 1)
x, y = np.meshgrid(x, y)
cMap = colors.ListedColormap(['blue', 'orange'])

plt.pcolormesh(x, y, map, cmap = cMap)
plt.colorbar()
plt.show()

plt.pcolormesh(x, y, groupMap)
plt.colorbar()
plt.show()
