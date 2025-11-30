# -*- coding: utf-8 -*-
"""
Created on Mon Dec  7 14:25:44 2020

@author: Lucio
"""

import numpy as np

numbers = np.loadtxt('inputs/day1.txt', dtype = int)

searching_for_sum = True

ii = 0

while searching_for_sum:
    for number in numbers:
        summy = numbers[ii] + number
        if summy == 2020:
            first_number = numbers[ii]
            second_number = number
            searching_for_sum = False
            break
    ii += 1
    
print(first_number*second_number)
        
output_array = []
searching_for_sum = True
while searching_for_sum:
    for second_number in numbers:
        for third_number in numbers:
            summy = numbers[ii] + second_number + third_number
            if summy == 2020:
                output_array = [numbers[ii], second_number, third_number]
                searching_for_sum = False
                break
    ii += 1
    
print(np.prod(output_array))