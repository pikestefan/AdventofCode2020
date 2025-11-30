# -*- coding: utf-8 -*-
"""
Created on Wed Dec  9 18:44:32 2020

@author: Lucio
"""

import numpy as np

with open('inputs/day5.txt') as file:
    sequences = []
    for line in file.readlines():
        sequences.append(line.strip())

def find_seat_id(position_sequence):
    current_row_min = 1
    current_row_max = 128
    
    current_col_min = 1
    current_col_max = 8
    for char in position_sequence:
        row_split = ( current_row_max - current_row_min + 1 ) // 2
        col_split =  ( current_col_max - current_col_min + 1 ) // 2
        if char == 'F':
            current_row_max = current_row_min + row_split - 1
        elif char == 'B':
            current_row_min = current_row_min + row_split
        elif char == 'L':
            current_col_max = current_col_min + col_split - 1
        elif char == 'R':
            current_col_min = current_col_min + col_split
            
    return (current_row_max -1)* 8  + (current_col_max-1)

seat_ids = []
for sequence in sequences:
    seat_ids.append(find_seat_id(sequence))
    
sorted_ids = np.sort(seat_ids)

print(sorted_ids[-1])

#### Part 2
all_ids = np.arange(sorted_ids[0], sorted_ids[-1]+1)

print(np.setdiff1d(all_ids, sorted_ids))
    
        