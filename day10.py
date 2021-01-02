# -*- coding: utf-8 -*-
"""
Created on Sat Dec 12 15:06:28 2020

@author: Lucio
"""

import numpy as np


adapters = np.loadtxt('inputs/day10.txt', dtype = int)
adapters = sorted(adapters)
adapters = [0] + adapters + [adapters[-1] + 3] #Add the first outlet

jolt_diff = np.diff(adapters)

unique_differences = np.unique(jolt_diff)

amount_differences = []
for diff in unique_differences:
    amount_differences.append( len(jolt_diff[jolt_diff == diff]) )
    
print( amount_differences[0] * amount_differences[1] )

### Part 2
adapters_amt = len(adapters)
adapter_indices = np.arange(adapters_amt)
combo_counter = 1

combos_up_to_index = [1] * adapters_amt
for i in range(1, adapters_amt):
    combos_up_to_index[i] = combos_up_to_index[i - 1]
    
    if i > 1 and (adapters[i] - adapters[i - 2] <= 3):
        combos_up_to_index[i] += combos_up_to_index[i - 2]
        
    if i > 2 and (adapters[i] - adapters[ i - 3]) <= 3:
        combos_up_to_index[i] += combos_up_to_index[i - 3]

print(combos_up_to_index[-1])

    


