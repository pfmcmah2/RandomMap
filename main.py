import matplotlib.pyplot as plt
import numpy as np
import math
import scipy.stats
import random

# creates an NxN array of 1's and 0's with an expected percent of p 1's

# another method is to pick array indexes at random and place 1's until quota is filled
# the the rest with 0's
# However this might be harder to scale to having clustering of numbers
N = 100
p = .5
c = 1 # cluster
map = []

def generateRandomMap():
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



def generateClusterMap():
    # same as generateRandomMap but prioritizes same as neighbors
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
    print(count)


#generateRandomMap()
generateClusterMap()
numNeighbors()


x = np.arange(0, N, 1)
y = np.arange(0, N, 1)
x, y = np.meshgrid(x, y)

plt.pcolormesh(x, y, map)
plt.colorbar() #need a colorbar to show the intensity scale
plt.show() #boom
