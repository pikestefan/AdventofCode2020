# -*- coding: utf-8 -*-
"""
Created on Thu Dec 17 11:40:46 2020

@author: Lucio
"""

import numpy as np

def remap_characters(character):
    if character == '#':
        output = 1
    elif character == '.':
        output = 0
    return output

def get_neighbour_val_v2( matrix, ind_tuple ):
    w, z, x, y = ind_tuple
    
    if x == 0:
        start_x = 0
    else:
        start_x = x -1
        
    if y == 0:
        start_y = 0
    else:
        start_y = y -1
        
    if z == 0:
        start_z = 0
    else:
        start_z = z - 1
        
    if w == 0:
        start_w = 0
    else:
        start_w = w - 1
        
    neighbourhood = matrix[ start_w : w + 2, start_z : z + 2,
                            start_x : x + 2, start_y : y + 2 ]
    
    return np.sum( neighbourhood ) - matrix[ind_tuple]

def do_cycle_v2( matrix ):
    
    new_matrix = np.copy(matrix)
    max_w, max_z, max_x, max_y = new_matrix.shape
    
    for w in range(max_w):
        for z in range(max_z):
            for x in range(max_x):
                for y in range(max_y):
                    coord_tuple = (w, z, x, y)
                    value = matrix[coord_tuple]
                    neighbour_val = get_neighbour_val_v2(matrix, coord_tuple )
                    if ( value == 1 ) and not ( 2<=neighbour_val<=3 ):
                        new_matrix[coord_tuple] = 0
                        
                    elif (value == 0) and (neighbour_val == 3):
                        new_matrix[coord_tuple] = 1
                        
    return new_matrix


def get_neighbour_val_v1( matrix, ind_tuple ):
    z, x, y = ind_tuple
    
    if x == 0:
        start_x = 0
    else:
        start_x = x -1
        
    if y == 0:
        start_y = 0
    else:
        start_y = y -1
        
    if z == 0:
        start_z = 0
    else:
        start_z = z - 1
        
    neighbourhood = matrix[ start_z : z + 2, start_x : x + 2, start_y : y + 2 ]
    
    return np.sum( neighbourhood ) - matrix[ind_tuple]

def do_cycle_v1( matrix ):
    
    new_matrix = np.copy(matrix)
    max_z, max_x, max_y = new_matrix.shape
    
    for z in range(max_z):
        for x in range(max_x):
            for y in range(max_y):
                coord_tuple = (z, x, y)
                value = matrix[coord_tuple]
                
                neighbour_val = get_neighbour_val_v1(matrix, coord_tuple )
                if ( value == 1 ) and not ( 2<=neighbour_val<=3 ):
                    new_matrix[coord_tuple] = 0
                    
                elif (value == 0) and (neighbour_val == 3):
                    new_matrix[coord_tuple] = 1
                    
    return new_matrix

def do_many_cycles( matrix, cycle_num, cycle_function ):
    new_matrix = np.copy(matrix)
    for ii in range(cycle_num):
        new_matrix = np.pad(new_matrix, pad_width=1, mode='constant',
                            constant_values = 0)
        
        new_matrix = cycle_function(new_matrix)
    return new_matrix
    
with open('inputs/day17.txt') as file:
    starting_area = []
    for line in file.readlines():
        line = [ character for character in line.strip()]
        line = list( map(remap_characters, line) )
        
        starting_area.append(line)
  

# Part 1
area_3d = np.array(starting_area, ndmin = 3, dtype = int)

final_output = do_many_cycles(area_3d, 6, do_cycle_v1)
        
print(np.sum(final_output))

# Part 2
area_4d = np.array(starting_area, ndmin = 4, dtype = int)

final_output = do_many_cycles(area_4d, 6, do_cycle_v2)
        
print(np.sum(final_output))

