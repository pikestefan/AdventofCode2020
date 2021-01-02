# -*- coding: utf-8 -*-
"""
Created on Sat Dec 12 18:22:51 2020

@author: Lucio
"""

import numpy as np

def get_neighbours(matrix, index_tuple):
    ii, jj = index_tuple
    
    neighbourhood = np.array(matrix[ ii-1 : ii+2, jj-1 : jj+2 ])
    neighbourhood[1,1] = '.'
    
    return len( neighbourhood[neighbourhood == '#'] )

def get_semiaxes(matrix, index_tuple, direction):
    
    ii, jj = index_tuple
    
    if direction == 'n':
        semiaxis = matrix[ii-1::-1,jj]
    elif direction == 'e':
        semiaxis = matrix[ii, jj + 1:]
    elif direction == 's':
        semiaxis = matrix[ii+1:,jj]
    elif direction == 'w':
        semiaxis = matrix[ii,jj - 1::-1]
    else:  
        rows, cols = matrix.shape

        if direction == 'ne':
            row_coords = np.arange(ii-1,-1,-1)
            col_coords = np.arange(jj + 1, cols)
            min_len = min( len(row_coords), len(col_coords))

            semiaxis = matrix[ (row_coords[:min_len]), col_coords[:min_len] ]
            
        elif direction == 'se':
            row_coords = np.arange(ii+1, rows)
            col_coords = np.arange(jj+1, cols)
            min_len = min( len(row_coords), len(col_coords))

            semiaxis = matrix[ (row_coords[:min_len]), col_coords[:min_len] ]
        elif direction == 'sw':
            row_coords = np.arange(ii+1, rows)
            col_coords = np.arange(jj-1, -1, -1)
            min_len = min( len(row_coords), len(col_coords))
           
        elif direction == 'nw':
            row_coords = np.arange(ii-1, -1, -1)
            col_coords = np.arange(jj-1, -1, -1)
            min_len = min( len(row_coords), len(col_coords))
            
            
        semiaxis = matrix[ (row_coords[:min_len]), col_coords[:min_len] ]
            
    return semiaxis

def get_neighbours_v2(matrix, index_tuple):
    
    directions = ['n','ne','e','se','s','sw','w','nw']
    
    neighbours = 0
    for direction in directions:
        semiax = get_semiaxes(matrix, index_tuple, direction)
        semiax = semiax[semiax != '.']
        if (semiax.size > 0) and (semiax[0] == '#'):
            neighbours += 1

    return neighbours
            

def print_mat(matrix):
    for row in matrix:
        line = ''
        for jj in row:
            line += jj
        print(line)
    print('\n')

def run_cycle_first(input_matrix):
    output_matrix = np.array(input_matrix)
    
    for ii in range(1, input_matrix.shape[0] - 1):
        for jj in range(1, input_matrix.shape[1] - 1):
            element = input_matrix[ii, jj]
            if element == 'L':
                occupied = get_neighbours(input_matrix, (ii, jj) )
                if occupied == 0:
                    output_matrix[ii, jj] = '#'
            elif element == '#':
                occupied = get_neighbours(input_matrix, (ii, jj) )
                if occupied >= 4:
                    output_matrix[ii, jj] = 'L'
                    
    return output_matrix

def run_cycle_second(input_matrix):
    output_matrix = np.array(input_matrix)
    
    for ii in range(1, input_matrix.shape[0] - 1):
        for jj in range(1, input_matrix.shape[1] - 1):
            element = input_matrix[ii, jj]
            if element == 'L':
                occupied = get_neighbours_v2( input_matrix, (ii, jj) )
                if occupied == 0:
                    output_matrix[ii, jj] = '#'
            elif element == '#':
                occupied = get_neighbours_v2(input_matrix, (ii, jj) )
                if occupied >= 5:
                    output_matrix[ii, jj] = 'L'
                    
    return output_matrix

def run_many_cycles(input_matrix, func):
    
    keep_going = True
    
    previous_matrix = np.array(input_matrix)
    while keep_going:
        new_matrix = func(previous_matrix)
        if np.all(new_matrix == previous_matrix):
            keep_going = False
        else:
            previous_matrix = np.copy(new_matrix)
    return new_matrix
            

with open('inputs/day11.txt') as file:
    
    seat_matrix = []
    
    for line in file.readlines():
        line = line.strip()
        row = [char for char in line]
        seat_matrix.append(row)
               
seat_matrix = np.array(seat_matrix)
seat_matrix = np.pad( seat_matrix, pad_width=1, constant_values = '.' )

#### Part 1
final_matrix = run_many_cycles(seat_matrix, run_cycle_first)
print( len( final_matrix[final_matrix == '#'] ) )

#### Part 2
final_matrix = run_many_cycles(seat_matrix, run_cycle_second)
print( len( final_matrix[final_matrix == '#'] ) )