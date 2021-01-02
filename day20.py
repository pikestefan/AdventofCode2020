# -*- coding: utf-8 -*-
"""
Created on Mon Dec 21 22:14:36 2020

@author: Lucio
"""

import numpy as np
from collections import OrderedDict, deque
import re
import matplotlib.pyplot as plt
from matplotlib import colors

with open('inputs/day20.txt') as file:
    
    original_dict = dict()
    tile_list = []
    
    for line in file.readlines():
        line = line.strip()
        if 'Tile' in line:
            _, ID = line.split(' ')
            ID = int(ID[:-1])
        elif line != '':
            tile_list.append([0 if char == '.' else 1 for char in line])
        else:
            original_dict[ID] = np.array(tile_list, dtype = int)
            ID = ''
            tile_list= []
            
    original_dict[ID] = np.array(tile_list, dtype = int)
            
def get_tile_edges(tile):
    
    edge_dict = [ ['t', tile[0,:]  ],
                  ['r', tile[:,-1] ],
                  ['b', tile[-1,::-1] ],
                  ['l', tile[::-1,0]  ],
                   ]
    return edge_dict

def get_matrix_operation(dir1, dir2):
    
    
    directions = ['t','r','b','l']
    opposites  = ['b','l','t','r' ]
    
    dir1_idx = directions.index(dir1)
    dir2_idx = directions.index(dir2)
    
    opposite_dir1 = opposites[ dir1_idx ]
    
    rotation = 0
    new_dir = dir2
    if dir2 != opposite_dir1:
        ii = dir2_idx + 1
        while new_dir != opposite_dir1:
            new_dir = directions[ ii % 4]
            rotation += 90
            ii += 1
            
    return new_dir, -rotation

def add_ID(array, curr_ID, matched_ID, dir_rel_to_curr):

    ID_row, ID_col = np.argwhere( array == curr_ID )[0]
    
    curr_rows, curr_cols = array.shape
    
    new_row, new_col = ID_row, ID_col
    if dir_rel_to_curr == 't':
         new_row -= 1
    elif dir_rel_to_curr == 'b':
        new_row += 1
    elif dir_rel_to_curr == 'r':
        new_col += 1
    elif dir_rel_to_curr == 'l':
        new_col -= 1
        
    if new_row >= curr_rows:
        array = np.vstack( (array, np.zeros((1,curr_cols)) ) )
    elif new_row < 0:
        array = np.vstack( (np.zeros((1,curr_cols)), array ) )
        new_row += 1
    elif new_col >= curr_cols:
        array = np.hstack( (array, np.zeros((curr_rows,1)) ) )
    elif new_col < 0:
        array = np.hstack( (np.zeros((curr_rows,1)), array ) )
        new_col += 1
    
    array[new_row, new_col] = matched_ID
    return array


def find_snake(string_list):
                      # 
    #    ##    ##    ###
     #  #  #  #  #  #    
    pattern_mid = r'(?=(#(.{4})##(.{4})##(.{4})###))'
    pattern_bot = r'((.{1})#' + '(.{2})#'*4 + '(.{2})#(.{3}))'
    
    found_snakes = []
    #Mid patten is allowed to match only from 1 to -1
    for ii in range(1, len(string_list) -1  ):
        line = string_list[ii]
        matched_mid = re.findall(pattern_mid, line)
        
        if len(matched_mid)>0: 
            for midline in matched_mid:
                midline = midline[0]
                mid_patt_len = len(midline)
                mid_idx = line.find(midline)
                
                #Check if the "horn" is there
                top_substring = string_list[ii-1]
                horn_is_there = top_substring[mid_idx + mid_patt_len - 2] == '#'
                if horn_is_there:
                    bott_substring = string_list[ii+1]
                    bott_substring = bott_substring[mid_idx:mid_idx+mid_patt_len]
                    bottom_match = re.match(pattern_bot, bott_substring)
                    if bottom_match is not None:
                        body_is_there = True
                    else:
                        body_is_there = False
                
                if horn_is_there and body_is_there:
                    
                    string = string_list[ii]
                    mid_substring = string[mid_idx:mid_idx+mid_patt_len]
                    replace_mid = re.sub(pattern_mid[3:-1], r'o\2oo\3oo\4ooo', mid_substring)
                    replace_mid = (string[:mid_idx] + replace_mid + 
                                   string[mid_idx+mid_patt_len:] )
                    
                    string = string_list[ii + 1]
                    replace_bot = re.sub(pattern_bot, r'\2o\3o\4o\5o\6o\7o\8', bott_substring)
                    replace_bot = (string[:mid_idx] + replace_bot + 
                                   string[mid_idx+mid_patt_len:] )
                    
                    #Put the horn in the top string
                    string = string_list[ii-1]
                    
                    replace_top = [char for char in string_list[ii-1] ]
                    replace_top[ mid_idx + mid_patt_len - 2 ] = 'o'
                    replace_top = ''.join(replace_top)
                    
                    string_list[ii-1] = replace_top
                    string_list[ii] = replace_mid
                    string_list[ii+1] = replace_bot
                    found_snakes.append([ re.sub(pattern_mid, r'o\2oo\3oo\4ooo', midline) ])
                    #found_snakes.append([ replace_top, replace_mid, replace_bot ])
    return found_snakes

def make_stringed_image(image_array):
    output_image = []
    for row in image_array:
        line = ''.join(row)
        output_image.append(line)
    return output_image

### Part 1
tile_dict = dict( original_dict )

tile_list = list(tile_dict.keys())

start = tile_list[0]

# I use the queue to keep track of which tiles have been aligned to the previous ones
tile_queue = deque()
tile_queue.append(start)

ID_array = np.zeros((3,3), dtype = int)
ID_array[1,1] = start

while tile_list:
    
    curr_tileID = tile_queue.popleft()
    #At the end of the while step, the current tile will have all the borders
    #matched, so there is no need to check it again
    tile_list.remove(curr_tileID)

    curr_borders = get_tile_edges( tile_dict[curr_tileID] )
    
    for otherID in tile_list:
        compare_tile = tile_dict[otherID]
        compare_borders = get_tile_edges( compare_tile )
        
        match_found = False
        ii = 0
        while not match_found and ii < 4:
            curr_dir, curr_border = curr_borders[ii]
            
            for comp_dir, comp_border in compare_borders:
                #Check for a normal match
                if np.all(comp_border == curr_border):
                    matching_side, rotation = get_matrix_operation(curr_dir,
                                                                   comp_dir)
                    rotated_tile = np.rot90(compare_tile, rotation // 90)
                    
                    if (curr_dir == 't') or (curr_dir == 'b'):
                        rotated_tile = np.fliplr(rotated_tile)
                    else:
                        rotated_tile = np.flipud(rotated_tile)
                    
                    tile_dict[otherID] = rotated_tile
                    match_found = True
                    
                #Else check for a flipped match
                elif np.all(comp_border[::-1] == curr_border):
                    matching_side, rotation = get_matrix_operation(curr_dir,
                                                                   comp_dir)
                    
                    rotated_tile = np.rot90(compare_tile, rotation // 90)
                    
                    tile_dict[otherID] = rotated_tile
                    match_found = True
            ii += 1
        if match_found and (otherID not in ID_array):
            tile_queue.appendleft(otherID)
            ID_array = add_ID(ID_array, curr_tileID, otherID, curr_dir)

#Delete remaining 0 columns
idx = np.argwhere(np.all(ID_array == 0, axis=0))
ID_array = np.delete(ID_array, idx, axis=1)

#Delete remaining 0 rows
idx = np.argwhere(np.all(ID_array == 0, axis=1))
ID_array = np.delete(ID_array, idx, axis=0).astype(np.longlong)

print(ID_array[0,0]*ID_array[0,-1]*ID_array[-1,0]*ID_array[-1,-1])

### Part 2
grid_size = ID_array.shape

tile_size = len(  tile_dict[ID_array[0,0]][1:-1,1:-1] )

image = np.zeros( (tile_size*grid_size[0],)*2, dtype = int )

for ii, row in enumerate(ID_array):
    for jj, ID in enumerate(row):
        reduced_tile = tile_dict[ID][1:-1,1:-1]
        image[ii*tile_size : (ii + 1) * tile_size,
              jj*tile_size : (jj + 1) * tile_size] = reduced_tile 

bare_image = np.array(image)        

image = image.astype(str)
image[image == '1'] = '#'
image[image == '0'] = '.'
    
found_snakes = []
rotator = 0
while (len(found_snakes) == 0) and (rotator > -4):
    curr_view = np.rot90(image, rotator)
    stringed_image = make_stringed_image( curr_view )
    found_snakes = find_snake(stringed_image)
    
    if len(found_snakes) == 0:
        stringed_image = make_stringed_image( np.fliplr(curr_view) )
        found_snakes = find_snake(stringed_image)
        
    if len(found_snakes) == 0:
        stringed_image = make_stringed_image( np.flipud(curr_view) )
        found_snakes = find_snake(stringed_image)
        
    rotator -= 1
    
if rotator == -4:
    print("Failed to find")

#Reconvert the sucessful image to numpy array
final_image = []
for line in stringed_image:
    line = [char for char in line]
    final_image.append(line)

final_image = np.array(final_image, dtype = str)

my_map = colors.LinearSegmentedColormap.from_list('gne', ['k','b','r'], N= 3)
plt.figure(figsize = (10,10))
to_plot = np.array(final_image)
to_plot[to_plot=='#'] = 1
to_plot[to_plot=='o'] = 2
to_plot[to_plot=='.'] = 0
to_plot = to_plot.astype(int)
plt.imshow(to_plot)
plt.axis('off')


print(len(final_image[final_image == '#']))
