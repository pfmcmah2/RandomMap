import matplotlib.pyplot as plt
from matplotlib import colors
import numpy as np
import math
import scipy.stats
import random
import generateMap as gM
N = 100
p = .2
c = 9

map = gM.RandomShuffleCluster(N, p, c)



x = np.arange(0, N, 1)
y = np.arange(0, N, 1)
x, y = np.meshgrid(x, y)
cMap = colors.ListedColormap(['blue', 'orange'])

plt.pcolormesh(x, y, map, cmap = cMap)
plt.colorbar()
plt.show()
