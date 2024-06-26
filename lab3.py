# -*- coding: utf-8 -*-
"""lab3.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1-Pj5j__FLwpfxGNrUzTdeaJfOVtySy7v
"""

import numpy as np
import numba
from numba import cuda
from random import seed, random
import time

start = time.time()

r = 3
w = 2 * r
arr_size = 2000000

r_arr_x = np.random.uniform(0, w, size=arr_size)
r_arr_y = np.random.uniform(0, w, size=arr_size)
#print(r_arr_x)
#print(r_arr_y)
@cuda.jit
def in_circle(r, d_arr, r_arr_x, r_arr_y):

    i = ((cuda.threadIdx.x + cuda.blockDim.x * cuda.blockIdx.x)) 

    x = r_arr_x[i] 
    y = r_arr_y[i] 

    d = ((x-r)**2 + (y - r)**2)**(1/2)

    if d < r:
        d_arr[i] = 1
    else:
        d_arr[i] = 0


arr = np.full(arr_size, r)
d_arr = cuda.to_device(arr)

threads_per_block = 1
blocks_per_grid = (arr.size + (threads_per_block - 1)) // threads_per_block


in_circle[blocks_per_grid, threads_per_block](r, d_arr, r_arr_x, r_arr_y)

result_array = d_arr.copy_to_host()

print(result_array)

zeros = 0
ones = 0
for j in range(arr_size):

  if result_array[j] == 0:
    zeros = zeros + 1
  else:
    ones = ones + 1

ratio = ones / arr_size
area = ratio * w**2
pi = (area / (r**2))

print(ratio)
print(area)
print(pi)
end = time.time()
print(end - start)