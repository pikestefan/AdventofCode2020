# -*- coding: utf-8 -*-
"""
Created on Mon Dec 28 17:17:12 2020

@author: Lucio
"""
import re
from collections import defaultdict

def def_val():
    return False

def move_to_new(index, direction):
    i, j = index
    
    ### Indeces represent the two orthogonal Bragg planes of the lattice
    d_i, d_j = 0, 0
    if direction == 'w':
        d_i, d_j = -1, 1
    elif direction == 'e':
        d_i, d_j = 1, -1
    elif direction == 'ne':
        d_i = 1
    elif direction == 'sw':
        d_i = -1
    elif direction == 'nw':
        d_j = 1
    elif direction == 'se':
        d_j = -1
        
    return i + d_i, j + d_j

def get_neighbours(index, tile_dictionary):
    
    neighbour_list = []
    for direction in ['ne','e','se','sw','w','nw']:
        neighbour_list.append( move_to_new(index, direction) )
        
    neighbour_val = []
    tiles_to_check = []
    for neighbour in neighbour_list:
        if neighbour in tile_dictionary:
            neighbour_val.append(tile_dictionary[neighbour])
        else:
            tiles_to_check.append(neighbour)
    
    return neighbour_val, tiles_to_check
        
    

pattern = r'n{}|s{}|w|e'.format('[e,w]','[e,w]')

with open('inputs/day24.txt') as file:
    tiles = [line.strip() for line in file.readlines()]
    
tile_dirs = [re.findall(pattern, tile) for tile in tiles]

### Part 1
tile_dict = dict()
for tile in tile_dirs:
    
    idx = (0,0)
    for step in tile:
        idx = move_to_new(idx, step)
    # True represents black tile, False white tile
    if idx in tile_dict:
        tile_dict[idx] = not tile_dict[idx]
    else:
        tile_dict[idx] = True
        
print(sum(tile_dict.values()))

### Part 2
current_tile_dict = dict(tile_dict)
tile_list = list(tile_dict.keys())
for day in range(1,101):
    
    
    new_tile_dict = dict(current_tile_dict)
    all_tiles_to_check = []
    for tile, curr_is_black in current_tile_dict.items():
        neighbour_vals, to_check = get_neighbours(tile, current_tile_dict)
        
        # Check the neighbourhood, if there are currently missing tiles with
        # two adjacent black tiles, add them with the black value
        all_tiles_to_check += to_check
        
        black_count = sum( neighbour_vals)
        #Now flip the existing tiles if needed
        if curr_is_black and ((black_count == 0) or (black_count > 2)):
            new_tile_dict[tile] = False
        elif (not curr_is_black) and (black_count == 2):
            new_tile_dict[tile] = True
            
    # Now have a look at the non-existing tiles, if they are adjacent to two
    # black tiles add them as a black tile
    all_tiles_to_check = list( dict.fromkeys(all_tiles_to_check) ) 
    for tile_to_check in all_tiles_to_check:

        neighbour_vals, _ =  get_neighbours(tile_to_check, current_tile_dict)
        if sum(neighbour_vals) == 2:
            new_tile_dict[tile_to_check] = True
            
    current_tile_dict = dict(new_tile_dict)
    
print('Day {:d}:'.format(day), sum(new_tile_dict.values()))
            
