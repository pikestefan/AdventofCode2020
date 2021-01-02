# -*- coding: utf-8 -*-
"""
Created on Mon Dec  7 17:09:57 2020

@author: Lucio
"""

import numpy as np

from math import ceil

base_patt = []
with open('inputs/day3.txt') as file:
    for line in file.readlines():
        string = line.strip()
        base_patt.append(list(string))
        
base_patt = np.array(base_patt)

traversed_columns = 3 * base_patt.shape[0]

req_reps = ceil(traversed_columns / base_patt.shape[1])

new_patt = np.tile(base_patt, req_reps)

tree_count = 0
for ii in range( new_patt.shape[0] ):
    if new_patt[ii, ii*3] == '#':
        tree_count += 1
        
print(tree_count)
        
### Part two
slope_list = np.array( [ [1,1],
                         [3,1],
                         [5,1],
                         [7,1],
                         [1,2]] )

traversed_columns = max( slope_list[:,0] ) * base_patt.shape[0]
req_reps = ceil(traversed_columns / base_patt.shape[1])
new_patt = np.tile(base_patt, req_reps)

tree_count = np.zeros( (len(slope_list), ), dtype = np.ulonglong )
for jj, slope in enumerate(slope_list):
    loc_tree_count = 0
    for ii in range( new_patt.shape[0] ):
        next_idx = [ii * slope[1], ii * slope[0]]
        if (next_idx[0] < new_patt.shape[0]) and (new_patt[next_idx[0], next_idx[1]] == '#'):
            loc_tree_count += 1
    tree_count[jj] = loc_tree_count
    
print(np.prod(tree_count))