# -*- coding: utf-8 -*-
"""
Created on Sat Dec 12 12:17:42 2020

@author: Lucio
"""

def get_valid_sums(numbers):
    
    valid_sums = []
    
    for number in numbers:
        for second_number in numbers:
            valid_sums.append(number + second_number)
    return valid_sums

with open('inputs/day9.txt') as file:
    xmas_code = []
    for line in file.readlines():
        xmas_code.append(int( line ))
        

code_len = len(xmas_code)

start = 25
keep_going = True

ii = start
while keep_going:
    number = xmas_code[ii]
    last_idx = (ii-1-start) if (ii-1-start)>-1 else None
    
    previous_numbers = xmas_code[ii-1:last_idx:-1]
    valid_numbers = get_valid_sums(previous_numbers)
    if number not in valid_numbers:
       keep_going = False
       print(number)
    ii += 1

invalid_number = number

### Part two

keep_going = True
ii = 0
len_list = len(xmas_code)
while keep_going and (ii < len_list):
    
    
    vec_contiguous = []
    summy = 0
    
    jj = 0
    while (summy <= invalid_number) and (ii + jj < len_list) and keep_going:
        nummy = xmas_code[ii + jj]
        vec_contiguous.append(nummy)
        summy =  sum(vec_contiguous)
        if summy == invalid_number:
            keep_going = False
            print("Success")
        jj += 1
        
    ii += 1
    
weakness = min(vec_contiguous) + max(vec_contiguous)
print( weakness )
        
