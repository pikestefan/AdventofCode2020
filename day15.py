# -*- coding: utf-8 -*-
"""
Created on Tue Dec 15 11:21:38 2020

@author: Lucio
"""

from collections import deque, defaultdict

def def_value():
    return []

def custom_append(listy, new_el):
    if len(listy) < 2:
        listy.append(new_el)
    else:
        listy.pop(0)
        listy.append(new_el)
        
        
def test_deque():
    a = deque(maxlen=2)
    for ii in range(100):
        a.append(ii)
        
starting_numbers = '16,12,1,0,15,7,11'
starting_numbers = list( map(int, starting_numbers.split(',')) )

starting_points = len( starting_numbers )

spoken_numbers = defaultdict(def_value,
                             zip(starting_numbers,
                                 [ [ii] for ii in range(starting_points) ]) )


last_spoken = int(starting_numbers[-1])

for ii in range(starting_points, 30000000):
    spoken_turns = spoken_numbers[last_spoken]
    
    if len(spoken_turns) < 2:
        spoken = 0
        custom_append(spoken_numbers[spoken], ii)
    else:
        spoken = spoken_turns[1] - spoken_turns[0]
        custom_append(spoken_numbers[spoken], ii)    
    last_spoken = spoken

print(spoken)
    