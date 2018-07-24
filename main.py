import numpy as np
import math
import scipy.stats
import random

# creates an NxN array of 1's and 0's with an expected percent of p 1's

# another method is to pick array indexes at random and place 1's until quota is filled
# the the rest with 0's
# However this might be harder to scale to having clustering of numbers
N = 5
p = .2

num0 = N*N*(1-p)    # quota of 0's
num1 = N*N*p       # quota of 1's

map = []
for i in range(N):
    row = []
    for j in range(N):
        # Fill in an element with a 1 or 0 determined by a bernoilli random variable
        # Probabily is based on past values which have been filled in
        P = num1/(num0 + num1)  # local probability
        print(P)
        rand = random.uniform(0, 1) # generate random number
        if(rand < P):
            row.append(1)
            num1 -= 1
            print(1)
        else:
            row.append(0)
            num0 -= 1
            print(0)
    map.append(row)

print(map)
