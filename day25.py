# -*- coding: utf-8 -*-
"""
Created on Thu Dec 31 12:30:32 2020

@author: Lucio
"""

from math import log, floor
import timeit

with open('inputs/day25.txt') as file:
    
    card_public = int( file.readline().strip() )
    door_public = int( file.readline().strip() )
    
def key_gen(loops, start_number = 1, subj_number = 7):
    
    number = start_number
    
    for ii in range(loops):
        number *= subj_number
        number %= 20201227
    
    return number

def get_loop_size( target_number=0, subject = 7 ):
    
    number = 1
    divisor = 20201227
    
    loops = 0
    while number != target_number:
        
        number *= subject
        number %= divisor
        
        loops += 1
        
    return loops
        
### Part  1

door_loops = get_loop_size(target_number=door_public)
card_loops = get_loop_size(target_number=card_public)

card_encrypted = key_gen(card_loops, subj_number=door_public)
door_encrypted = key_gen(door_loops, subj_number=card_public)

print(card_encrypted)

