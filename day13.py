# -*- coding: utf-8 -*-
"""
Created on Sun Dec 13 18:15:03 2020

@author: Lucio
"""

import numpy as np

with open('inputs/day13.txt') as file:
    my_time = int( file.readline() )
    
    buses_line = file.readline().strip().split(',')
    
    buses = [int(bus) for bus in buses_line if bus != 'x']
    
    complete_buses = [int(bus) if bus != 'x' else bus for bus in buses_line ]
    
    
closest_times = []

for bus in buses:
    
    closest_multiple = bus * ( my_time // bus )
    
    if closest_multiple < my_time:
        closest_multiple += bus
    
    closest_times.append(closest_multiple - my_time)
    
closest_time = min(closest_times)
bus_id = buses[ closest_times.index(closest_time) ]

print(bus_id * closest_time)

### Part 2

lags_rel_to_first = [0]


lag_counter = 0
for ii, bus in enumerate(complete_buses[1:]):
    lag_counter += 1

    if type(bus) is int:
        lags_rel_to_first.append(lag_counter)
        
t0 = 0
multiplier = 1

step = 1

for lag, bus in zip(lags_rel_to_first, buses):
    
    while (t0 + lag) % bus != 0:
        t0 += step
    step *= bus

            
print(t0)
            
        




